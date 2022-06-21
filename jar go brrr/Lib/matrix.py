# matrix.py, V1.0
# Adapted from Massimo Di Pierro, DePaul University, USA
# with thanks to the author

class Matrix():
    def __init__(self, rows, cols=1, fill=0.0):
        """
        Constructor a zero matrix
        Examples:
        A = Matrix([[1,2],[3,4]])
        A = Matrix([1,2,3,4])
        A = Matrix(10,20)
        A = Matrix(10,20,fill=0.0)
        A = Matrix(10,20,fill=lambda r,c: 1.0 if r==c else 0.0)
        """
        if isinstance(rows, list):
            if isinstance(rows[0], list):
                self.rows = [[e for e in row] for row in rows]
            else:
                self.rows = [[e] for e in rows]
        elif isinstance(rows,int) and isinstance(cols,int):
            xrows, xcols = xrange(rows), xrange(cols)
            if callable(fill):
                self.rows = [[fill(r,c) for c in xcols] for r in xrows]
            else:
                self.rows = [[fill for c in xcols] for r in xrows]
        else:
            raise RuntimeError("Unable to build matrix from %s" % repr(rows))
        self.nrows = len(self.rows)
        self.ncols = len(self.rows[0])

    def __getitem__(A, coords):
        " x = A[0,1]"
        i,j = coords
        return A.rows[i][j]

    def __setitem__(A, coords, value):
        " A[0,1] = 3.0 "
        i,j = coords
        A.rows[i][j] = value

    def tolist(A):
        " assert(Matrix([[1,2],[3,4]]).tolist() == [[1,2],[3,4]]) "
        return A.rows

    def __str__(A):
        return str(A.rows)

    def flatten(A):
        " assert(Matrix([[1,2],[3,4]]).flatten() == [1,2,3,4]) "
        return [A[r,c] for r in xrange(A.nrows) for c in xrange(A.ncols)]

    def reshape(A, n, m):
        " assert(Matrix([[1,2],[3,4]]).reshape(1,4).tolist() == [[1,2,3,4]]) "
        if n*m != A.nrows*A.ncols:
             raise RuntimeError("Impossible reshape")
        flat = A.flatten()
        return Matrix(n, m, fill=lambda r, c, m=m, flat=flat: flat[r*m+c])

    def swap_rows(A, i, j):
        " assert(Matrix([[1,2],[3,4]]).swap_rows(1,0).tolist() == [[3,4],[1,2]]) "
        A.rows[i], A.rows[j] = A.rows[j], A.rows[i]

    @staticmethod
    def identity(rows=1, e=1.0):
        return Matrix(rows, rows, lambda r, c, e=e: e if r == c else 0.0)

    @staticmethod
    def diagonal(d):
        return Matrix(len(d), len(d), lambda r, c, d=d:d[r] if r == c else 0.0)

    def __add__(A, B):
        """
        Adds A and B element by element, A and B must have the same size
        Example
        >>> A = Matrix([[4,3.0], [2,1.0]])
        >>> B = Matrix([[1,2.0], [3,4.0]])
        >>> C = A + B
        >>> print C
        [[5, 5.0], [5, 5.0]]
        """
        n, m = A.nrows, A.ncols
        if not isinstance(B,Matrix):
            if n==m:
                B = Matrix.identity(n,B)
            elif n==1 or m==1:
                B = Matrix([[B for c in xrange(m)] for r in xrange(n)])
        if B.nrows != n or B.ncols != m:
            raise ArithmeticError('incompatible dimensions')
        C = Matrix(n, m)
        for r in xrange(n):
            for c in xrange(m):
                C[r,c] = A[r,c] + B[r,c]
        return C

    def __sub__(A, B):
        """
        Adds A and B element by element, A and B must have the same size
        Example
        >>> A = Matrix([[4.0,3.0], [2.0,1.0]])
        >>> B = Matrix([[1.0,2.0], [3.0,4.0]])
        >>> C = A - B
        >>> print C
        [[3.0, 1.0], [-1.0, -3.0]]
        """
        n, m = A.nrows, A.ncols
        if not isinstance(B, Matrix):
            if n == m:
                B = Matrix.identity(n, B)
            elif n == 1 or m == 1:
                B = Matrix(n, m, fill=B)
        if B.nrows != n or B.ncols != m:
            raise ArithmeticError('Incompatible dimensions')
        C = Matrix(n, m)
        for r in xrange(n):
            for c in xrange(m):
                C[r,c] = A[r,c] - B[r,c]
        return C
    
    def __radd__(A, B): #B+A
        return A + B

    def __rsub__(A, B): #B-A
        return (-A) + B

    def __neg__(A):
        return Matrix(A.nrows, A.ncols, fill=lambda r, c:-A[r,c])

    def __rmul__(A, x):
        "multiplies a number of matrix A by a scalar number x"
        import copy
        M = copy.deepcopy(A)
        for r in xrange(M.nrows):
            for c in xrange(M.ncols):
                 M[r,c] *= x
        return M

    def __mul__(A, B):
        "multiplies a number of matrix A by another matrix B"
        if isinstance(B, (list,tuple)):
            return (A*Matrix(len(B),1, fill=lambda r, c:B[r])).nrows
        elif not isinstance(B, Matrix):
            return B * A
        elif A.ncols == 1 and B.ncols == 1 and A.nrows == B.nrows:
            # try a scalar product ;-)
            return sum(A[r,0] * B[r,0] for r in xrange(A.nrows))
        elif A.ncols != B.nrows:
            raise ArithmeticError('Incompatible dimension')
        M = Matrix(A.nrows, B.ncols)
        for r in xrange(A.nrows):
            for c in xrange(B.ncols):
                for k in xrange(A.ncols):
                    M[r,c] += A[r,k] *B [k,c]
        return M

    def div(A, x):
        """Computes x/A using Gauss-Jordan elimination where x is a scalar"""
        import copy
        n = A.ncols
        if A.nrows != n:
           raise ArithmeticError('matrix not squared')
        indexes = xrange(n)
        A = copy.deepcopy(A)
        B = Matrix.identity(n,x)
        for c in indexes:
            for r in xrange(c+1,n):
                if abs(A[r,c]) > abs(A[c,c]):
                    A.swap_rows(r, c)
                    B.swap_rows(r, c)
            p = 0.0 + A[c,c] # trick to make sure it is not integer
            for k in indexes:
                A[c,k] = A[c,k] / p
                B[c,k] = B[c,k] / p
            for r in range(0,c) + range(c+1,n):
                p = 0.0 + A[r,c] # trick to make sure it is not integer
                for k in indexes:
                    A[r,k] -= A[c,k] * p
                    B[r,k] -= B[c,k] * p
            # if DEBUG: print A, B
        return B
    
   # used when __future__ division is turned off
    def __div__(C, A):
        return A.div(1)
    
   # used when __future__ division is turned on
    def __truediv__(C, A):
        return A.div(1)
    
    def __pow__(A,x):
        if not isinstance(x, int):
           raise ArithmeticError('exponent not integer')
        if x == -1:
            C = Matrix(1)  # dummy
            return C / A
        if x == 0:
            return A * 0
        if x >= 0:
            C = A 
            for i in range(x - 1):
                C = C * A
            return C
        if x < -1:
            Z = A**(-x)
            return Z**(-1)
   
    @property
    def T(A):
        """Transposed of A"""
        return Matrix(A.ncols, A.nrows, fill=lambda r, c: A[c,r])

    @property
    def H(A):
        """Hermitian of A"""
        return Matrix(A.ncols, A.nrows, fill=lambda r, c: A[c,r].conj())
