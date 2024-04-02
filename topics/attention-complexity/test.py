#!/usr/bin/env python3

import numpy as NP
import matplotlib.pyplot as Plot

def draw_uniform_vector(low, high, dimension):
   generator = NP.random.default_rng()
   return generator.uniform(low, high, dimension)

def draw_uniform(low, high):
   generator = NP.random.default_rng()
   return generator.uniform(low, high)

def main():
   array_first = (
      NP.array(range(20))
      + NP.array(draw_uniform_vector(0, 1, (1, 20)))
   ).flatten().tolist()
   array_second = (
      NP.array(list(range(20)))
      + NP.array(draw_uniform_vector(0, 1, (1, 20)))
   ).flatten().tolist()

   Plot.plot(array_first, array_second, label = "test")
   Plot.xlabel("edge squared over sample")
   Plot.ylabel("squared loss squared")
   Plot.title("Attention Mechanism")
   title = ("current/plot-test.png")
   Plot.legend()
   Plot.savefig(title, dpi = 300)
   Plot.clf()

# # # # # # # # # # # # # # # # # # # # # # # #

main()

'''
for _ in range(6):
   print(draw_uniform_vector(1, 5, (2, 3)))
'''