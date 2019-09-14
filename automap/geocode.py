
import sqlite3


##class Matches(object):
##    def __init__(self, stream):
##        self.stream = stream
##        self.matches = []
##
##    def __bool__(self):
##        return next(self)
##
##    def __nonzero(self):
##        return self.__bool__()
##
##    def __next__(self):
##        nxt = next(self.stream, None)
##        if nxt:
##            self.matches.append(nxt)
##            return nxt
##
##    def __iter__(self):
##        for m in self.matches:
##            yield m
##            
##        nxt = next(self, None)
##        while nxt:
##            yield nxt
##            nxt = next(self, None)



class Online(object):
    def __init__(self):
        import geopy
        self.coder = geopy.geocoders.Nominatim()

    def geocode(self, name, limit=10):
        ms = self.coder.geocode(name, exactly_one=False, limit=limit) or []
        for m in ms:
            yield {'type': 'Feature',
                   'properties': {'name': m.address,
                                  },
                   'geometry': {'type': 'Point',
                                'coordinates': (m.longitude, m.latitude)
                                },
                   }



class OptimizedCoder(object):
    def __init__(self, path=None):
        self.path = path or r'C:\Users\kimok\Desktop\BIGDATA\gazetteer data\optim\gazetteers.db'
        self.db = sqlite3.connect(self.path)

    def geocode(self, name, limit=10):
        # NOT CORRRECT QUERY, RETURNS DUPLICATES
        results = self.db.cursor().execute("SELECT locs.data, locs.id, GROUP_CONCAT(names.name, '|'), locs.geom FROM locs, names, (SELECT data,id FROM names WHERE name = ?) AS m WHERE locs.id=m.id AND locs.data=m.data and names.id=m.id and names.data=m.data GROUP BY m.data,m.id", (name,))
        results = ({'type': 'Feature',
                   'properties': {'data':data,
                                  'id':ID,
                                  'name':names,
                                  'search':name,
                                  },
                   'geometry': geom.__geo_interface__,
                   } for data,ID,names,geom in results)
        return results #Matches(results)



class SQLiteCoder(object):
    def __init__(self, db=None, table=None):
        self.path = db
        self.db = sqlite3.connect(self.path)
        self.table = table

    def geocode(self, name, limit=10):
        #where = u"names like '%{0}%'".format(name)
        where = u" '|' || names || '|' like '%|{0}|%' ".format(name)
        #where = u"names like '{0}|%' or names like '%|{0}|%' or names like '%|{0}'".format(name)
        results = self.db.cursor.execute('select names,lon,lat from {table} where {where} limit {limit}'.format(table=self.table, where=where, limit=limit))
        results = ({'type': 'Feature',
                   'properties': {'name': names,
                                  },
                   'geometry': {'type': 'Point',
                                'coordinates': (lon,lat)
                                },
                   } for names,lon,lat in results)
        return results #Matches(results)


class GNS(SQLiteCoder):
    db = r'C:\Users\kimok\Desktop\BIGDATA\gazetteer data\prepped\gns.db'
    table = 'data'


class GeoNames(SQLiteCoder):
    db = r'C:\Users\kimok\Desktop\BIGDATA\gazetteer data\prepped\geonames.db'
    table = 'data'


class OSM(SQLiteCoder):
    db = r'C:\Users\kimok\Desktop\BIGDATA\gazetteer data\prepped\osm.db'
    table = 'data'


class CIESIN(SQLiteCoder):
    db = r'C:\Users\kimok\Desktop\BIGDATA\gazetteer data\prepped\ciesin.db'
    table = 'data'


class NatEarth(SQLiteCoder):
    db = r'C:\Users\kimok\Desktop\BIGDATA\gazetteer data\prepped\natearth.db'
    table = 'data'

