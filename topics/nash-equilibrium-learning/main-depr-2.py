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

def test():
   array = [[1,3], [2,4]]
   np.concatenate(array)
   flat = [item for row in array for item in row]
   print(flat)

def update(tt, yy):
   xx = yy[0:3]
   qq = yy[3:6]
   uu = yy[6:9]
   ss = yy[9:12]
   pp = yy[12:15]
   d_xx = vv(xx, pp)
   d_qq = gg(qq, xx)
   d_uu = np.array([
      (
         - (20 + 30 * 2 * (xx[0] + xx[2])) * vv(xx, pp)[0]
         - (30 * 2 * (xx[0] + xx[2])) * vv(xx, pp)[2]
      ),
      (
         - (20 + 30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[1]
         - (30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[2]
      ),
      (
         - (30 * 2 * (xx[0] + xx[2])) * vv(xx, pp)[0]
         - (30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[1]
         - (20 + 30 * 2 * (xx[0] + xx[2]) + 30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[2]
      ),
   ])
   d_ss = (uu - mu * ss)
   d_pp = (
      gamma * d_ss(xx, qq, uu, ss, pp)
      + gamma * nu * d_uu(xx, qq, uu, ss, pp)
   )


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


def draw():
   mu = 1
   nu = 1
   gamma = 1
   gg = (lambda qq, xx: np.zeros(3))
   vv = vv_smith
   '''
   hh = (
      lambda qq, xx:
      [
         - (6 + 20 * xx[0] + 30 * (xx[0] + xx[2]) ** 2),
         - (6 + 20 * xx[1] + 30 * (xx[1] + xx[2]) ** 2),
         - (5 + 20 * xx[2] + 30 * (xx[0] + xx[2]) ** 2 + 30 * (xx[1] + xx[2]) ** 2)
      ]
   )
   '''
   d_xx = (
      lambda xx, qq, uu, ss, pp:
      vv(xx, pp)
   )
   d_qq = (
      lambda xx, qq, uu, ss, pp:
      gg(qq, xx)
   )
   d_uu = (
      lambda xx, qq, uu, ss, pp:
      np.array([
         (
            - (20 + 30 * 2 * (xx[0] + xx[2])) * vv(xx, pp)[0]
            - (30 * 2 * (xx[0] + xx[2])) * vv(xx, pp)[2]
         ),
         (
            - (20 + 30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[1]
            - (30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[2]
         ),
         (
            - (30 * 2 * (xx[0] + xx[2])) * vv(xx, pp)[0]
            - (30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[1]
            - (20 + 30 * 2 * (xx[0] + xx[2]) + 30 * 2 * (xx[1] + xx[2])) * vv(xx, pp)[2]
         ),
      ])
   )
   d_ss = (
      lambda xx, qq, uu, ss, pp:
      uu - mu * ss
   )
   d_pp = (
      lambda xx, qq, uu, ss, pp:
      (
         gamma * d_ss(xx, qq, uu, ss, pp)
         + gamma * nu * d_uu(xx, qq, uu, ss, pp)
      )
   )
   array_tt = np.linspace(0, 10, 100)
   update = (
      lambda xx, qq, uu, ss, pp:
      (
         np.array([
            d_xx(xx, qq, uu, ss, pp)[0], d_xx(xx, qq, uu, ss, pp)[1], d_xx(xx, qq, uu, ss, pp)[2],
            d_qq(xx, qq, uu, ss, pp)[0], d_qq(xx, qq, uu, ss, pp)[1], d_qq(xx, qq, uu, ss, pp)[2],
            d_uu(xx, qq, uu, ss, pp)[0], d_uu(xx, qq, uu, ss, pp)[1], d_uu(xx, qq, uu, ss, pp)[2],
            d_ss(xx, qq, uu, ss, pp)[0], d_ss(xx, qq, uu, ss, pp)[1], d_ss(xx, qq, uu, ss, pp)[2],
            d_pp(xx, qq, uu, ss, pp)[0], d_pp(xx, qq, uu, ss, pp)[1], d_pp(xx, qq, uu, ss, pp)[2],
         ])
      )
   )
   yy_initial = [
      1/3, 1/3, 1/3,
      0, 0, 0,
      0, 0, 0,
      0, 0, 0,
      0, 0, 0,
   ]
   answer = Solve(
      update,
      [0, 10],
      yy_initial,
      t_eval = array_tt,
   )
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

# tt: time
# qq: state

'''
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
'''

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
