#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as PLOT
import numpy.polynomial.polynomial as PLN
import numpy.random as RANDOM
from time import time


'''
def test():
   left = -8
   right = 8
   for _ in range(20000):
      poly = RANDOM.default_rng().uniform(left, right, 12)
      square = PLN.polypow(poly, 2)
      #print("square", square)
      antiderivative = PLN.polyint(square)
      #print("antiderivative", antiderivative)
      result = 0
      result += PLN.polyval(right, antiderivative)
      result -= PLN.polyval(left, antiderivative)
      assert(result >= 0)
      result = NP.log(result)
'''

def main():
   number_experiment = 128
   left = -4
   right = 4
   degree_correct_low = 12
   degree_correct_high = 18
   choice_degree_model_low = [6, 9]
   choice_degree_model_high = [32, 24]
   choice_number_sample = [64, 96]

   time_start = time()
   for number_sample in choice_number_sample:
      print("number of sample", number_sample)
      for degree_model_low in choice_degree_model_low:
         print("  ", "lowest degree of estimator", degree_model_low)
         for degree_model_high in choice_degree_model_high:
            print("    ", "highest degree of estimator", degree_model_high)
            simulate(
               left = left,
               right = right,
               number_experiment = number_experiment,
               number_sample = number_sample,
               degree_model_low = degree_model_low,
               degree_model_high = degree_model_high,
               degree_correct_low = degree_correct_low,
               degree_correct_high = degree_correct_high,
            )
   time_end = time()
   time_total = (time_end - time_start) / 60
   print("time taken:", f"{time_total:.3f}", "minutes")


def simulate(**setup):
   left = setup["left"]
   right = setup["right"]
   number_experiment = setup["number_experiment"]
   number_sample = setup["number_sample"]
   degree_model_low = setup["degree_model_low"]
   degree_model_high = setup["degree_model_high"]
   degree_correct_low = setup["degree_correct_low"]
   degree_correct_high = setup["degree_correct_high"]
   threshold = 1e3

   range_degree_correct = range(degree_correct_low, degree_correct_high + 1)
   akaike = []
   bayes = []

   for degree_correct in range_degree_correct:
      print("      ", "calculating for true degree", degree_correct)
      total = NP.array([0.0, 0.0])
      for _ in range(number_experiment):
         hold = learn(
            left = left,
            right = right,
            number_sample = number_sample,
            degree_model_low = degree_model_low,
            degree_model_high = degree_model_high,
            degree_correct = degree_correct,
         )
         if (NP.abs(total[0]) > threshold): continue
         if (NP.abs(total[1]) > threshold): continue
         total += hold
      total /= number_experiment
      akaike.append(total[0])
      bayes.append(total[1])

   PLOT.plot(range_degree_correct, akaike, label = "akaike")
   PLOT.plot(range_degree_correct, bayes, label = "bayes")
   PLOT.xlabel("degree of true polynomial")
   PLOT.ylabel("squared loss")
   PLOT.title("Information Criteria")
   title = (
      "plot"
      + '-' + "sample" + '-' + str(number_sample).zfill(2)
      + '-' + "degree" + '-' + str(degree_model_low).zfill(2)
      + '-' + str(degree_model_high)
      + '.' + "png"
   )
   PLOT.savefig(title, dpi=300)
   PLOT.clf()

def learn(**setup):
   left = setup["left"]
   right = setup["right"]
   number_sample = setup["number_sample"]
   degree_model_low = setup["degree_model_low"]
   degree_model_high = setup["degree_model_high"]
   degree_correct = setup["degree_correct"]
   threshold = 1e3

   root = RANDOM.default_rng().uniform(left, right, degree_correct)
   sample = RANDOM.default_rng().uniform(left, right, number_sample)
   correct = PLN.polyfromroots(root)
   range_degree_model = range(degree_model_low, degree_model_high)
   record_loss = []
   record_akaike = []
   record_bayes = []

   for degree in range_degree_model:
      evaluation = PLN.polyval(sample, correct)
      noise = RANDOM.default_rng().standard_normal(number_sample)
      observation = evaluation + noise
      estimator = PLN.polyfit(sample, observation, degree)
      loss = find_loss(left, right, correct, estimator)
      likelihood = find_likelihood(correct, estimator)
      akaike = - 2 * likelihood + 2 * degree
      bayes = - 2 * likelihood + NP.log(number_sample) * degree

      if (loss > threshold): loss = threshold
      if (loss < - threshold): loss = - threshold
      if (akaike > threshold): akaike = threshold
      if (akaike < - threshold): akaike = - threshold
      if (bayes > threshold): bayes = threshold
      if (bayes < - threshold): bayes = - threshold
      record_loss.append(loss)
      record_akaike.append(akaike)
      record_bayes.append(bayes)

   loss_akaike = record_loss[NP.argmin(record_akaike)]
   loss_bayes = record_loss[NP.argmin(record_bayes)]
   return NP.array([loss_akaike, loss_bayes])

def find_likelihood(polynomial_one, polynomial_two):
   difference = PLN.polysub(polynomial_one, polynomial_two)
   result = 0
   result += - (1/2) * NP.log(2 * NP.pi) * difference.size
   result += NP.sum(- (difference * difference) / 2)
   return result

def find_loss(left, right, polynomial_one, polynomial_two):
   difference = PLN.polysub(polynomial_one, polynomial_two)
   square = PLN.polypow(difference, 2)
   antiderivative = PLN.polyint(square)
   result = 0
   result += PLN.polyval(right, antiderivative)
   result -= PLN.polyval(left, antiderivative)
   return result

# # # # # # # # # # # # # # # # # # # # # # # #

main()

#test()
