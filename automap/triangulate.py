"""
"""

import itertools

import geopy

from . import shapematch


def geocode(name):
    coder = geopy.geocoders.Nominatim()
    ms = coder.geocode(name, exactly_one=False, limit=100)
    for m in ms:
        yield {'type': 'Feature',
               'properties': {'name': m.address,
                              },
               'geometry': {'type': 'Point',
                            'coordinates': (m.longitude, m.latitude)
                            },
               }

def triangulate(names, positions):
    assert len(names) == len(positions)
    assert len(names) >= 3

    # define input names/positions as a polygon feature
    findpoly = {'type': 'Feature',
               'properties': {'combination': names,
                              },
               'geometry': {'type': 'Polygon',
                            'coordinates': [positions]
                            },
               }

    # find matches for each name
    print 'finding matches'
    matchcandidates = []
    for name in names:
        match = geocode(name)
        if match:
            matchcandidates.append(list(match))
            
    for match in matchcandidates:
        print len(match)

    # find unique combinations of all possible candidates
    print 'combining'
    combis = list(itertools.product(*matchcandidates))
    combipolys = []
    for combi in combis:
        #print '--->', combi
        # make into polygon feature
        combinames = [f['properties']['name'] for f in combi]
        combipositions = [f['geometry']['coordinates'] for f in combi]
        combipoly = {'type': 'Feature',
                   'properties': {'combination': combinames,
                                  },
                   'geometry': {'type': 'Polygon',
                                'coordinates': [combipositions]
                                },
                   }
        combipolys.append(combipoly)

    # prep/normalize combipolys
    print 'prepping'
    combipolys = shapematch.prep_pool(combipolys)

    # find closest match
    print 'finding'
    matches = shapematch.find_exact_match_prepped(findpoly, combipolys)
    return matches



        
