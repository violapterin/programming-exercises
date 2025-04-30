#! /usr/bin/env python3

#import os
#import control as ct
import numpy as np
from scipy.integrate import solve_ivp as Solve
import matplotlib.pyplot as Plot



def main():
   test()
   #draw()
   '''
      many_catalog = generate_parameter()
      for catalog in many_catalog:
         print("Case:")
         print(catalog["title"])
         draw(catalog)
   '''

def test():
   print(beta(5)(2))

def beta(c):
   def alpha(x):
      return c * x ** 3
   return alpha

def update(tt, yy):
   mu = 0.01
   nu = 0
   gamma = 1
   xx = yy[0:3]
   ss = yy[3:6]
   uu = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2)
   ])
   pp = gamma * ss + gamma * nu * uu
   d_xx = update_hybrid(xx, pp)
   d_ss = uu - mu * ss
   result = np.concatenate((d_xx, d_ss))
   return result

def update_smith(xx, pp):
   vv = np.zeros(3)
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * max(pp[j] - pp[i], 0) # T[j, i]
            - xx[i] * max(pp[i] - pp[j], 0) # T[i, j]
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
               2 * max(pp[i] - pp[j], 0)
               + max(pp[i] - pp[j], 0) ** 2
               + 4 * max(pp[i] - pp_hat, 0) ** 3
               + np.exp(pp[i] - pp_hat) - 1
            ) # T[j, i]
            - xx[i] * (
               2 * max(pp[j] - pp[i], 0)
               + max(pp[j] - pp[i], 0) ** 2
               + 4 * max(pp[j] - pp_hat, 0) ** 3
               + np.exp(pp[j] - pp_hat) - 1
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

def draw():
   array_tt = np.linspace(0, 10, 100)
   yy_initial = np.array([
      1/3, 2/3, 0,
      0, 0, 0,
   ])
   print("initial: ", project_to_simplex(yy_initial[0:3]))
   answer = Solve(
      fun = update,
      t_span = [0, 10],
      y0 = yy_initial,
      t_eval = array_tt,
      method = 'Radau',
   )
   #print("y = ", answer.y.transpose())
   print("t = ", answer.t)
   trajectory = np.array([
      project_to_simplex(row[0:3])
      for row in answer.y.transpose()
   ])
   print("trajectory: ", trajectory)
   Plot.plot(
      trajectory.transpose()[0],
      trajectory.transpose()[1],
      marker = "D",
   )
   Plot.xlabel("along x_2 + x_1 == 0")
   Plot.ylabel("along - x_1 - x_2 + x_3 == 0")
   Plot.title("trajectory")
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
      "test.png",
      format = "png"
   )
   Plot.clf()

def project_to_simplex(xx):
   unit_aa = np.array([-1, 1, 0])
   unit_bb = np.array([-1/2, -1/2, 1])
   unit_aa = unit_aa / np.linalg.norm(unit_aa)
   unit_bb = unit_bb / np.linalg.norm(unit_bb)
   result = np.array([
      unit_aa.T @ (xx - np.array([1/2, 1/2, 0])),
      unit_bb.T @ (xx - np.array([1/2, 1/2, 0])),
   ])
   return result



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
