#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as PLOT
import numpy.polynomial.polynomial as PLN
import numpy.random as RANDOM
from time import time as TIME
from datetime import datetime as DATETIME

class Network:
   def __init__(self, constant):
      self.depth = constant.depth
      self.width = constant.width
      self.epoch = constant.epoch
      self.tolerance = constant.tolerance
      self.input = NP.zeros(self.width)
      self.initialize_weight()
      self.initialize_propagation(weight_top)

   def stochastic_gradient_descent(self, many_input, many_observation):
      assert(len(many_input) == len(many_observation))
      size_data = len(many_input)
      step_weight = [NP.zeros((self.width, self.width))] * layer
      increment = 0
      for _ in self.number_exploration:
         hold_step_weight = [NP.zeros((self.width, self.width))] * layer
         hold_increment = 0
         for index in range(size_data):
            self.input = many_input[index]
            observation = many_observation[index]
            self.permeate()
            for layer in range(self.depth - 1):
               hold_step_weight[layer] = NP.normal((self.width, self.width))
            change = self.find_gradient(hold_step_weight)
            hold_increment += 2 * (self.output - observation) * change
         if (increment < hold_increment):
            step_weight = hold_step_weight
            increment = hold_increment
      for layer in range(self.depth - 1):
         self.weight[layer] += step_weight[layer]
      self.propagate()

   def find_gradient(self, step_weight):
      change = 0
      for layer in range(self.depth - 1):
         active = int([(abs(node) <= 1) for node in self.hidden[layer]])
         change += self.propagation[layer] * step_weight[layer] * active
      result = self.propagation[layer - 1] * change[self.depth - 1]
      return result

   def find_loss(self, many_input, many_observation):
      assert(len(many_input) == len(many_observation))
      size_data = len(many_input)
      loss = 0
      for index in range(size_data):
         self.input = many_input[index]
         self.permeate()
         self.propagate()
         loss += (self.output - many_observation[index])^2
      return loss

   def permeate(self, input):
      self.input = input
      for layer in range(self.depth - 1):
         self.hidden[layer + 1] = self.weight[layer] * self.hidden[layer]
         self.hidden[layer + 1] = [
            x if abs(x) <= 1 else int(NP.sign(x)) for x in self.hidden[layer + 1]
         ]

   def propagate(self):
      for layer in reversed(range(self.depth - 1)):
         self.propagation[layer] = self.propagation[layer + 1] * self.weight[layer]

   def initialize_weight(self):
      self.weight = []
      for _ in range(self.depth - 1):
         self.weight.append(NP.ones(self.width) / self.depth)

   def initialize_propagation(self, weight_top):
      self.propagation = []
      for _ in range(self.depth - 1):
         self.propagation.append(NP.zeros(self.width))
      self.propagation[self.depth - 1] = weight_top
      self.propagate()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Constant:
   def __init__(self, constant):
      self.transition_low = constant.transition_low
      self.transition_high = constant.transition_high
      self.range = constant.range

   def candidate_period(self):
      [2, 3, 4, 5, 6]

def generate_random(constant):
   bound_entry = constant.bound_entry
   width = constant.width
   history = NP.random.uniform(- bound_entry, bound_entry, width)
   return history

def generate_history(constant):
   transition_low = constant.transition_low
   transition_high = constant.transition_high
   period = constant.period
   bound_entry = constant.bound_entry
   width = constant.width
   transition = NP.random.uniform(transition_low, transition_high, period) 
   history = NP.zeros(period)
   for _ in width:
      latest = 0
      if (NP.random.uniform(0, period) <= 1):
         latest = NP.random.uniform(- bound_entry, bound_entry)
      else:
         latest = history[:period] * transition
      history.append(latest)
   return history

def fit_data(constant, period, many_input, many_observation):
   network = Network(constant)
   for _ in constant.epoch:
      network.stochastic_gradient_descent(many_input, many_observation)
   loss = network.find_loss(many_input, many_observation)
   return loss

def add_attention(many_input, period):
   if (period == 0):
      return many_input
   attentive = many_input
   # XXX

def main():
   constant = Constant("small-six")
   experiment_attention_loss = []
   experiment_vanilla_loss = []
   for _ in range(constant.number_experiment):
      many_input = []
      many_observation = []
      for _ in range(constant.number_sample):
         if (NP.random.uniform(0, 2) <= 1):
            many_observation.append(1)
            many_input.append(generate_history(constant))
         else:
            many_observation.append(0)
            many_input.append(generate_random(constant))
      many_loss = []
      for period_blind in constant.candidate_period:
         many_attentive_blind = add_attention(many_input, period_blind)
         loss = fit_data(constant, period_blind, many_attentive_blind, many_observation)
         many_loss.append(loss)
      period_chosen = constant.candidate_period[many_loss.index(min(many_loss))]
      many_attentive_chosen = add_attention(many_input, period_chosen)
      actual_loss = fit_data(constant, many_attentive_chosen, many_observation)
      experiment_attention_loss += actual_loss / constant.number_experiment
   for _ in range(constant.number_experiment):
      many_input = []
      many_observation = []
      for _ in range(constant.number_sample):
         if (NP.random.uniform(0, 2) <= 1):
            many_observation.append(1)
            many_input.append(generate_history(constant))
         else:
            many_observation.append(0)
            many_input.append(generate_random(constant))
      many_attentive = add_attention(many_input, period_chosen)
      actual_loss = fit_data(constant, many_attentive, many_observation)
      experiment_vanilla_loss += actual_loss / constant.number_experiment

   range_depth = constant.range_depth
   PLOT.plot(range_depth, experiment_vanilla_loss, label = "vanilla")
   PLOT.plot(range_depth, experiment_attention_loss, label = "attention")
   PLOT.xlabel("depth")
   PLOT.ylabel("squared loss")
   PLOT.title("Attention Mechanism")
   title = (
      "current/plot"
      + '-' + "times" + '-' + str(constant.number_experiment).zfill(2)
      + '-' + "sample" + '-' + str(constant.number_sample).zfill(2)
      + '-' + str(degree_model_high).zfill(2)
      + '.' + "png"
   )
   PLOT.legend()
   PLOT.savefig(title, dpi=300)
   PLOT.clf()


# # # # # # # # # # # # # # # # # # # # # # # #

main()

'''
def main():
   left = -1
   right = 1
   number_experiment = 384
   degree_correct_low = 24
   degree_correct_high = 32
   choice_degree_model = [[12, 40], [8, 48]]
   choice_number_sample = [240, 320]

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
'''
