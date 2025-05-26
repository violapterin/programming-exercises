#! /usr/bin/env python3

#import time
#import copy
import sys
import os
import numpy as np
from scipy.integrate import solve_ivp as Solve
import matplotlib.pyplot as Plot

from custom import custom


def main():
   mode = sys.argv[1] # not used for now
   os.system("rm -rf ./{}".format("plot"))
   os.system("mkdir {}".format("plot"))
   all_catalog = custom.find_catalog()
   for many_many_catalog in all_catalog:
      many_many_catalog.pop(0)
      for many_catalog in many_many_catalog:
         many_catalog.pop(0)
         for catalog in many_catalog:
            catalog.pop(0)
            for parameter in catalog:
               print(
                  "Case {} of {}: {}".format(
                     parameter["count"],
                     parameter["total"],
                     custom.get_name_graphics(parameter),
                  )
               )
               draw(parameter)

def payoff(xx):
   uu = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2)
   ])
   return uu

def give_update_from_parameter(parameter):
   def update(tt, yy):
      mu = parameter["mu"]
      nu = parameter["nu"]
      gamma = parameter["gamma"]
      alpha = parameter["alpha"]
      xx = yy[0:3]
      ss = yy[3:6]
      uu = payoff(xx)
      pp = gamma * ss + gamma * nu * uu
      d_xx = np.zeros(3)
      aa = np.zeros(3)
      bb = np.zeros(3)
      if (parameter["rule"] == "smith"):
         aa = update_smith(xx, pp)
      elif (parameter["rule"] == "brown"):
         aa = update_brown(xx, pp)
      elif (parameter["rule"] == "hybrid"):
         aa = update_hybrid(xx, pp)
      bb = update_best(xx, pp)
      d_xx = alpha * aa + (1 - alpha) * bb
      d_ss = uu - mu * ss
      result = np.concatenate((d_xx, d_ss))
      return result
   return update

def draw(parameter):
   cc = custom.give_constant()
   horizon = cc["horizon"]
   step = cc["step"]
   array_tt = np.linspace(0, int(horizon), int(horizon/step))
   yy_initial = np.concatenate(
      (parameter["start"], np.array([0, 0, 0]))
   )
   #print("initial: ", project_to_simplex(yy_initial[0:3]))
   update = give_update_from_parameter(parameter)
   answer = Solve(
      fun = update,
      t_span = [0, horizon],
      y0 = yy_initial,
      t_eval = array_tt,
      method = cc["method_solve"],
   )
   #print("t = ", answer.t)
   trajectory = np.array([
      custom.project_to_simplex(row[0:3])
      for row in answer.y.transpose()
   ])
   #print("trajectory: ", trajectory)
   Plot.plot(
      trajectory.transpose()[0],
      trajectory.transpose()[1],
      marker = "D",
      markersize = 2.1,
      linewidth = 0.7,
      color = "blue",
   )
   Plot.plot(
      [-np.sqrt(1/2), 0, np.sqrt(1/2)],
      [0, np.sqrt(3/2), 0],
      marker = ".",
      color = "cyan",
   )
   Plot.xlabel("along (-1, 1, 0)")
   Plot.ylabel("along (-1/2, -1/2, 1)")
   Plot.title("trajectory")
   Plot.axis("equal")
   Plot.subplots_adjust(top = 0.75)
   '''
   Plot.legend(
      loc = "center left",
      bbox_to_anchor = (0.0, 1.14),
      ncol = 3,
      fontsize = "x-small",
   )
   '''
   Plot.savefig(
      custom.get_name_graphics(parameter),
      dpi = cc["resolution_image"],
      format = "png",
   )
   Plot.clf()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def update_smith(xx, pp):
   vv = np.zeros(3)
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * max(pp[i] - pp[j], 0) # T[j, i]
            - xx[i] * max(pp[j] - pp[i], 0) # T[i, j]
         )
   return np.array(vv)

def update_brown(xx, pp):
   vv = np.zeros(3)
   pp_hat = pp.T @ xx
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * max(pp[i] - pp_hat, 0) # T[j, i]
            - xx[i] * max(pp[j] - pp_hat, 0) # T[i, j]
         )
   return vv

def update_hybrid(xx, pp):
   vv = np.zeros(3)
   pp_hat = pp.T @ xx
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * (
               0.2 * max(pp[i] - pp[j], 0)
               + 0.1 * max(pp[i] - pp[j], 0) ** 2
               + 0.4 * max(pp[i] - pp_hat, 0) ** 3
            ) # T[j, i]
            - xx[i] * (
               0.2 * max(pp[j] - pp[i], 0)
               + 0.1 * max(pp[j] - pp[i], 0) ** 2
               + 0.4 * max(pp[j] - pp_hat, 0) ** 3
            ) # T[i, j]
         )
   return vv

def update_best(xx, pp):
   yy = np.array(pp, copy = True)
   pp_max = max(pp)
   number_nonzero = len(pp)
   for index in range(len(pp)):
      if (yy[index] < pp_max - 1e-9):
         yy[index] = 0
         number_nonzero -= 1
      else:
         yy[index] = 1
   yy = yy / number_nonzero
   vv = yy - xx
   return vv

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
