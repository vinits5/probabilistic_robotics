########################################################################
# Created by Vinit Sarode
# Ref. (http://ais.informatik.uni-freiburg.de/teaching/ss19/robotics/slides/06-motion-models.pdf)
########################################################################

import numpy as np 
import matplotlib.pyplot as plt 

# Sample from Normal Distribution
def sample12_normal(sigma):
	total = 0.0
	for i in range(12):
		total += (-2*sigma*np.random.rand()+sigma)
	return (total/2.0)

# Odometry Based Motion Model.
def odom_motion_model(particle, odometry, alpha):
	# Arguments
		# particle 		-> (x, y, theta)
		# odometry 		-> (delta-rot1, delta-rot2, delta-trans)
		# alpha 		-> (alpha1, alpha2, alpha3, alpha4)	
		# 				   (alpha1, alpha2 associate with noise in rotation and the other two are related to noise in translation.)
	# Output
		# new_particle	-> (x', y', theta') 

	u_t = np.array([odometry['r1'], odometry['r2'], odometry['t']])
	# Find Std. Dev. of Normal Distribution for noise in rotation and translation.
	sigma_rot1 = np.sqrt(alpha[0]*abs(odometry['r1']) + alpha[1]*odometry['t'])
	sigma_rot2 = np.sqrt(alpha[0]*abs(odometry['r2']) + alpha[1]*odometry['t'])
	sigma_trans = np.sqrt(alpha[2]*abs(odometry['t']) + alpha[3]*(abs(odometry['r1']) + abs(odometry['r2'])))

	# Add the sampled noise to the u_t (kind of measurement noise in sensor).
	new_odometry = dict()
	new_odometry['r1'] = odometry['r1'] + sample12_normal(sigma_rot1)
	new_odometry['r2'] = odometry['r2'] + sample12_normal(sigma_rot2)
	new_odometry['t'] = odometry['t'] + sample12_normal(sigma_trans)

	# Update the position of robot using the del_u_t.
	new_particle = dict()
	new_particle['x'] = particle['x'] + new_odometry['t']*np.cos(particle['theta']+new_odometry['r1'])
	new_particle['y'] = particle['y'] + new_odometry['t']*np.sin(particle['theta']+new_odometry['r1'])
	new_particle['theta'] = particle['theta'] + new_odometry['r1'] + new_odometry['r2']

	return new_particle

def likelihood(landmark, idx, particle, d, sigma=0.2):
	# landmark -> m
	# particle -> x
	# d is d

	# How to Use this Function:
	# m is location in the map.
	# x0 and x1 are the position from where readings are taken.
	# d0 & d1 are the distance measurements from the x0 and x1 respectively.
	# sigma0 & sigma1 are the std deviation of the gaussian with zero mean. 
	# p will give the probability of the location in the map given the
	# measurements by the sensor.

	# We will find P(d0|m)(At university) at x0(tower 0).
	d_c = np.sqrt((particle['x']-landmark[idx][0]) * (particle['x']-landmark[idx][0]) + (particle['y']-landmark[idx][1]) * (particle['y']-landmark[idx][1]))
	pdf = (1.0 / (np.sqrt(2*np.pi*sigma*sigma))) * np.exp(-(((d - d_c)*(d - d_c)) / (2.0*sigma*sigma)))

	return pdf