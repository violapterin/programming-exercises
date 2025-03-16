#! /usr/bin/env python3

import os
import control as ct
import numpy as np
import matplotlib.pyplot as Plot

from custom import custom

def test():
   many_catalog = generate_parameter()
   for catalog in many_catalog:
      draw(catalog)

def draw(catalog):
   title = catalog.get("title")
   nu = catalog.get("nu")
   mu = catalog.get("mu")
   update_evolution = catalog.get("update_evolution")
   handle_payoff_proper = ct.nlsys(
      update_payoff_proper,
      output_payoff_proper,
      inputs = ('xx'),
      outputs = ('uu'),
      name = 'payoff_proper'
   )
   handle_first_order = ct.nlsys(
      update_first_order,
      output_first_order,
      inputs = ('uu'),
      outputs = ('pp'),
      states = ('qq'),
      name = 'first_order'
   )
   handle_evolution = ct.nlsys(
      update_evolution,
      output_evolution,
      inputs = ('pp'),
      outputs = ('xx'),
      states = ('qq'),
      name = 'evolution'
   )
   handle_payoff = ct.interconnect(
      [handle_payoff_proper, handle_first_order],
      connections = [
         ['evolution.pp', 'payoff.pp'],
         ['payoff.xx', 'evolution.xx'],
      ],
      outlist = ['evolution.xx'],
      outputs = 'xx',
   )
   handle_closed = ct.interconnect(
      [handle_evolution, handle_payoff],
      connections = [
         ['evolution.pp', 'payoff.pp'],
         ['payoff.xx', 'evolution.xx'],
      ],
      outlist = ['evolution.xx'],
      outputs = 'xx',
   )

   xx_initial = np.array([1, 0, 0])
   qq_initial = np.array([0, 0, 0])
   array_time, array_output = ct.input_output_response(
      handle_closed,
      T = np.linspace(0, 50, 250),
      U = 0,
      X0 = np.vstack((xx_0, qq_0)),
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
      title,
      format = "png"
   )
   Plot.clf()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def generate_parameter():
   many_rule = ["smith", "brown", "hybrid"]
   many_mu = [2 ** zz for zz in range(-1, 2)]
   many_nu = [2 ** zz for zz in range(-1, 2)]
   many_alpha = [(1/6) ** zz for zz in range(1, 4)]
   result = []
   for rule in many_rule:
      for alpha in many_alpha:
         for mu in many_mu:
            for nu in many_nu:
               title = "rule-"
               result = {
                  title: title
               }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# tt: time
# qq: state

def update_payoff_proper(tt, rr, xx):
   return None

# Sandholm, Population Games and Evolutionary Dynamics, p.62
def output_payoff_proper(tt, rr, xx):
   pp = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2),
   ])
   return pp

def give_update_first_order(cc):
   mu = cc.get("mu")
   nu = cc.get("nu")
   update_first_order = (
      lambda tt, qq, uu:
      uu - mu * qq
   )
   return update_first_order

def give_output_first_order(cc):
   mu = cc.get("mu")
   nu = cc.get("nu")
   output_first_order = (
      lambda tt, qq, uu:
      (mu / (mu * nu + 1)) * (nu * uu + qq)
   )
   return output_first_order

def give_update_evolution(cc):
   rule = cc.get("rule")
   alpha = cc.get("alpha")
   if (rule == "smith"):
      result = (
         lambda tt, xx, pp: (
            alpha * update_best_response(tt, xx, pp)
            + (1 - alpha) * update_smith(tt, xx, pp)
         )
      )
   elif (rule == "brown"):
      result = (
         lambda tt, xx, pp: (
            alpha * update_best_response(tt, xx, pp)
            + (1 - alpha) * update_brown(tt, xx, pp)
         )
      )
   elif (rule == "hybrid"):
      result = (lambda tt, qq, uu:
         lambda tt, xx, pp: (
            alpha * update_best_response(tt, xx, pp)
            + (1 - alpha) * update_hybrid(tt, xx, pp)
         )
      )

def give_output_evolution(cc):
   result = (
      lambda tt, xx, pp: (xx)
   )

def update_smith(tt, xx, pp):
   return None

def update_brown(tt, xx, pp):
   return None

def update_hybrid(tt, xx, pp):
   return None

def update_best_response(tt, xx, pp):
   pp_copy = np.array(pp, copy = True)
   pp_max = max(pp)
   result = []
   for value in pp:
      if pp_copy < pp_max:
         result.append(0)
      else:
         result.append(value)
   return result

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
