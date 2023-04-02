#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as PLOT
import numpy.polynomial.polynomial as PLN
import numpy.random as RANDOM
'''
import warnings as WN
with WN.catch_warnings():
   WN.filterwarnings('error')
   try:
      estimator = NP.polyfit(sample, observation, degree)
   except NP.RankWarning:
      print("not enough data")
'''

def test():
   poly = NP.array([0,0,1])
   x = 2
   print("poly", poly)
   print("point", x)
   print("value", PLN.polyval(x, poly))

'''
def test():
   left = -4
   right = 4

   for _ in range(300):
      poly = NP.array(RANDOM.default_rng().uniform(left, right, 4))
      square = PLN.polypow(poly, 2)
      antiderivative = PLN.polyint(square)

   poly = NP.array([-2.0, 2.0, 3.3, 0.6])
   square = PLN.polypow(poly, 2)
   print("square", square)
   antiderivative = PLN.polyint(square)
   print("antiderivative", antiderivative)
   print("right", NP.polyval(antiderivative, right))
   print("left", NP.polyval(antiderivative, left))

   try:
      assert (NP.polyval(antiderivative, right) - NP.polyval(antiderivative, left) > 0)
   except AssertionError:
      print("poly", poly)
      raise
'''

def main():
   number_experiment = 24
   left = -4
   right = 4
   degree_correct_low = 9
   degree_correct_high = 18
   choice_degree_model_low = [6, 3]
   choice_degree_model_high = [32, 24]
   choice_number_sample = [90, 120, 150]

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

def simulate(**setup):
   left = setup["left"]
   right = setup["right"]
   number_experiment = setup["number_experiment"]
   number_sample = setup["number_sample"]
   degree_model_low = setup["degree_model_low"]
   degree_model_high = setup["degree_model_high"]
   degree_correct_low = setup["degree_correct_low"]
   degree_correct_high = setup["degree_correct_high"]

   range_degree_correct = range(degree_correct_low, degree_correct_high + 1)
   akaike = []
   bayes = []

   for degree_correct in range_degree_correct:
      print("      ", "calculating for true degree", degree_correct)
      total = NP.array([0.0, 0.0])
      for _ in range(number_experiment):
         total += learn(
            left = left,
            right = right,
            number_sample = number_sample,
            degree_model_low = degree_model_low,
            degree_model_high = degree_model_high,
            degree_correct = degree_correct,
         )
      total /= number_experiment
      akaike.append(total[0])
      bayes.append(total[1])

   PLOT.plot(range_degree_correct, akaike)
   PLOT.plot(range_degree_correct, bayes)
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

def learn(**setup):
   left = setup["left"]
   right = setup["right"]
   number_sample = setup["number_sample"]
   degree_model_low = setup["degree_model_low"]
   degree_model_high = setup["degree_model_high"]
   degree_correct = setup["degree_correct"]

   root = RANDOM.default_rng().uniform(left, right, degree_correct)
   sample = RANDOM.default_rng().uniform(left, right, number_sample)
   correct = PLN.polyfromroots(root)
   range_degree_model = range(degree_model_low, degree_model_high)
   record_loss = []
   record_akaike = []
   record_bayes = []

   for degree in range_degree_model:
      evaluation = NP.polyval(correct, sample)
      noise = RANDOM.default_rng().standard_normal(number_sample)
      observation = evaluation + noise
      estimator = NP.polyfit(sample, observation, degree)
      loss = find_loss(left, right, correct, estimator)
      likelihood = find_likelihood(correct, estimator)
      akaike = - 2 * likelihood + 2 * degree
      bayes = - 2 * likelihood + NP.log(number_sample) * degree
      record_loss.append(loss)
      record_akaike.append(akaike)
      record_bayes.append(bayes)

   loss_akaike = record_loss[NP.argmin(record_akaike)]
   loss_bayes = record_loss[NP.argmin(record_bayes)]
   print("record_loss", record_loss)
   return NP.array([loss_akaike, loss_bayes])

def find_likelihood(polynomial_one, polynomial_two):
   difference = NP.polysub(polynomial_one, polynomial_two)
   result = 0
   result += - (1/2) * NP.log(2 * NP.pi) * difference.size
   result += NP.sum(- (difference * difference) / 2)
   return result

def find_loss(left, right, polynomial_one, polynomial_two):
   difference = NP.polysub(polynomial_one, polynomial_two)
   square = PLN.polypow(difference, 2)
   print("square", square)
   antiderivative = PLN.polyint(square)
   print("antiderivative", antiderivative)
   result = 0
   result += NP.polyval(antiderivative, right)
   result -= NP.polyval(antiderivative, left)
   #result = NP.log(result)
   print("result", result)
   return result

# # # # # # # # # # # # # # # # # # # # # # # #

#main()

test()
