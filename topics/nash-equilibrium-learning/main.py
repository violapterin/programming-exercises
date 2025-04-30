#! /usr/bin/env python3

import os
#import control as ct
import numpy as np
from scipy.integrate import solve_ivp as Solve
import matplotlib.pyplot as Plot



def main():
   os.system("rm -rf ./{}".format("plot"))
   os.system("mkdir {}".format("plot"))
   #os.system("python3 ./draw.py {}".format(mode))
   #test()
   #draw()
   many_catalog = generate_parameter()
   cutoff = 24 # XXX
   for catalog in many_catalog:
      if (catalog["count"] > cutoff): break
      print("Case {} of {}: {}".format(catalog["count"], catalog["total"], catalog["title"]))
      draw(catalog)

def payoff(xx):
   uu = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2)
   ])
   return uu

def give_update_from_catalog(catalog):
   def update(tt, yy):
      mu = catalog["mu"]
      nu = catalog["nu"]
      gamma = catalog["gamma"]
      xx = yy[0:3]
      ss = yy[3:6]
      uu = payoff(xx)
      pp = gamma * ss + gamma * nu * uu
      d_xx = np.zeros(3)
      if (catalog["rule"] == "smith"):
         d_xx = update_hybrid(xx, pp)
      elif (catalog["rule"] == "brown"):
         d_xx = update_brown(xx, pp)
      elif (catalog["rule"] == "best"):
         d_xx = update_best(xx, pp)
      d_ss = uu - mu * ss
      result = np.concatenate((d_xx, d_ss))
      return result
   return update

def draw(catalog):
   array_tt = np.linspace(0, 10, 100)
   yy_initial = np.concatenate(
      (catalog["start"], np.array([0, 0, 0]))
   )
   #print("initial: ", project_to_simplex(yy_initial[0:3]))
   update = give_update_from_catalog(catalog)
   answer = Solve(
      fun = update,
      t_span = [0, 10],
      y0 = yy_initial,
      t_eval = array_tt,
      method = 'Radau',
   )
   #print("t = ", answer.t)
   trajectory = np.array([
      project_to_simplex(row[0:3])
      for row in answer.y.transpose()
   ])
   #print("trajectory: ", trajectory)
   Plot.plot(
      trajectory.transpose()[0],
      trajectory.transpose()[1],
      marker = "D",
   )
   Plot.xlabel("along (-1, 1, 0)")
   Plot.ylabel("along (-1/2, -1/2, 1)")
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
      "plot/" + catalog["title"] + ".png",
      format = "png"
   )
   Plot.clf()

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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def generate_parameter():
   many_start = [
      np.array([1/3, 2/3, 0]),
      np.array([2/3, 1/3, 0]),
      np.array([1/3, 0, 2/3]),
      np.array([2/3, 0, 1/3]),
      np.array([0, 1/3, 2/3]),
      np.array([0, 2/3, 1/3]),
   ]
   many_rule = ["smith", "brown", "hybrid"]
   many_mu = [3 ** zz for zz in range(-1, 0)]
   many_mu = [- mu for mu in many_mu] + [0] + many_mu
   many_nu = [3 ** zz for zz in range(-1, 0)]
   many_nu = [- nu for nu in many_nu] + [0] + many_nu
   #many_alpha = [(1/6) ** zz for zz in range(1, 4)]
   many_alpha = [1.00]
   many_gamma = [1.00]
   total = len(many_rule) * len(many_start) * len(many_alpha) * len(many_mu) * len(many_nu)
   many_catalog = []
   count = 0
   for alpha in many_alpha:
      for gamma in many_gamma:
         for start in many_start:
            for mu in many_mu:
               for nu in many_nu:
                  for rule in many_rule:
                     count += 1
                     proper = (
                        ''
                        + "no-{}-".format(str(count))
                        + "start-{:.1f},{:.1f},{:.1f}-".format(start[0], start[1], start[2])
                        + "rule-{}-".format(rule)
                        + "mu-{:.2f}-".format(mu)
                        + "nu-{:.2f}-".format(nu)
                        + "alpha-{:.2f}-".format(alpha)
                        + "gamma-{:.2f}-".format(gamma)
                     )
                     title = proper.replace('.', '-')
                     catalog = {
                        "title": title,
                        "count": count,
                        "total": total,
                        "start": start,
                        "rule": rule,
                        "alpha": alpha,
                        "gamma": gamma,
                        "mu": mu,
                        "nu": nu,
                     }
                     many_catalog.append(catalog.copy())
   return many_catalog

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
