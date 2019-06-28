########################################################################
# Solution to Sheet 2
# Created by Vinit Sarode
########################################################################

import numpy as np 
import matplotlib.pyplot as plt 

# Implemenation of Differential Drive Kinematics
def diffdrive(x, y, theta, v_l, v_r, t, l):
	# Arguments:
		# x:		position on x-axis
		# y:		position on y-axis
		# theta:	orientation of robot
		# v_l:		velocity of left wheel
		# v_r:		velocity of right wheel
		# t:		time of motion
		# l:		distance between two wheels
	# Ouput:
		# x_n:		position on x-axis after motion
		# y_n:		position on y-axis after motion
		# theta_n:	orientation of robot after motion

	if v_l == v_r: 
		theta_n = theta
		x_n = x + v_l*t*np.cos(theta)
		y_n = y + v_l*t*np.sin(theta)
	else:
		w = (v_r - v_l)/(l*1.0)
		R = (l/2.0)*((v_r + v_l)/(v_r - v_l))
		ICC = [x - R*np.sin(theta), y + R*np.cos(theta)]

		sin, cos = np.sin(w*t), np.cos(w*t)
		T = np.array([[cos, -sin, 0.0],
					  [sin,  cos, 0.0],
					  [0.0,  0.0, 1.0]])

		ans = (np.matmul(T, np.array([x-ICC[0], y-ICC[1], theta]).T) + np.array([ICC[0], ICC[1], w*t])).T
		x_n, y_n, theta_n = ans

	return x_n, y_n, theta_n

def plot(x, y, theta):
	dl = 0.2
	plt.arrow(x, y, dl*np.cos(theta), dl*np.sin(theta), width=0.015)


if __name__ == '__main__':
	l = 0.5
	x_i, y_i, theta_i = 1.5, 2.0, np.pi/2

	x_1, y_1, theta_1 = diffdrive(x_i, y_i, theta_i, 0.3, 0.3, 3, l)
	x_2, y_2, theta_2 = diffdrive(x_1, y_1, theta_1, 0.1, -0.1, 1, l)
	x_3, y_3, theta_3 = diffdrive(x_2, y_2, theta_2, 0.2, 0.0, 2, l)

	print('Initial Position: x: {0}, y: {1}, theta: {2}'.format(x_i, y_i, theta_i))
	print('First Position: x: {0}, y: {1}, theta: {2}'.format(x_1, y_1, theta_1))
	print('Second Position: x: {0}, y: {1}, theta: {2}'.format(x_2, y_2, theta_2))
	print('Third Position: x: {0}, y: {1}, theta: {2}'.format(x_3, y_3, theta_3))

	plt.figure()
	plt.xlim(1,3)
	plt.ylim(1.5,3.5)
	plt.xlabel('X-Axis')
	plt.ylabel('X-Axis')
	plt.title('Motion of Robot')
	plt.gca().set_aspect('equal', adjustable='box')
	plot(x_i, y_i, theta_i)
	plot(x_1, y_1, theta_1)
	plot(x_2, y_2, theta_2)
	plot(x_3, y_3, theta_3)
	plt.plot([x_i,x_1,x_2,x_3], [y_i,y_1,y_2,y_3], linestyle='--', color='black')
	plt.show()