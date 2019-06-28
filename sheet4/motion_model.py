########################################################################
# Solution to Sheet 4: Odometry Based Motion Model
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
def odom_motion_model(x_t, u_t, alpha):
	# Arguments
		# x_t 	-> (x, y, theta)
		# u_t 	-> (delta-rot1, delta-rot2, delta-trans)
		# alpha -> (alpha1, alpha2, alpha3, alpha4)	
		# 		   (alpha1, alpha2 associate with noise in rotation and the other two are related to noise in translation.)
	# Output
		# x_n	-> (x', y', theta') 

	# Find Std. Dev. of Normal Distribution for noise in rotation and translation.
	sigma_rot1 = np.sqrt(alpha[0]*abs(u_t[0]) + alpha[1]*u_t[2])
	sigma_rot2 = np.sqrt(alpha[0]*abs(u_t[1]) + alpha[1]*u_t[2])
	sigma_trans = np.sqrt(alpha[2]*abs(u_t[2]) + alpha[3]*(abs(u_t[0]) + abs(u_t[1])))

	# Add the sampled noise to the u_t (kind of measurement noise in sensor).
	del_u_t = np.zeros(u_t.shape)
	del_u_t[0] = u_t[0] + sample12_normal(sigma_rot1)
	del_u_t[1] = u_t[1] + sample12_normal(sigma_rot2)
	del_u_t[2] = u_t[2] + sample12_normal(sigma_trans)

	# Update the position of robot using the del_u_t.
	x_n = np.zeros(x_t.shape)
	x_n[0] = x_t[0] + del_u_t[2]*np.cos(x_t[2]+del_u_t[0])
	x_n[1] = x_t[1] + del_u_t[2]*np.sin(x_t[2]+del_u_t[0])
	x_n[2] = x_t[2] + del_u_t[0] + del_u_t[1]

	return x_n

def velocity_motion_model(x_t, u_t, alpha, dt):
	# Arguments
		# x_t 	-> (x, y, theta)
		# u_t 	-> (v, w, gamma)
		# alpha -> (alpha1, alpha2, alpha3, alpha4, alpha5, alpha6)	
		# dt 	-> (time)
	# Output
		# x_n	-> (x', y', theta')
	sigma_v = np.sqrt(alpha[0]*u_t[0]*u_t[0]+alpha[1]*u_t[1]*u_t[1])
	sigma_w = np.sqrt(alpha[2]*u_t[0]*u_t[0]+alpha[3]*u_t[1]*u_t[1])
	sigma_g = np.sqrt(alpha[4]*u_t[0]*u_t[0]+alpha[5]*u_t[1]*u_t[1])

	del_v = u_t[0] + sample12_normal(sigma_v)
	del_w = u_t[1] + sample12_normal(sigma_w)
	del_g = sample12_normal(sigma_g)

	x_n = np.zeros(x_t.shape)
	x_n[0] = x_t[0] - (del_v/del_w)*(np.sin(x_t[2]) - np.sin(x_t[2]+del_w*dt))
	x_n[1] = x_t[1] + (del_v/del_w)*(np.cos(x_t[2]) - np.cos(x_t[2]+del_w*dt))
	x_n[2] = x_t[2] + del_w*dt + del_g*dt

	return x_n

if __name__=='__main__':
	x_t = np.array([2.0, 4.0, 0.0])
	u_t_odom = np.array([np.pi/2, 0, 2.0])
	u_t_vel = np.array([2,2,0])
	alpha_odom = np.array([0.1, 0.1, 0.01, 0.01])
	alpha_vel = np.array([0.01,0.01,0.001,0.001,0.001,0.001])
	dt = 0.5

	# positions = np.array([odom_motion_model(x_t, u_t, alpha) for i in range(5000)])
	positions = np.array([velocity_motion_model(x_t, u_t_vel, alpha_vel, dt) for i in range(5000)])

	plt.figure()
	plt.scatter(positions[:,0], positions[:,1], s=2, c='red')
	plt.scatter(x_t[0], x_t[1], c='black')
	plt.xlim(0,4)
	plt.ylim(0,7)
	plt.show()