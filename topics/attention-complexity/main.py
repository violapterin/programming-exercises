#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as Plot
import numpy.random.Generator.uniform as Uniform
import time.time as Time
import datetime.datetime as Datetime

class Network:
   def __init__(self, dot):
      self.depth = dot.depth
      self.width = dot.width
      self.epoch = dot.epoch
      self.input = NP.zeros((self.width, 1))
      self.initialize_weight(dot.weight_top)
      self.initialize_propagation()

   def fit_data(self, many_input, many_observation):
      for time in range(self.epoch):
         assert(len(many_input) == len(many_observation))
         step = self.size_step * (self.decay_step ^ time)
         self.stochastic_gradient_descent(step, many_input, many_observation)

   def stochastic_gradient_descent(self, step, many_input, many_observation):
      size_data = len(many_input)
      increment = [NP.zeros((self.width, self.width))] * (layer - 1)
      for index in range(size_data):
         self.input = many_input[index]
         observation = many_observation[index]
         self.permeate()
         gradient = self.find_gradient()
         for layer in range(self.depth - 1):
            increment[layer] = - (
               step
               * 2 * (self.output - observation)
               * gradient[layer]
            )
      for layer in range(self.depth - 1):
         self.weight[layer] += increment[layer]
      self.propagate()

   def find_gradient(self):
      result = 0
      for layer in range(self.depth - 1):
         active = int([(abs(node) <= 1) for node in self.hidden[layer]])
         result += self.propagation[layer] * active
      return result

   def find_loss(self, many_input, many_observation):
      assert(len(many_input) == len(many_observation))
      size_data = len(many_input)
      loss = 0
      for index in range(size_data):
         self.input = many_input[index]
         self.permeate()
         loss += (self.output - many_observation[index])^2
      return loss

   def permeate(self, input):
      self.input = input
      for layer in range(self.depth - 1):
         hold_hidden = self.weight[layer] * self.hidden[layer]
         self.hidden[layer + 1] = [
            x if abs(x) <= 1
            else int(NP.sign(x))
            for x in hold_hidden
         ]

   def propagate(self):
      self.propagation[self.depth - 1] = self.weight_top 
      for layer in reversed(range(self.depth - 1)):
         self.propagation[layer] = self.propagation[layer + 1] * self.weight[layer]

   def initialize_weight(self, weight_top):
      self.weight = []
      for _ in range(self.depth - 1):
         self.weight.append(NP.eye(self.width) / self.depth)
      self.weight.append(weight_top)

   def initialize_propagation(self):
      self.propagation = []
      for _ in range(self.depth - 1):
         self.propagation.append(NP.zeros((self.width, 1)))
      self.propagate()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def display_array_constant(self, **method):
      dot_depth = 1
      width = 1
      dot_sample = 1
      experiment = 1
      match method["depth"]:
         case "big":
            dot_depth = 24
         case "medium":
            dot_depth = 16
         case "small":
            dot_depth = 8
      self.table =  [[None]*self.dot_sample for _ in range(self.dot_depth)]
      for index_depth in range(self.dot_depth):
         for index_sample in range(self.dot_sample):
            self.table[index_depth][index_sample] = Constant(
               depth = 8 + 2 * index_depth,
               width = width,
               sample = 40 + 5 * index_sample,
               experiment = experiment,
            )

prefix_constant_label

class Constant:
   def __init__(self, depth, width, sample):
      self.depth = depth
      self.width = width
      self.sample = sample
      self.bound_transition = 2
      self.bound_entry = 5
      self.range = 12
      self.candidate_period = [4, 5, 6]
      self.weight_top = NP.array(NP.ones((1, self.width)) / self.width)
      self.epoch = 1024
      self.step_size = 0.1
      self.step_decay = 0.95

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():
   situation = "small"
   match situation:
      case "small":
         point = 4
         array_factor = [1, 3, 5, 7]
         array_depth = [6, 9, 12, 15]
      case "medium":
         point = 6
         array_factor = [1, 3, 5, 7, 9, 11]
         array_depth = [6, 9, 12, 15, 18, 21]
      case _:
         pass
   assert(len(array_factor) == point)
   assert(len(array_depth) == point)

   setting = []
   for method in ["vanilla", "attention"]:
      for index_depth in range(point):
         array_constant = []
         depth = array_depth[index_depth]
         width = 8
         label = (
            "method-" + method
            + "-depth-" + str(depth)
         )
         array_constant.append(label)
         for index_point in range(point):
            sample = array_factor[index_point] * depth ** 2
            constant = Constant(
               depth = depth,
               width = width,
               sample = sample,
            )
            array_constant.append(constant)

   # diimension == error^2 * sample == edge^2
   result = []
   for array_constant in setting:
      label = array_constant[0]
      curve = []
      curve.append(label)
      if label.startwith("attention"):
         for dot in array_constant[1:]:
            loss = 0
            for _ in range(dot.experiment):
               # attention: training
               many_input = []
               many_observation = []
               for _ in range(dot.sample):
                  if (Uniform(0, 2) <= 1):
                     many_observation.append(1)
                     many_input.append(generate_history(dot))
                  else:
                     many_observation.append(0)
                     many_input.append(generate_random(dot))
               many_trained = []
               candidate_focus = (
                  dot.candidate_period + [0]
                  + [- x for x in dot.candidate_period]
               )
               for focus_guess in candidate_focus:
                  many_attentive = add_attention(focus_guess, many_input)
                  trained = fit_data_find_loss(dot, many_attentive, many_observation)
                  many_trained.append(trained)
               focus_chosen = candidate_focus[many_trained.index(min(many_trained))]
               # attention: proper experiments
               many_attentive = add_attention(focus_chosen, many_input)
               loss += (
                  fit_data_find_loss(dot, many_attentive, many_observation)
                  / dot.experiment
               )
            curve.append(loss)
      elif label.startwith("vanilla"):
         for dot in array_constant[1:]:
            loss = 0
            for _ in range(dot.experiment):
               # vanilla: experiments
               many_input = []
               many_observation = []
               for _ in range(dot.sample):
                  if (Uniform(0, 2) <= 1):
                     many_observation.append(1)
                     many_input.append(generate_history(dot))
                  else:
                     many_observation.append(0)
                     many_input.append(generate_random(dot))
               loss += (
                  fit_data_find_loss(dot, many_input, many_observation)
                  / dot.experiment
               )
            curve.append(loss)
      else:
         pass

   for curve in result:
      label = curve[0]
      array_loss = curve[1:]
      Plot.plot(array_depth, array_loss, label = label)
   Plot.xlabel("depth")
   Plot.ylabel("squared loss")
   Plot.title("Attention Mechanism")
   title = ("current/plot" + situation + '.' + "png")
   Plot.legend()
   Plot.savefig(title, dpi = 300)
   Plot.clf()

def fit_data_find_loss(dot, many_input, many_observation):
   network = Network(dot)
   network.fit_data(many_input, many_observation)
   loss = network.give_loss(many_input, many_observation)
   return loss

def generate_history(dot):
   transition = Uniform(- dot.bound_transition, cc.bound_transition, (1, cc.period)) 
   history = NP.zeros((dot.period, 1))
   for _ in dot.width:
      latest = 0
      if (Uniform(0, dot.period) <= 1):
         latest = Uniform(- dot.bound_entry, cc.bound_entry)
      else:
         latest = transition * history[:dot.period, :]
      history.append(latest)
   return history

def generate_random(dot):
   history = Uniform(- dot.bound_entry, cc.bound_entry, (cc.width, 1))
   return history

def add_attention(period, many_input):
   width = len(many_input[0])
   many_attentive = many_input
   if period > 0:
      many_attentive = [
         input
         + NP.array([NP.sin(2 * NP.pi * k / period) for k in range(width)])
         for input in many_input
      ]
   elif period < 0:
      many_attentive = [
         input
         + NP.array([NP.cos(2 * NP.pi * k / period) for k in range(width)])
         for input in many_input
      ]
   return many_attentive

# # # # # # # # # # # # # # # # # # # # # # # #

main()
