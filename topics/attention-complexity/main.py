#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as Plot
# import time.time as Time
# import datetime.datetime as Datetime

class Network:
   def __init__(self, dot):
      self.depth = dot.depth
      self.width = dot.width
      self.epoch = dot.epoch
      self.input = NP.zeros((self.width, 1))
      self.output = 0
      self.initialize_hidden()
      self.initialize_weight(dot.weight_top)
      self.initialize_propagation()

   def fit_data(self, dot, many_input, many_observation):
      for time in range(dot.epoch):
         assert(len(many_input) == len(many_observation))
         step = dot.size_step * (dot.decay_step ** time)
         self.stochastic_gradient_descent(step, many_input, many_observation)

   def stochastic_gradient_descent(self, step, many_input, many_observation):
      size_data = len(many_input)
      increment = [NP.zeros((self.width, self.width))] * (self.depth - 1)
      for index in range(size_data):
         self.input = many_input[index]
         #print("input", many_input[index])
         observation = many_observation[index]
         self.permeate()
         gradient = self.find_gradient()
         for layer in range(self.depth - 1):
            increment[layer] = - (
               step * 2 * (self.output - observation)
               * gradient[layer]
            )
      for layer in range(self.depth - 1):
         self.weight[layer] += increment[layer]
      self.propagate()

   def find_gradient(self):
      result = 0
      for layer in range(self.depth - 1):
         active = [int(abs(node) <= 1) for node in self.hidden[layer]]
         active = NP.array(active)
         result += self.propagation[layer] @ active
      return result

   def find_loss(self, dot, many_input, many_observation):
      assert(len(many_input) == len(many_observation))
      size_data = len(many_input)
      loss = 0
      for index in range(size_data):
         self.input = many_input[index]
         self.permeate()
         loss += (self.output - many_observation[index])^2
      return loss

   def permeate(self):
      self.hidden[0] = self.input
      for layer in range(self.depth - 1):
         print("layer:", layer)
         #print("weight:", self.weight[layer].shape)
         #print("hidden:", self.hidden[layer].shape)
         hold_hidden = self.weight[layer] @ self.hidden[layer]
         hold_hidden = [
            int(node) if abs(node) <= 1
            else int(NP.sign(node))
            for node in hold_hidden
         ]
         self.hidden[layer + 1] = NP.array(hold_hidden)

   def propagate(self):
      self.propagation[self.depth - 1] = self.weight[self.depth - 1]
      for layer in reversed(range(self.depth - 1)):
         self.propagation[layer] = self.propagation[layer + 1] @ self.weight[layer]

   def initialize_weight(self, weight_top):
      self.weight = []
      for _ in range(self.depth - 1):
         self.weight.append(NP.eye(self.width))
      self.weight.append(weight_top)

   def initialize_propagation(self):
      self.propagation = []
      for _ in range(self.depth):
         self.propagation.append(NP.zeros((self.width, 1)))
      self.propagate()

   def initialize_hidden(self):
      self.hidden = []
      for _ in range(self.depth):
         self.hidden.append(NP.zeros((self.width, 1)))

class Constant:
   def __init__(self, depth, width, sample, period):
      self.depth = depth
      self.width = width
      self.sample = sample
      self.period = period
      self.bound_transition = 2
      self.bound_entry = 5
      self.range = 12
      self.candidate_period = [4, 5, 6]
      self.weight_top = NP.array(NP.ones((1, self.width)) / self.width)
      self.experiment = 36
      self.epoch = 128
      self.size_step = 0.1
      self.decay_step = 0.95

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():
   situation = "small"
   array_sample = []
   array_depth = []
   width = 1
   if (situation == "small"):
      array_sample = [3, 4, 5] * 6
      array_depth = [9, 12]
      width = 24
   elif (situation == "medium"):
      array_sample = [4, 5, 6, 7] * 12
      array_depth = [6, 12, 18]
      width = 36
   elif (situation == "large"):
      array_sample = [5, 6, 7, 8, 9, 10] * 18
      array_depth = [4, 8, 12, 16, 20, 24]
      width = 48
   else:
      pass
   array_period = [2, 3, 6]

   setting = []
   for method in ["vanilla", "attention"]:
      for depth in array_depth:
         for period in array_period:
            array_constant = []
            label = (
               "method-" + method
               + "-depth-" + str(depth)
               + "-period-" + str(period)
            )
            array_constant.append(label)
            for sample in array_sample:
               constant = Constant(
                  depth = depth,
                  width = width,
                  sample = sample,
                  period = period,
               )
               array_constant.append(constant)
            setting.append(array_constant)

   # diimension ~ error^2 * sample ~ edge^2
   # error^2 ~ edge^2 / sample
   result = []
   for array_constant in setting:
      label = array_constant[0]
      #print("label:", label)
      curve = []
      curve.append(label)
      if "attention" in label:
         for dot in array_constant[1:]:
            loss = 0
            for _ in range(dot.experiment):
               # attention: training
               many_input = []
               many_observation = []
               for _ in range(dot.sample):
                  if (draw_uniform(0, 2) <= 1):
                     many_input.append(generate_history(dot))
                     many_observation.append(1)
                  else:
                     many_input.append(generate_random(dot))
                     many_observation.append(0)
               print("many_input", many_input)
               many_trained = []
               candidate_focus = (
                  dot.candidate_period + [0]
                  + [-period for period in dot.candidate_period]
               )
               for focus in candidate_focus:
                  many_attempt = add_attention(focus, many_input)
                  trained = fit_data_find_loss(dot, many_attempt, many_observation)
                  many_trained.append(trained)
               focus_chosen = candidate_focus[many_trained.index(min(many_trained))]
               # attention: proper experiments
               many_attentive = add_attention(focus_chosen, many_input)
               loss += (
                  fit_data_find_loss(dot, many_attentive, many_observation)
                  / dot.experiment
               )
            curve.append(((dot.depth ** 2) / sample, loss ** 2))
      elif "vanilla" in label:
         for dot in array_constant[1:]:
            loss = 0
            for _ in range(dot.experiment):
               # vanilla: experiments
               many_input = []
               many_observation = []
               for _ in range(dot.sample):
                  if (draw_uniform(0, 2) <= 1):
                     many_input.append(generate_history(dot))
                     many_observation.append(1)
                  else:
                     many_input.append(generate_random(dot))
                     many_observation.append(0)
               #print("many_input", many_input)
               loss += (
                  fit_data_find_loss(dot, many_input, many_observation)
                  / dot.experiment
               )
            curve.append(((dot.depth ** 2) / sample, loss ** 2))
      else:
         pass
      result.append(curve)

   for curve in result:
      many_pair = curve[1:]
      array_first = [pair[0] for pair in many_pair]
      array_second = [pair[1] for pair in many_pair]
      #print("array_first", array_first)
      #print("array_second", array_second)
      Plot.plot(array_first, array_second, label = curve[0])
   Plot.xlabel("edge squared over sample")
   Plot.ylabel("squared loss squared")
   Plot.title("Attention Mechanism")
   title = ("current/plot-" + situation + '.' + "png")
   Plot.legend(loc = "upper left")
   Plot.savefig(title, dpi = 300)
   Plot.clf()

def fit_data_find_loss(dot, many_input, many_observation):
   network = Network(dot)
   network.fit_data(dot, many_input, many_observation)
   loss = network.find_loss(dot, many_input, many_observation)
   return loss

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
   else:
      pass
   return NP.array(many_attentive)

def generate_history(dot):
   transition = draw_uniform_vector(
      -dot.bound_transition, dot.bound_transition, (1, dot.period)
   ) 
   history = draw_uniform_vector(
      - dot.bound_entry, dot.bound_entry, (dot.period, 1)
   )
   for _ in range(dot.width):
      latest = 0
      if (draw_uniform(0, dot.period) <= 1):
         latest = draw_uniform(-dot.bound_entry, dot.bound_entry)
      else:
         latest = transition @ history[-dot.period:, :]
      history = history.reshape(1, -1)
      history = NP.append(history, latest)
      history = history.reshape(-1, 1)
   #print("history", history)
   return NP.array(history[-dot.width:, :])

def generate_random(dot):
   history = draw_uniform_vector(
      - dot.bound_entry, dot.bound_entry, (dot.width, 1)
   )
   return NP.array(history)

def draw_uniform_vector(low, high, dimension):
   generator = NP.random.default_rng()
   return NP.array(generator.uniform(low, high, dimension))

def draw_uniform(low, high):
   generator = NP.random.default_rng()
   return NP.array(generator.uniform(low, high))

# # # # # # # # # # # # # # # # # # # # # # # #

main()
