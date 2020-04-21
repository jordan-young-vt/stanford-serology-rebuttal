import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import scipy.stats as st

#set variables

SANTA_CLARA_POP = 1928000
#SANTA_CLARA_POP = 8300000
SANTA_CLARA_DEATHS = 100
#SANTA_CLARA_DEATHS = 13000
US_POPULATION = 330000000

#Number tested
N = 3330
positive_tests = 50

#Default values
sensitivity = 0.8
specificity = 0.995

#raw test quality values
sens_num = 78
sens_den = 85

spec_num = 369
spec_den = 371

class StanfordStudySensitivity():
	# This function calculates the implied fatality rate in 
	def adjust_to_implied_fatality_rate(self,positive_test,N=N,population=SANTA_CLARA_POP,deaths=SANTA_CLARA_DEATHS):
		if (N > 0 and positive_test > 0):
			return deaths*1.0/(positive_test*1.0*population/N)*100
		elif positive_test == 0:
			return 0
		else:
			return None

	def id(self,positive_test,N=N,population=SANTA_CLARA_POP,deaths=SANTA_CLARA_DEATHS):
		return positive_test

	def adjust_to_implied_cases(self,positive_test,N=N,population=SANTA_CLARA_POP):
		return positive_test*1.0*population/N

	def adjust_to_implied_prevalence(self,positive_test,N=N,population=SANTA_CLARA_POP):
		return positive_test*100.0/N

	def adjust_to_implied_us_deaths(self,positive_tests,N=N,population=SANTA_CLARA_POP,deaths=SANTA_CLARA_DEATHS,total_pop=US_POPULATION):
		if (N > 0 and positive_tests > 0):
			return total_pop*self.adjust_to_implied_fatality_rate(positive_tests,N,population,deaths)/100
		else:
			return None

	def determine_adjusted_cases(self, N,positives,sens,spec):
		fp = N*(1-spec)
		tp = max(positives - fp,0)
		tn = max(N - tp*(1/sens) - fp,0)
		fn = N - tn - tp - fp
		return max(tp + fn,0)

	def compute_binomial_variance_normal(self,N,p):
		return N*p*(1-p)

	def compute_binomial_ci_normal(self, N,p,range):
		variance = self.compute_binomial_variance_normal(N,p)
		mean = N*p
		lower_bound_val = (1 - range)*1.0/2
		upper_bound_val = 1 - lower_bound_val
		lower_bound = max(mean + st.norm.ppf(lower_bound_val)*variance**0.5,0)
		upper_bound = mean + st.norm.ppf(upper_bound_val)*variance**0.5
		return lower_bound, upper_bound

	def compute_binomial_ci_poisson(self,N,p,range):
		lower_bound_val = (1 - range)*1.0/2
		upper_bound_val = 1 - lower_bound_val
		lower_bound = st.chi2.ppf(lower_bound_val,N*p)
		upper_bound = st.chi2.ppf(upper_bound_val,N*p)
		return lower_bound, upper_bound

	def generate_plot_data(self, fn, ci_fn, opt="spec"):
		specificities = numpy.arange(0.986, 1, 0.001)
		sensitivities = numpy.arange(0.5,1,0.05)
		x = []
		y = []
		xerr_right = []
		xerr_left = []
		if (opt=="spec"):
			for spec in specificities:
				l = self.determine_adjusted_cases(N,positive_tests,0.995,spec)
				x.append(fn(l))
				y.append(spec)
				lower_bound, upper_bound = ci_fn(N, l*1.0/N, 0.95)
				xerr_right.append(abs(fn(upper_bound)-fn(l)))
				xerr_left.append(abs(fn(lower_bound)-fn(l)))
		else:
			for sens in sensitivities:
				l = self.determine_adjusted_cases(N,positive_tests,sens,0.995)
				#l = self.determine_adjusted_cases(N,positive_tests,0.995,spec)
				x.append(fn(l))
				y.append(sens)
				lower_bound, upper_bound = ci_fn(N, l*1.0/N, 0.95)
				xerr_right.append(abs(fn(upper_bound)-fn(l)))
				xerr_left.append(abs(fn(lower_bound)-fn(l)))
		return x,y,xerr_right,xerr_left


	def plot_chart(self, fn, ci_fn, xlim, ylabel, fmt, inverse=False, opt="spec"):
		#set x-axis to be true positive rate
		#set y-axis to be test specificity
		#set right-bound error to be 95th percentile
		#set left-bound error to be 5th percentile
		x, y, xerr_right, xerr_left = self.generate_plot_data(fn, ci_fn, opt)

		print("Left error")
		print xerr_left
		print("right error")
		print xerr_right
		print ("means")
		print x
		print y

		#start plot
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		if(inverse):
			plt.errorbar(y, x, yerr=[xerr_right,xerr_left])
		else:
			plt.errorbar(y, x, yerr=[xerr_left,xerr_right])
		plt.ylim(xlim[0],xlim[1])
		
		if (opt=="spec"):
			plt.xlabel('Test Specificity')
			plt.title("Implied Fatality Rate by Test Specificity")
			plt.xlim(1.002,0.984)
		if (opt=="sens"):
			plt.xlabel('Test Sensitivity')
			plt.title("Implied Fatality Rate by Test Sensitivity")
			plt.xlim(0.49,1.01)
		plt.ylabel(ylabel)
		yticks = mtick.FormatStrFormatter('%.0f%%')
		ax.yaxis.set_major_formatter(yticks)
		plt.show()

if __name__=="__main__":
	study_rebut = StanfordStudySensitivity()
	study_rebut.plot_chart(study_rebut.adjust_to_implied_fatality_rate,study_rebut.compute_binomial_ci_poisson,[-1,10],'Implied Fatality Rate', '%.0f%%', True)
	study_rebut.plot_chart(study_rebut.adjust_to_implied_fatality_rate,study_rebut.compute_binomial_ci_poisson,[-1,10],'Implied Fatality Rate', '%.0f%%', True, "sens")

	#study_rebut.plot_chart(study_rebut.adjust_to_implied_fatality_rate,study_rebut.compute_binomial_ci_normal,[-1,10],'Implied Fatality Rate', '%.0f%%', True)
	#study_rebut.plot_chart(study_rebut.adjust_to_implied_cases,study_rebut.compute_binomial_ci_poisson,[0,100000],'Implied Fatality Rate', '%.0f%%')
	#study_rebut.plot_chart(study_rebut.adjust_to_implied_cases,study_rebut.compute_binomial_ci_normal,[0,100000],'Implied Fatality Rate', '%.0f%%')
	#study_rebut.plot_chart(study_rebut.adjust_to_implied_prevalence,study_rebut.compute_binomial_ci_poisson,[0,10],'Implied Prevalence Rate', '%.0f%%')
	#study_rebut.plot_chart(study_rebut.adjust_to_implied_prevalence,study_rebut.compute_binomial_ci_normal,[0,10],'Implied Prevalence Rate', '%.0f%%')



#plot_chart(adjust_to_implied_cases,[-10000,150000], 'Implied SC Cases', '%d')
#plot_chart(adjust_to_implied_us_deaths,[-10000,15000000], 'Implied US Deaths', '%d', True)
#result_array = []
#for i in range(1000):
#	result_array.extend(simulate_adjusted_cases())

#print(numpy.average(result_array))
#print(numpy.percentile(result_array,5))
#print(numpy.percentile(result_array,95))
