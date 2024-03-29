#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as PLOT
import numpy.polynomial.polynomial as PLN
import numpy.random as RANDOM
from time import time as TIME
from datetime import datetime as DATETIME


def main():
   left = -1
   right = 1
   number_experiment = 384
   degree_correct_low = 24
   degree_correct_high = 32
   choice_degree_model = [[12, 40], [8, 48]]
   choice_number_sample = [240, 320]
   '''
   number_experiment = 48
   degree_correct_low = 24
   degree_correct_high = 32
   choice_degree_model = [[12, 40], [8, 48]]
   choice_number_sample = [240, 320]
   '''

   time_start = TIME()
   for number_sample in choice_number_sample:
      print("number of sample", number_sample)
      for pair_degree in choice_degree_model:
         #print("pair", pair_degree)
         print("  ", "range of estimated degree", pair_degree)
         degree_model_low = pair_degree[0]
         degree_model_high = pair_degree[1]
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
   time_end = TIME()
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
   threshold_big = 1e3
   threshold_small = 1e-3

   range_degree_correct = range(degree_correct_low, degree_correct_high + 1)
   akaike = []
   bayes = []

   for degree_correct in range_degree_correct:
      print(
         "    ",
         '(', DATETIME.now().strftime('%H:%M'), ')',
         "true degree", degree_correct,
      )
      total = NP.array([0.0, 0.0])
      for _ in range(number_experiment):
         while (True):
            try:
               hold = learn(
                  left = left,
                  right = right,
                  number_sample = number_sample,
                  degree_model_low = degree_model_low,
                  degree_model_high = degree_model_high,
                  degree_correct = degree_correct,
               )
            except NP.linalg.LinAlgError:
               continue
            flag = True
            if (hold[0] < 0): flag = False
            if (hold[1] < 0): flag = False
            if (hold[0] > threshold_big): flag = False
            if (hold[1] > threshold_big): flag = False
            if (NP.abs(hold[1] - hold[0]) < threshold_small): flag = False
            if (flag): break
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
      "current/plot"
      + '-' + "times" + '-' + str(number_experiment).zfill(2)
      + '-' + "sample" + '-' + str(number_sample).zfill(2)
      + '-' + "degree" + '-' + str(degree_model_low).zfill(2)
      + '-' + str(degree_model_high).zfill(2)
      + '.' + "png"
   )
   PLOT.legend()
   PLOT.savefig(title, dpi=300)
   PLOT.clf()

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
   evaluation = PLN.polyval(sample, correct)
   noise = RANDOM.default_rng().standard_normal(number_sample)
   observation = evaluation + noise
   range_degree_model = range(degree_model_low, degree_model_high)
   record_loss = []
   record_akaike = []
   record_bayes = []

   for degree in range_degree_model:
      estimator = PLN.polyfit(sample, observation, degree)
      loss = find_loss(left, right, correct, estimator)
      likelihood = find_likelihood(sample, correct, estimator)
      akaike = - 2 * likelihood + 2 * degree
      bayes = - 2 * likelihood + NP.log(number_sample) * degree
      record_loss.append(loss)
      record_akaike.append(akaike)
      record_bayes.append(bayes)

   loss_akaike = record_loss[NP.argmin(record_akaike)]
   loss_bayes = record_loss[NP.argmin(record_bayes)]
   return NP.array([loss_akaike, loss_bayes])

def find_likelihood(sample, polynomial_one, polynomial_two):
   value_one = PLN.polyval(sample, polynomial_one)
   value_two = PLN.polyval(sample, polynomial_two)
   difference = value_one - value_two
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
