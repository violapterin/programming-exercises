#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as Plot
import datetime

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
         observation = many_observation[index]
         self.permeate()
         for layer in range(self.depth - 1):
            increment[layer] = - (
               step * 2 * (self.output - observation)
               * self.find_gradient(layer)
            )
      for layer in range(self.depth - 1):
         self.weight[layer] += increment[layer]
      self.propagate()

   def find_gradient(self, layer):
      result = [
         self.propagation[layer].flatten().tolist()
         if abs(node) <= 1
         else NP.zeros(self.width).tolist()
         for node in self.hidden[layer]
      ]
      result = NP.transpose(NP.array(result))
      #print("gradient max entry:", NP.max(NP.abs(result)))
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

   def permeate(self):
      self.hidden[0] = self.input
      for layer in range(self.depth - 1):
         #print("weight", self.weight[layer])
         #print("hidden", self.hidden[layer])
         hold_hidden = self.weight[layer] @ self.hidden[layer]
         hold_hidden = [
            float(node) if abs(node) <= 1
            else 0 if check_abnormal(float(node))
            else float(NP.sign(node))
            for node in hold_hidden
         ]
         self.hidden[layer + 1] = NP.array(hold_hidden).reshape(-1, 1)

   def propagate(self):
      self.propagation[self.depth - 1] = self.weight[self.depth - 1].reshape(1, -1)
      for layer in reversed(range(self.depth - 1)):
         self.propagation[layer] = self.propagation[layer + 1] @ self.weight[layer]

   def initialize_weight(self, weight_top):
      self.weight = []
      for _ in range(self.depth - 1):
         #self.weight.append(NP.eye(self.width))
         self.weight.append(draw_uniform_vector(-1, 1, (self.width, self.width)))
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
      self.candidate_period = [4, 6]
      self.bound_transition = 2
      self.bound_entry = 5
      self.range = 12
      self.epoch = 16
      self.size_step = 0.1
      self.decay_step = 0.95
      self.weight_top = draw_uniform_vector(-1, 1, (1, self.width))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(situation):
   array_sample = []
   array_depth = []
   width = 1
   experiment = 1
   if ("small" in situation):
      array_sample = [3 * item for item in range(3, 6)]
      array_depth = [4, 6]
      width = 4
   elif ("medium" in situation):
      array_sample = [4 * item for item in range(4, 8)]
      array_depth = [6, 9, 12]
      width = 6
   elif ("large" in situation):
      array_sample = [6 * item for item in range(5, 10)]
      array_depth = [8, 10, 12, 14]
      width = 8
   else:
      return
   if ("test" in situation):
      experiment = 6
   elif ("normal" in situation):
      experiment = 32
   elif ("final" in situation):
      experiment = 60
   else:
      return
   array_period = [4, 6]

   setting = []
   for method in ["vanilla", "attention"]:
      for depth in array_depth:
         for period in array_period:
            array_constant = []
            label = (
               method
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
      print(
         "* * * * * *",
         datetime.datetime.now().strftime("%H"), ":",
         datetime.datetime.now().strftime("%M"), ":",
         label
      )
      curve = []
      curve.append(label)
      if "attention" in label:
         for dot in array_constant[1:]:
            loss = 0
            for _ in range(experiment):
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
               loss_increment = (
                  fit_data_find_loss(dot, many_attentive, many_observation)
                  / experiment
               )
               if check_abnormal(loss_increment): pass
               loss += loss_increment
            curve.append((
                  NP.log(((dot.depth ** 2 ) * (dot.width ** 4)) / dot.sample),
                  NP.log(loss ** 2)
            ))
      elif "vanilla" in label:
         for dot in array_constant[1:]:
            loss = 0
            for _ in range(experiment):
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
               loss_increment = (
                  fit_data_find_loss(dot, many_input, many_observation)
                  / experiment
               )
               if check_abnormal(loss_increment): pass
               loss += loss_increment
            curve.append((
                  NP.log(((dot.depth ** 2 ) * (dot.width ** 4)) / dot.sample),
                  NP.log(loss ** 2)
            ))
      else:
         pass
      result.append(curve)

   count_line = 0
   count_marker = 0
   many_line = ['-', '--', '-.', ':']
   many_marker = ['o', 's', 'D', 'P', '^', 'v']
   for curve in result:
      many_pair = curve[1:]
      array_first = [pair[0] for pair in many_pair]
      array_second = [pair[1] for pair in many_pair]
      print("array_first", array_first)
      print("array_second", array_second)
      Plot.plot(
         array_first,
         array_second,
         label = curve[0],
         linestyle = many_line[count_line],
         marker = many_marker[count_marker],
      )
      count_line = (count_line + 1) % len(many_line)
      count_marker = (count_marker + 1) % len(many_marker)

   Plot.xlabel("edge squared over sample (log)")
   Plot.ylabel("squared loss squared (log)")
   Plot.title("Attention Mechanism")
   title = ("current/plot-" + situation + '.' + "png")
   Plot.legend(
      loc = "center left",
      bbox_to_anchor = (0.0, 1.23),
      ncol = 3,
      fontsize = "x-small",
   )
   Plot.subplots_adjust(top = 0.75)
   Plot.savefig(title, dpi = 600)
   Plot.clf()

def fit_data_find_loss(dot, many_input, many_observation):
   network = Network(dot)
   network.fit_data(dot, many_input, many_observation)
   loss = network.find_loss(many_input, many_observation)
   return loss

def add_attention(period, many_input):
   width = len(many_input[0])
   many_attentive = many_input
   if period > 0:
      sinusoidal = [NP.sin(2 * NP.pi * k / period) for k in range(width)]
      many_attentive = [
         NP.array(input.reshape(1, -1) + NP.array(sinusoidal)).reshape(-1, 1)
         for input in many_input
      ]
   elif period < 0:
      sinusoidal = [NP.cos(2 * NP.pi * k / period) for k in range(width)]
      many_attentive = [
         NP.array(input.reshape(1, -1) + NP.array(sinusoidal)).reshape(-1, 1)
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

def check_abnormal(value):
   if NP.isnan(value): return False
   if NP.isinf(value): return False
   if not (value < 2 ** 16): return False
   if not (value > - 2 ** 16): return False


# # # # # # # # # # # # # # # # # # # # # # # #

#main("test-small")
#main("test-medium")
#main("test-large")
#main("normal-small")
main("normal-medium")
main("normal-large")
