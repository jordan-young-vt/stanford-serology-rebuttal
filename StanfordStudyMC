import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import StanfordStudySensitivity as sss
from scipy import stats

#set variables

SANTA_CLARA_POP = 1928000
SANTA_CLARA_DEATHS = 100
US_POPULATION = 330000000

N = 3330
positive_tests = 50

sensitivity = 0.65
specificity = 0.995

sens_num = 78
sens_den = 85

spec_num = 369
spec_den = 371

#Simulation Parameters
OUTER_LOOPS = 1000
INNER_LOOPS = 500

class StanfordStudyMC():

	def __init__(self):
		self.sss = sss.StanfordStudySensitivity()

	def draw_bin(self,N,p):
		return numpy.random.binomial(N,p)*1.0/N

	def draw_bin_perc(self,N,p):
		try:
			return numpy.random.binomial(N,p)*1.0
		except ValueError:
			print(p)

	def simulate_adjusted_cases(self):
		sampled_pos = []

		# Draw A Specificity
		spec = self.draw_bin(spec_den,spec_num*1.0/spec_den)

		# Draw A Sensitivity
		sens = self.draw_bin(sens_den,sens_num*1.0/sens_den)
		for i in range(INNER_LOOPS):
			sampled_pos.append(self.sss.determine_adjusted_cases(N,self.draw_bin_perc(N,positive_tests*1.0/N),sens,spec))
		return sampled_pos

	def draw_distribution_given_inputs(self,times=1000):
		sampled_pos = []
		for i in range(times):
			sampled_pos.extend(self.simulate_adjusted_cases())
		return sampled_pos

	def times10(self,a):
		return a*10

	def div10(self,a, b):
		return a*1.0/10


	def plot_hist(self):
		# Set up Figure and variables
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)

		#Plot histogram
		#Adjusted upwards to make density values readable
		data = map(self.sss.adjust_to_implied_prevalence,self.draw_distribution_given_inputs(OUTER_LOOPS))
		plt.hist(data, color='#0504aa',bins=numpy.arange(0,7,0.1),normed=True,stacked=True)
		
		lb = numpy.percentile(data,2.5)
		ub = numpy.percentile(data,97.5)
		mean = numpy.average(data)
		# X-Axis
		plt.xlabel('Prevalence Rate')
		xticks = mtick.FormatStrFormatter('%.1f%%')
		ax.xaxis.set_major_formatter(xticks)

		plt.ylabel("Probability Density")
		yticks = mtick.FuncFormatter(self.div10)
		ax.yaxis.set_major_formatter(yticks)

		plt.title("Bootstrapped Prevalance Rates")

		plt.text(1.5,0.8,"Mean: %.2f%%\n95%% Confidence Bound: [%.2f%%,%.2f%%] " % (mean,lb,ub))

		plt.show()

if __name__=="__main__":
	
	ssmc = StanfordStudyMC()
	ssmc.plot_hist()

