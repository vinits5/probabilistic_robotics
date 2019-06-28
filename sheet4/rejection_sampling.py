import numpy as np
import matplotlib.pyplot as plt 

class RejectionSampling:
	def __init__(self, interval, func, args):
		self.interval = interval
		self.args = args
		self.func = func
		self.f_max = self.find_fmax()

	def round_up(self, number):
		count = 0
		if number-int(number) != 0:			# Check if number is an integer / decimal.
			remainder = -1
			while remainder<1:				# Check if the remainder is integer / decimal. [If it is integer then, number is also integer.]
				number = number*10			# Multiply the number by 10
				remainder = number%10		# Update the remainder.
				count += 1					# Count number of times multiplied by 10.
		return int(number), count	

	def find_fmax(self):
		b, power = self.round_up(self.interval)
		return max([self.func([i/(pow(10,power)*1.0), self.args[1], self.args[2]]) for i in range(-b,b)])

	def rejection_sampling(self):
		sample_not_found = True
		while sample_not_found:
			sample = -2*self.interval*np.random.rand()+self.interval
			y = self.f_max*np.random.rand()
			f_x = self.func([sample, self.args[1], self.args[2]])
			if y<f_x:
				return sample

	def sample(self, no_of_samples):
		self.samples = [self.rejection_sampling() for i in range(no_of_samples)]
		return self.samples

	def plot(self):
		plt.hist(self.samples, 100)
		plt.show()

def normal_distribution(query_pt, std_dev):
	return (1.0/np.sqrt(2*np.pi*np.pi))*np.exp(-(query_pt*query_pt)/(2.0*std_dev*std_dev))

def normal_distribution_mu(mu, query_pt, std_dev):
	return (1.0/np.sqrt(2*np.pi*np.pi))*np.exp(-((query_pt-mu)*(query_pt-mu))/(2.0*std_dev*std_dev))

def complex_func(args):
	return normal_distribution_mu(-1.5, args[0], args[2]) + normal_distribution_mu(1.5, args[0], args[2])


if __name__ == '__main__':
	interval = 0.5*5
	mu, sigma = 0, 0.5
	args = [0, mu, sigma]

	rej_samp = RejectionSampling(interval, complex_func, args)
	rej_samp.sample(10000)
	rej_samp.plot()