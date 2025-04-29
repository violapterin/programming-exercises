#! /usr/bin/env python3

#import os
#import control as ct
import numpy as np
from scipy.integrate import solve_ivp as Solve
import matplotlib.pyplot as Plot



def main():
   #test()
   draw()
   '''
      many_catalog = generate_parameter()
      for catalog in many_catalog:
         print("Case:")
         print(catalog["title"])
         draw(catalog)
   '''

def update(tt, yy):
   mu = 1
   nu = 1
   gamma = 1
   xx = yy[0:3]
   qq = yy[3:6]
   ss = yy[6:9]
   '''
   uu = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2)
   ])
   '''
   uu = np.array([
      - (xx[0] + (xx[0] + xx[2]) ** 2),
      - (xx[1] + (xx[1] + xx[2]) ** 2),
      - (xx[2] + (xx[0] + xx[2]) ** 2),
   ])
   pp = gamma * ss + gamma * nu * uu
   d_xx = vv_smith(xx, pp)
   d_qq = np.zeros(3)
   d_ss = uu - mu * ss
   result = np.concatenate((d_xx, d_qq, d_ss))
   return result

def vv_smith(xx, pp):
   vv = np.zeros(3)
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * max(pp[j] - pp[i], 0) # T[j, i]
            + xx[i] * max(pp[i] - pp[j], 0) # T[i, j]
         )
   return np.array(vv)

'''
def update(tt, yy):
   xx = yy[0:3]
   qq = yy[3:6]
   d_xx = - 2 * qq
   d_qq = - qq + xx
   result = np.concatenate((d_xx, d_qq))
   return result
'''

def draw():
   array_tt = np.linspace(0, 10, 100)
   yy_initial = [
      1/3, 1/3, 1/3,
      0, 0, 0,
      0, 0, 0,
   ]
   answer = Solve(
      fun = update,
      t_span = [0, 10],
      y0 = yy_initial,
      t_eval = array_tt,
   )
   #print("y = ", answer.y)
   #print("t = ", answer.t)
   array_xx = [np.linalg.norm(row[0:3]) for row in answer.y.transpose()]
   Plot.plot(
      array_tt,
      array_xx,
   )
   Plot.xlabel("along x[2] == 0")
   Plot.ylabel("along x[0] == x[1]")
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

'''
   xx_initial = np.array([1/2, 1/2, 0])
   array_time, array_output = ct.input_output_response(
      handle_closed,
      T = np.linspace(0, 50, 250),
      #U = None,
      X0 = [1/2, 1/2, 0, 0, 0, 0],
      #X0 = [1/2, 1/2, 0, 0, 0, 0, 0, 0, 0],
      #X0 = [1/2, 1/2, 0],
   )
'''



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
