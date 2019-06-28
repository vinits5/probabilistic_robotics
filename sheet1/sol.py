########################################################################
# Solution to Sheet 1
# Created by Vinit Sarode
########################################################################

import numpy as np 
import math
import matplotlib.pyplot as plt

# Exercise  1, Question C
def check_orthogonal(matrix):
	matrix_t = matrix.T 
	assert len(matrix.shape) == 2, "Oops! Not a 2D matrix!"
	assert matrix.shape[0] == matrix.shape[1], "Oops! Not a square matrix!"

	if (np.matmul(matrix, matrix_t) == np.eye(matrix.shape[0])).all():
		print('Yes! Given Matrix is Orthogonal.')
		return True
	else:
		print('No! Given Matrix is not Orthogonal.')
		return False

# Exercies 3,
def read_sensor_data(filename):
	scan = np.loadtxt(filename)
	angle = np.linspace(-math.pi/2, math.pi/2, scan.shape[0], endpoint='true')
	return scan, angle

def laser_points(scan, angle):
	laserdata = np.ones((scan.shape[0],3))
	for idx, val in enumerate(scan):
		laserdata[idx,0] = val*np.cos(angle[idx])
		laserdata[idx,1] = val*np.sin(angle[idx])
	return laserdata

def plot_laser_data(laserdata, title=''):
	plt.scatter(laserdata[:,0],laserdata[:,1])
	plt.xlabel('X-axis')
	plt.ylabel('Y-axis')
	plt.gca().set_aspect('equal', adjustable='box')
	plt.title(title)
	plt.show()

def global_laser_data(laserdata, robot_pos):
	sin, cos = np.sin(np.pi), np.cos(np.pi)
	T_sensor2robot = np.array([[cos, -sin, 0.2],
							   [sin, cos,  0.0],
							   [0,    0,   1.0]])
	
	sin, cos = np.sin(robot_pos[2]), np.cos(robot_pos[2])
	T_robot2global = np.array([[cos, -sin, robot_pos[0]],
							   [sin, cos,  robot_pos[1]],
							   [0,    0,   1.0]])

	T_sensor2global = np.matmul(T_robot2global, T_sensor2robot)
	laserdata = (np.matmul(T_sensor2global, laserdata.T)).T
	return laserdata

if __name__ == '__main__':
	# Exercise 1, Question D
	D = (1/3.0)*np.array([[2,2,-1],[2,-1,2],[-1,2,2]])
	print('Given Matrix:\n {}'.format(D))
	check_orthogonal(np.eye(3))

	# Exercies 3, Question A
	scan, angle = read_sensor_data('laserscan.dat')
	plot_laser_data(laser_points(scan, angle), title='Plot of all laser-end points in sensor frame')

	# Exercise 3, Question C
	plot_laser_data(global_laser_data(laser_points(scan, angle), [1.0, 0.5, np.pi/4]), title='Plot of all laser-end points in global frame')