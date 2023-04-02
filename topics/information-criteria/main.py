#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as PLOT
import numpy.polynomial as PLN

def main():
   left = -8
   right = 8
   degree_maximum = 20
   degree_true = 5
   number_sample = 20
   root = RANDOM.default_rng().uniform(degree_true, left, right)
   sample = RANDOM.default_rng().uniform(number_sample, left, right)
   true = PLN.polyfromroots(root)

   record_loss = zeros(degree_maximum)
   record_akaike = zeros(degree_maximum)
   record_bayes = zeros(degree_maximum)
   for degree_fitted in range(1, degree_maximum + 1):
      evaluation = NP.polyval(true, sample)
      noise = RANDOM.default_rng().standard_normal(number_sample)
      observation = evaluation + noise
      estimator = NP.polyfit(sample, observation, degree_fitted)
      loss = find_loss(true, estimator, left, right)
      likelihood = find_likelihood(true, estimator)

'''
   x = NP.linspace(0, 10, 100)
   y_1 = 4 + 2 * NP.sin(2 * x)
   y_2 = 2 + 3 * NP.sin(4 * x)

   PLOT.plot(x, y_1)
   PLOT.plot(x, y_2)
   PLOT.xlabel("X-axis data")
   PLOT.ylabel("Y-axis data")
   PLOT.title('Information Criteria')
   PLOT.savefig('foo.png', dpi=300)
'''

def find_loss(polynomial_one, polynomial_two, left, right):
   difference = NP.polysub(polynomial_one, polynomial_two)
   square = difference.polypow()
   antiderivative = square.integ()
   result = (
      NP.polyval(antiderivative, right)
      - NP.polyval(antiderivative, left)
   )
   return result
