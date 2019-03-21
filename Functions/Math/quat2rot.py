import numpy
def quat2rot(q):
	return transpose(matrix([ \
	1-2*q[2]**2-2*q[3]**2, \
	2*(q[1]*q[2] + q[3]*q[4]), \
    2*(q[1]*q[3] - q[2]*q[4]); \
	2*(q[1]*q[2] - q[3]*q[4]), \
    1-2*q[1]**2-2*q[3]**2, \
    2*(q[2]*q[3] + q[1]*q[4]); \
    2*(q[1]*q[3] + q[2]*q[4]), \
    2*(q[2]*q[3] - q[1]*q[4]), \
    1-2*q[1]**2 - 2*q[2]**2]))