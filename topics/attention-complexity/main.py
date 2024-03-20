#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as Plot
import numpy.random.Generator.uniform as Uniform
import time.time as Time
import datetime.datetime as Datetime

class Network:
   def __init__(self, cc):
      self.depth = cc.depth
      self.width = cc.width
      self.epoch = cc.epoch
      self.input = NP.zeros((self.width, 1))
      self.initialize_weight(cc.weight_top)
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

def display_many_constant(self, **situation):
      dot_depth = 1
      width = 1
      dot_sample = 1
      experiment = 1
      match situation["depth"]:
         case "big":
            dot_depth = 24
         case "medium":
            dot_depth = 16
         case "small":
            dot_depth = 8
      match situation["width"]:
         case "big":
            width = 36
         case "medium":
            width = 24
         case "small":
            width = 12
      match situation["sample"]:
         case "big":
            dot_sample = 120
         case "medium":
            dot_sample = 80
         case "small":
            dot_sample = 40
      match situation["experiment"]:
         case "big":
            experiment = 24
         case "medium":
            experiment = 16
         case "small":
            experiment = 8
      self.table =  [[None]*self.dot_sample for _ in range(self.dot_depth)]
      for index_depth in range(self.dot_depth):
         for index_sample in range(self.dot_sample):
            self.table[index_depth][index_sample] = Constant(
               depth = 8 + 2 * index_depth,
               width = width,
               sample = 40 + 5 * index_sample,
               experiment = experiment,
            )

class Constant:
   def __init__(self, depth, width, sample, experiment):
      self.depth = depth
      self.width = width
      self.sample = sample
      self.experiment = experiment
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
   many_constant = display_many_constant(
      depth = "small",
      width = "small",
      sample = "small",
      experiment = "small",
   )
   cc = Constant("small-six")
   experiment_attention_loss = []
   experiment_vanilla_loss = []
   collection = []
   for cc in display_many_constant:
      loss_attention = 0
      loss_vanilla = 0
      for _ in range(cc.experiment):
         # attention: training
         many_input = []
         many_observation = []
         for _ in range(cc.sample):
            if (Uniform(0, 2) <= 1):
               many_observation.append(1)
               many_input.append(generate_history(cc))
            else:
               many_observation.append(0)
               many_input.append(generate_random(cc))
         many_loss = []
         candidate_focus = cc.candidate_period + [0] + [- x for x in cc.candidate_period]
         for focus_guess in candidate_focus:
            many_attentive = add_attention(focus_guess, many_input)
            loss = fit_data_find_loss(cc, focus_guess, many_attentive, many_observation)
            many_loss.append(loss)
         focus_chosen = candidate_focus[many_loss.index(min(many_loss))]
         # attention: proper experiments
         many_attentive = add_attention(focus_chosen, many_input)
         loss_attention += (
            fit_data_find_loss(cc, many_attentive, many_observation)
            / cc.experiment
         )
         # vanilla: experiments
         many_input = []
         many_observation = []
         for _ in range(cc.sample):
            if (Uniform(0, 2) <= 1):
               many_observation.append(1)
               many_input.append(generate_history(cc))
            else:
               many_observation.append(0)
               many_input.append(generate_random(cc))
         loss_vanilla += (
            fit_data_find_loss(cc, many_input, many_observation)
            / cc.experiment
         )
      collection.append((cc.depth, cc.sample, loss_attention, loss_vanilla))

   histogram(collection, 0)
   Plot.plot(range_depth, experiment_vanilla_loss, label = "vanilla")
   Plot.plot(range_depth, experiment_attention_loss, label = "attention")
   Plot.xlabel("depth")
   Plot.ylabel("squared loss")
   Plot.title("Attention Mechanism")
   title = (
      "current/plot"
      + '-' + "experiment" + '-' + str(cc.experiment).zfill(2)
      + '-' + "sample" + '-' + str(cc.sample).zfill(2)
      + '.' + "png"
   )
   Plot.legend()
   Plot.savefig(title, dpi=300)
   Plot.clf()

def histogram(collection, argument):
   for item in collection:
      # XXX

def fit_data_find_loss(cc, many_input, many_observation):
   network = Network(cc)
   network.fit_data(many_input, many_observation)
   loss = network.give_loss(many_input, many_observation)
   return loss

def generate_history(cc):
   transition = Uniform(- cc.bound_transition, cc.bound_transition, (1, cc.period)) 
   history = NP.zeros((cc.period, 1))
   for _ in cc.width:
      latest = 0
      if (Uniform(0, cc.period) <= 1):
         latest = Uniform(- cc.bound_entry, cc.bound_entry)
      else:
         latest = transition * history[:cc.period, :]
      history.append(latest)
   return history

def generate_random(cc):
   history = Uniform(- cc.bound_entry, cc.bound_entry, (cc.width, 1))
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
