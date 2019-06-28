########################################################################
# Solution to Sheet 4
# Created by Vinit Sarode
########################################################################

import numpy as np 
import matplotlib.pyplot as plt 

# Exercise 1
def sample12_normal(mu, sigma):
	total = 0.0
	for i in range(12):
		total += (-2*sigma*np.random.rand()+sigma)
	return mu+(total/2)

def normal_distribution(query_pt, std_dev):
	return (1.0/np.sqrt(2*np.pi*np.pi))*np.exp(-(query_pt*query_pt)/(2.0*std_dev*std_dev))

def normal_distribution_mu(mu, query_pt, std_dev):
	return (1.0/np.sqrt(2*np.pi*np.pi))*np.exp(-((query_pt-mu)*(query_pt-mu))/(2.0*std_dev*std_dev))

def triangular_sampling(mu, sigma):
	return mu+(np.sqrt(6)/2.0)*((-2*sigma*np.random.rand()+sigma) + (-2*sigma*np.random.rand()+sigma))

# ------------------------------------------------------------------------------------------------------------------------
def round_up(number):
	count = 0
	if number-int(number) != 0:			# Check if number is an integer / decimal.
		remainder = -1
		while remainder<1:				# Check if the remainder is integer / decimal. [If it is integer then, number is also integer.]
			number = number*10			# Multiply the number by 10
			remainder = number%10		# Update the remainder.
			count += 1					# Count number of times multiplied by 10.
	return int(number), count	

def find_fmax(func, args, interval):
	b, power = round_up(interval)
	return max([func(i/(pow(10,power)*1.0), args[1]) for i in range(-b,b)])

def rejection_sampling(interval, func, args, f_max):
	sample_not_found = True
	while sample_not_found:
		sample = -2*interval*np.random.rand()+interval
		y = f_max*np.random.rand()
		f_x = func(sample, args[1])
		if y<f_x:
			return mu+sample

def complex_func(x, sigma):
	return normal_distribution_mu(-0.8, x, sigma) + normal_distribution_mu(1.5, x, sigma)

# ------------------------------------------------------------------------------------------------------------------------

# Box-Muller transformation
def sample_box_muller():
	u1 = np.random.rand()
	u2 = np.random.rand()
	return np.cos(2*np.pi*u1)*np.sqrt(-2*np.log(u2))

# ------------------------------------------------------------------------------------------------------------------------
def sample_distribution(mu, sigma, method, func=None, args=None):
	if method == triangular_sampling or method == sample12_normal:
		samples = [method(mu, sigma) for i in range(10000)]
	if method == rejection_sampling:
		interval = 5*sigma
		f_max = find_fmax(func, args, interval)
		samples = [method(interval, func, args, f_max) for i in range(10000)]
	if method == sample_box_muller:
		samples = [method() for i in range(10000)]

	plt.hist(samples, 100)
	plt.show()

if __name__ == '__main__':
	mu, sigma = 0.5, 0.5

	# F = []
	# for i in range(-int(sigma*1000),int(sigma*1000)):
	# 	F.append(normal_distribution(i/1000.0, sigma))
	# max_density = max(F)
	# for i in range(10000):
	# 	samples[i] = rejection_sampling(mu, sigma, max_density)

	sample_distribution(mu, sigma, rejection_sampling, complex_func, args=[mu, sigma])