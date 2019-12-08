
import numpy as np

class Polynomial(object):
    
    def __init__(self, order=None, A=None):
        if A is not None:
            A = np.array(A)
            if A.shape == (3,3):
                order = 1
            elif A.shape == (6,6):
                order = 2
            else:
                raise ValueError('Matrix A must be shape (3,3), or (6,6); not {}'.format(A.shape))

        self.A = A
        self.order = order

    def fit(self, inx, iny, outx, outy, invert=True):
        # to arrays
        inx = np.array(inx)
        iny = np.array(iny)
        outx = np.array(outx)
        outy = np.array(outy)
        
        if self.order == 1:
            # terms
            x = inx
            y = iny
            ones = np.ones(x.shape)
            # u consists of each term in equation, with each term being array if want to transform multiple
            u = np.array([x,y,ones]).transpose()
            # x and y coeffs
            xcoeffs,xres,xrank,xsing = np.linalg.lstsq(u, outx, rcond=-1) 
            ycoeffs,yres,yrank,ysing = np.linalg.lstsq(u, outy, rcond=-1)
            # A matrix
            A = np.eye(3)
            
        elif self.order == 2:
            # terms
            x = inx
            y = iny
            xx = x*x
            xy = x*y
            yy = y*y
            ones = np.ones(x.shape)
            # u consists of each term in equation, with each term being array if want to transform multiple
            u = np.array([xx,xy,yy,x,y,ones]).transpose()
            # x and y coeffs
            xcoeffs,xres,xrank,xsing = np.linalg.lstsq(u, outx, rcond=-1) 
            ycoeffs,yres,yrank,ysing = np.linalg.lstsq(u, outy, rcond=-1)
            # A matrix
            A = np.eye(6)

        # Two first rows of the A matrix are equations for the x and y coordinates, respectively
        A[0,:] = xcoeffs
        A[1,:] = ycoeffs
        self.A = A

        # Also invert
        if invert:
            if self.order == 1:
                inv = np.linalg.inv(self.A)

            elif self.order == 2:
                inv = Polynomial(self.order).fit(outx,outy, inx,iny, invert=False).A

            self.inv = inv
        
        return self

    def predict(self, x, y, invert=False):
        # to arrays
        x = np.array(x)
        y = np.array(y)

        # input
        u = np.array([x,y])
        
        if self.order == 1:
            # terms
            x = x
            y = y
            ones = np.ones(x.shape)
            # u consists of each term in equation, with each term being array if want to transform multiple
            u = np.array([x,y,ones])
            
        elif self.order == 2:
            # terms
            x = x
            y = y
            xx = x*x
            xy = x*y
            yy = y*y
            ones = np.ones(x.shape)
            # u consists of each term in equation, with each term being array if want to transform multiple
            u = np.array([xx,xy,yy,x,y,ones])

        # apply the transform matrix to predict output
        if invert:
            predx,predy = self.inv.dot(u)[:2]
        else:
            predx,predy = self.A.dot(u)[:2]
        return predx,predy





    
