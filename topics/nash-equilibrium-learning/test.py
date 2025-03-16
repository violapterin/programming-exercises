#! /usr/bin/env python3

import os
import control as ct
import numpy as np
import matplotlib.pyplot as Plot

from custom import custom

def test():
   block_evolution = block_best_response
   handle_payoff_proper = ct.nlsys(
      block_payoff_proper, # update function
      None,
      inputs = ('xx'),
      outputs = ('uu'),
      name = 'payoff_proper'
   )
   handle_first_order = ct.nlsys(
      block_first_order, # update function
      None,
      inputs = ('uu'),
      outputs = ('pp'),
      states = ('qq'),
      name = 'first_order'
   )
   handle_evolution = ct.nlsys(
      None,
      block_evolution, # output function
      inputs = ('xx'),
      outputs = ('pp'),
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

   xx_0 = np.array([1, 0, 0])
   qq_0 = np.array([0, 0, 0])
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
      name_transient,
      format = "png"
   )
   Plot.clf()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# tt: time
# qq: state

# Sandholm, Population Games and Evolutionary Dynamics, p.62
def block_payoff_proper_output(tt, qq, xx):
   pp = np.array([
      - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
      - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
      - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2),
   ])
   return pp

def block_first_order_output(tt, qq, uu):
   cc = give_constant()
   mu = cc.get("mu")
   nu = cc.get("nu")
   pp = (mu / (mu * nu + 1)) * (nu * uu + qq)
   return pp

def block_first_order_update(tt, qq, uu):
   cc = give_constant()
   mu = cc.get("mu")
   ddqq = uu - mu * qq
   return ddqq

def block_best_response(tt, pp, vv):
   a = params.get('a', 3.2)
   b = params.get('b', 0.6)
   c = params.get('c', 50.)
   d = params.get('d', 0.56)
   k = params.get('k', 125)
   r = params.get('r', 1.6)
   H = x[0]
   L = x[1]
   u_0 = u[0] if u[0] > 0 else 0
   dH = (r + u_0) * H * (1 - H/k) - (a * H * L)/(c + H)
   dL = b * (a * H *  L)/(c + H) - d * L

   return np.array([dH, dL])

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

def give_constant():
   return {
      'mu': 1.0,
      'nu': 2.0,
   }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

test()
