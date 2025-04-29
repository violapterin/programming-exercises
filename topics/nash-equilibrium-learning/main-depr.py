#! /usr/bin/env python3

import os
import control as ct
import numpy as np
import matplotlib.pyplot as Plot

def main():
   many_catalog = generate_parameter()
   for catalog in many_catalog:
      print("Case:")
      print(catalog["title"])
      draw(catalog)

def draw(catalog):
   handle_evolution = ct.NonlinearIOSystem(
      give_update_evolution(catalog),
      give_output_evolution(catalog),
      inputs = 3,
      outputs = 3,
      states = 3,
      name = 'evolution',
   )
   handle_payoff_proper = ct.NonlinearIOSystem(
      update_payoff_proper,
      output_payoff_proper,
      inputs = 3,
      outputs = 3,
      states = 3,
      name = 'payoff_proper',
   )
   handle_first_order = ct.NonlinearIOSystem(
      give_update_first_order(catalog),
      give_output_first_order(catalog),
      inputs = 3,
      outputs = 3,
      states = 3,
      name = 'first_order',
   )
   handle_closed = ct.interconnect(
      [handle_evolution, handle_payoff_proper],
      connections = [
         ['evolution.u[0]', 'payoff_proper.y[0]'],
         ['evolution.u[1]', 'payoff_proper.y[1]'],
         ['evolution.u[2]', 'payoff_proper.y[2]'],
         ['payoff_proper.u[0]', 'evolution.y[0]'],
         ['payoff_proper.u[1]', 'evolution.y[1]'],
         ['payoff_proper.u[2]', 'evolution.y[2]'],
      ],
      inplist = [],
      inputs = 0,
      outlist = ['evolution.y[0]', 'evolution.y[1]', 'evolution.y[2]'],
      outputs = 3,
      states = 6,
      name = 'closed',
   )
   '''
   handle_closed = ct.interconnect(
      [handle_evolution, handle_first_order, handle_payoff_proper],
      connections = [
         ['first_order.u[0]', 'payoff_proper.y[0]'],
         ['first_order.u[1]', 'payoff_proper.y[1]'],
         ['first_order.u[2]', 'payoff_proper.y[2]'],
         ['evolution.u[0]', 'first_order.y[0]'],
         ['evolution.u[1]', 'first_order.y[1]'],
         ['evolution.u[2]', 'first_order.y[2]'],
         ['payoff_proper.u[0]', 'evolution.y[0]'],
         ['payoff_proper.u[1]', 'evolution.y[1]'],
         ['payoff_proper.u[2]', 'evolution.y[2]'],
      ],
      inplist = [],
      inputs = 0,
      outlist = ['evolution.y[0]', 'evolution.y[1]', 'evolution.y[2]'],
      outputs = 3,
      states = 9,
      name = 'closed',
   )
   '''
   '''
   handle_payoff = ct.interconnect(
      [handle_payoff_proper, handle_first_order],
      connections = [
         ['first_order.u[0]', 'payoff_proper.y[0]'],
         ['first_order.u[1]', 'payoff_proper.y[1]'],
         ['first_order.u[2]', 'payoff_proper.y[2]'],
      ],
      inplist = ['payoff_proper.u[0]', 'payoff_proper.u[1]', 'payoff_proper.u[2]'],
      inputs = 3,
      outlist = ['first_order.y[0]', 'first_order.y[1]', 'first_order.y[2]'],
      outputs = 3,
      states = 6,
      name = 'payoff',
   )
   handle_closed = ct.interconnect(
      [handle_evolution, handle_payoff],
      connections = [
         ['evolution.u[0]', 'payoff.y[0]'],
         ['evolution.u[1]', 'payoff.y[1]'],
         ['evolution.u[2]', 'payoff.y[2]'],
         ['payoff.u[0]', 'evolution.y[0]'],
         ['payoff.u[1]', 'evolution.y[1]'],
         ['payoff.u[2]', 'evolution.y[2]'],
      ],
      inplist = [],
      inputs = 0,
      outlist = ['evolution.y[0]', 'evolution.y[1]', 'evolution.y[2]'],
      outputs = 3,
      states = 9,
      name = 'closed',
   )
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

   Plot.plot(
      array_time,
      array_output,
   )
   Plot.xlabel("along x[2] == 0")
   Plot.ylabel("along x[0] == x[1]")
   Plot.title("trajectory")
   Plot.subplots_adjust(top = 0.75)
   Plot.legend(
      loc = "center left",
      bbox_to_anchor = (0.0, 1.14),
      ncol = 3,
      fontsize = "x-small",
   )
   Plot.savefig(
      catalog.get("title"),
      format = "png"
   )
   Plot.clf()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def generate_parameter():
   many_rule = ["smith", "brown", "hybrid"]
   many_mu = [2 ** zz for zz in range(-1, 2)]
   many_nu = [2 ** zz for zz in range(-1, 2)]
   many_alpha = [(1/6) ** zz for zz in range(1, 4)]
   many_catalog = []
   count = 0
   for rule in many_rule:
      for alpha in many_alpha:
         for mu in many_mu:
            for nu in many_nu:
               count += 1
               proper = (
                  ''
                  + "no-{}-".format(str(count))
                  + "rule-{}-".format(rule)
                  + "alpha-{:.2f}-".format(nu)
                  + "mu-{:.2f}-".format(mu)
                  + "nu-{:.2f}-".format(nu)
               )
               title = proper.replace('.', '-')
               catalog = {
                  "title": title,
                  "rule": rule,
                  "alpha": alpha,
                  "mu": mu,
                  "nu": nu,
               }
               many_catalog.append(catalog.copy())
   return many_catalog

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# tt: time
# qq: state

def update_payoff_proper(tt, ss, xx, hold):
   return None

# Sandholm, Population Games and Evolutionary Dynamics, p.62
def output_payoff_proper(tt, ss, xx, hold):
   pp = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2),
   ])
   return pp

def give_update_first_order(catalog):
   mu = catalog.get("mu")
   nu = catalog.get("nu")
   update_first_order = (
      lambda tt, qq, uu, table:
      uu - mu * qq
   )
   return update_first_order

def give_output_first_order(catalog):
   mu = catalog.get("mu")
   nu = catalog.get("nu")
   output_first_order = (
      lambda tt, qq, uu, table:
      (mu / (mu * nu + 1)) * (nu * uu + qq)
   )
   return output_first_order

def give_update_evolution(catalog):
   rule = catalog.get("rule")
   alpha = catalog.get("alpha")
   result = None
   if (rule == "smith"):
      result = (
         lambda tt, xx, pp, table: (
            alpha * update_best_response(tt, xx, pp)
            + (1 - alpha) * update_smith(tt, xx, pp)
         )
      )
   elif (rule == "brown"):
      result = (
         lambda tt, xx, pp, table: (
            alpha * update_best_response(tt, xx, pp)
            + (1 - alpha) * update_brown(tt, xx, pp)
         )
      )
   elif (rule == "hybrid"):
      result = (
         lambda tt, xx, pp, table: (
            alpha * update_best_response(tt, xx, pp)
            + (1 - alpha) * update_hybrid(tt, xx, pp)
         )
      )
   return result

def give_output_evolution(catalog):
   result = (
      lambda tt, xx, pp, table:
      xx
   )

def update_smith(tt, xx, pp):
   vv = np.zeros(3)
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * max(pp[j] - pp[i], 0) # T[j, i]
            + xx[i] * max(pp[i] - pp[j], 0) # T[i, j]
         )
   return vv

def update_brown(tt, xx, pp):
   vv = np.zeros(3)
   pp_hat = np.inner(pp, xx)
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * max(pp[i] - pp_hat, 0) # T[j, i]
            + xx[i] * max(pp[j] - pp[j], 0) # T[i, j]
         )
   return vv

def update_hybrid(tt, xx, pp):
   vv = np.zeros(3)
   pp_hat = np.inner(pp, xx)
   for i in range(3):
      vv[i] = 0
      for j in range(3):
         vv[i] += (
            xx[j] * (
               2 * max(pp[i] - pp[j], 0)
               + max(pp[j] - pp[i], 0) ** 2
               + 4 * max(pp[i] - pp_hat, 0) ** 3
               + np.exp(pp[i] - pp_hat) - 1
            ) # T[j, i]
            + xx[i] * (
               2 * max(pp[j] - pp[i], 0)
               + max(pp[i] - pp[j], 0) ** 2
               + 4 * max(pp[j] - pp_hat, 0) ** 3
               + np.exp(pp[j] - pp_hat) - 1
            ) # T[i, j]
         )
   return vv

def update_best_response(tt, xx, pp):
   yy = np.array(pp, copy = True)
   pp_max = max(pp)
   for index in range(len(pp)):
      if (yy[index] < pp_max - 1e-6):
         yy[index] = 0
   yy = yy / np.count_nonzero(yy)
   vv = yy - xx
   return vv

def project_to_simplex(xx):
   nn = len(xx)
   unit_aa = np.array([1, -1, 0])
   unit_bb = np.array([1, -1, 0])
   unit_aa = unit_aa / np.linalg.norm(unit_aa)
   unit_bb = unit_bb / np.linalg.norm(unit_bb)
   result = np.array([
      (np.eye(nn) - unit_aa @ unit_aa.T) @ xx,
      (np.eye(nn) - unit_bb @ unit_bb.T) @ xx + 1 / np.sqrt(6),
   ])
   return result

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

test()
