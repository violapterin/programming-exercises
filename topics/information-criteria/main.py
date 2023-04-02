#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as PLOT
import numpy.polynomial as PLN
import numpy.random as RANDOM

def main():
   NUMBER_EXPERIMENT = 48
   LEFT = -8
   RIGHT = 8
   NUMBER_SAMPLE = 12
   DEGREE_LOW = 16
   DEGREE_HIGH = 24
   DEGREE_MAXIMUM = 32
   simulate(
      NUMBER_EXPERIMENT,
      LEFT,
      RIGHT,
      NUMBER_SAMPLE,
      DEGREE_LOW,
      DEGREE_HIGH,
      DEGREE_MAXIMUM,
   )

def simulate():
   NUMBER_EXPERIMENT = 48
   LEFT = -8
   RIGHT = 8
   NUMBER_SAMPLE = 12
   DEGREE_LOW = 16
   DEGREE_HIGH = 24
   DEGREE_MAXIMUM = 32
   range_degree = range(DEGREE_LOW, DEGREE_HIGH + 1)
   akaike = []
   bayes = []

   for degree in range_degree:
      total = [0, 0]
      for _ in range(NUMBER_EXPERIMENT):
         total += learn(
            left = LEFT,
            right = RIGHT,
            number_sample = NUMBER_SAMPLE,
            degree_maximum = DEGREE_MAXIMUM,
            degree_correct = degree,
         )
      total /= NUMBER_EXPERIMENT
      akaike.append(total[0])
      bayes.append(total[1])

   PLOT.plot(NP.array(range_correct), NP.array(akaike))
   PLOT.plot(NP.array(range_correct), NP.array(bayes))
   PLOT.xlabel("degree of true polynomial")
   PLOT.ylabel("squared loss")
   PLOT.title("Information Criteria")
   title = (
      "plot"
      + '-' + "degree" + '-' + str(DEGREE_LOW) + '-' + str(DEGREE_HIGH)
      + '-' + "maximum" + '-' + str(DEGREE_MAXIMUM)
      + '-' + "sample" + '-' + str(NUMBER_SAMPLE)
      + '.' + "png"
   )
   PLOT.savefig(title, dpi=300)


def learn(**setup):
   left = setup[left]
   right = setup[right]
   number_sample = setup[number_sample]
   degree_maximum = setup[degree_maximum]
   degree_correct = setup[degree_correct]

   root = RANDOM.default_rng().uniform(degree_correct, left, right)
   sample = RANDOM.default_rng().uniform(number_sample, left, right)
   correct = PLN.polyfromroots(root)
   record_loss = zeros(degree_maximum)
   record_akaike = zeros(degree_maximum)
   record_bayes = zeros(degree_maximum)

   for degree in range(1, degree_maximum + 1):
      evaluation = NP.polyval(correct, sample)
      noise = RANDOM.default_rng().standard_normal(number_sample)
      observation = evaluation + noise
      estimator = NP.polyfit(sample, observation, degree)
      loss = find_loss(left, right, correct, estimator)
      likelihood = find_likelihood(correct, estimator)
      akaike = - 2 * likelihood + 2 * degree
      bayes = - 2 * likelihood + NP.log(number_sample) * degree
      record_loss[degree] = loss
      record_akaike[degree] = akaike
      record_bayes[degree] = bayes

   loss_akaike = loss[numpy.argmin(record_akaike)]
   loss_bayes = loss[numpy.argmin(record_bayes)]
   return [loss_akaike, loss_bayes]

def find_likelihood():
   difference = NP.polysub(polynomial_one, polynomial_two)
   result = 0
   result += - (1/2) * NP.log(2 * NP.pi) * difference.size
   result += np.sum(- (difference * difference) / 2)
   return result

def find_loss(left, right, polynomial_one, polynomial_two):
   difference = NP.polysub(polynomial_one, polynomial_two)
   square = difference.polypow()
   antiderivative = square.integ()
   result = 0
   result = NP.polyval(antiderivative, right)
   result =  NP.polyval(antiderivative, left)
   return result

