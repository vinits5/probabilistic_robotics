########################################################################
# Solution to Sheet 5
# Created by Vinit Sarode
########################################################################

import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

def likelihood(m, x0, x1, d0, d1, sigma0, sigma1):
	# How to Use this Function:
	# m is location in the map.
	# x0 and x1 are the position from where readings are taken.
	# d0 & d1 are the distance measurements from the x0 and x1 respectively.
	# sigma0 & sigma1 are the std deviation of the gaussian with zero mean. 
	# p will give the probability of the location in the map given the
	# measurements by the sensor.

	# we have to find P(m|d).
	# By bayes rule, P(m|d)=(P(d|m)*P(m))/P(d).
	# Here P(m) is assumed to be uniform.
	# As P(m) is uniform and P(d) is just a normalization factor P(m|d) is
	# proportional to P(d|m).
	# Now, we have to find P(d|m).
	# We have assumed that two distances d0 and d1 are independent of each
	# other. Hence P(d|m)=P(d0|m)*P(d1|m).

	# Here first we have calculated the distance between the position in map and
	# the position of tower 0.
	# Then we will calculate probability using normal probability function with
	# calculated distace (d0c) as mean and measured distance by sensor in
	# tower1
	# Then we will do it same for d1 (sensor meauserment).

	# We will find P(d0|m)(At university) at x0(tower 0).
	d0c=np.sqrt((x0[0]-m[0]) * (x0[0]-m[0]) + (x0[1]-m[1]) * (x0[1]-m[1]))
	pdf0=(1.0 / (np.sqrt(2*np.pi*sigma0*sigma0))) * np.exp(-(((d0-d0c)*(d0-d0c)) / (2.0*sigma0*sigma0)))

	# We will find P(d0|m)(at friend's room) at x1(tower 1).
	d1c=np.sqrt((x1[0]-m[0]) * (x1[0]-m[0]) + (x1[1]-m[1]) * (x1[1]-m[1]))
	pdf1=(1.0 / (np.sqrt(2*np.pi*sigma1*sigma1))) * np.exp(-(((d1-d1c)*(d1-d1c)) / (2*sigma1*sigma1)));

	return pdf0*pdf1

def SensorModel():
	 # we have to find P(m|d).
	 # By bayes rule, P(m|d)=(P(d|m)*P(m))/P(d).
	 # Here P(m) is assumed to be uniform.
	 # As P(m) is uniform and P(d) is just a normalization factor P(m|d) is
	 # proportional to P(d|m).
	 # Now, we have to find P(d|m).
	 # We have assumed that two distances d0 and d1 are independent of each
	 # other. Hence P(d|m)=P(d0|m)*P(d1|m).

	m0=[10,8]			# Location of Uni of Freiburg.
	m1=[6,3]			# Location of friend's house.
	x0=[12,4]           # Location of cell tower 1.
	x1=[5,7]            # Location of cell tower 2.
	sigma0=1            # Std deviation for zero mean variance for measurements of tower 1.
	sigma1=np.sqrt(1.5)    # Std deviation for zero mean variance for measurements of tower 2.
	d0=3.9  	        # Measurements from the tower 1.
	d1=4.5	            # Measurements from the tower 2.

	x = np.arange(30,150,5)/10.0
	y = np.arange(-50,150,5)/10.
	P = np.zeros((y.shape[0],x.shape[0]))
	for i in range(y.shape[0]):
		for j in range(x.shape[0]):
			P[i,j] = likelihood([x[j], y[i]], x0, x1, d0, d1, sigma0, sigma1)

	[X,Y] = np.meshgrid(x,y)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(X,Y,P)
	plt.show()
	

if __name__=='__main__':
	SensorModel()