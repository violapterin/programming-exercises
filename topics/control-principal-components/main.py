#!/usr/bin/env python3

import numpy as NP
import scipy as SP
import matplotlib.pyplot as Plot
import datetime

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(situation):
   number_sample_train = 16
   number_sample_experiment = 16
   ratio_singular_kept = [0.8 + 0.05 * x for in list(range(4))]
   many_sample_yy = []
   many_sample_uu = []
   many_sample_vv = []

   for _ in range(number_sample_train):
      hold = run_linear_quadratic_regulator(
         horizon = 64
         size_xx = 16
         size_uu = 12
         size_yy = 8
         factor_cost = 1
         number_experiment = 32
      )
      many_sample_yy = hold[0]
      many_sample_uu = hold[1]

   many_reduction = [] # XXX
   for index_tt in range(horizon):
      variance_ll_uu = NP.cov(many_sample_uu[index_tt], many_sample_uu[index_tt])
      variance_ll_yy_uu = NP.cov(many_sample_yy[index_tt], many_sample_uu[index_tt])
      variance_ll_yy = NP.cov(many_sample_yy[index_tt], many_sample_yy[index_tt])
      unitary_gg, singular_ss, unitary_ff_tt = NP.linalg.svd(
         NP.linalg.inv(variance_ll_yy)
         @ variance_ll_yy_uu
         @ NP.linalg.inv(variance_ll_uu)
      )
      unitary_gg_tt = NP.transpose(unitary_gg)
      unitary_ff = NP.transpose(unitary_ff_tt)
      many_reduction.append(projection_ff)

   for _ in range(number_sample_experiment):
      hold = run_linear_quadratic_regulator(
         many_projection_cc = many_projection_cc,
         horizon = 64
         size_xx = 16
         size_uu = 12
         size_yy = 8
         factor_cost = 1
      )
      many_sample_vv = hold[0]

   '''
   count_line = 0
   count_marker = 0
   many_line = ['-', '--', '-.', ':']
   many_marker = ['o', 's', 'D', 'P', '^', 'v']
   '''
   Plot.plot(
      ratio_singular_kept,
      many_sample_vv,
      linestyle = ['-', '--'],
      marker = ['o', 's'],
   )

   Plot.xlabel("ratio of number of singular values")
   Plot.ylabel("cost function")
   Plot.title("Linear quadratic control with ")
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def run_linear_quadratic_regulator(
   many_reduction,
   horizon,
   size_xx,
   size_uu,
   size_yy,
   factor_cost,
):

   identity_xx = NP.eyes(size = (size_xx, size_xx))
   identity_uu = NP.eyes(size = (size_uu, size_uu))
   identity_yy = NP.eyes(size = (size_yy, size_yy))
   dynamics_aa = NP.random.normal(0, 1, size = (size_xx, size_xx))
   dynamics_bb = NP.random.normal(0, 1, size = (size_xx, size_uu))
   dynamics_aa_tt = NP.transpose(dynamics_aa)
   dynamics_bb_tt = NP.transpose(dynamics_bb)
   for index_tt in range(horizon):
      projection_cc = (
         many_reduction[index_tt]
         @ NP.random.normal(0, 1, size = (size_xx, size_yy))
      )
      projection_cc_tt = NP.transpose(projection_cc)

   mean_mm_present_last = NP.zeros(size = size_xx)
   variance_ss_present_last = NP.zeros(size = (size_xx, size_xx))
   mean_mm_future_last = NP.zeros(size = size_xx)
   variance_ss_future_last = NP.zeros(size = (size_xx, size_xx))
   state_xx_last = NP.zeros((size_xx, 1))
   control_uu_last = NP.zeros((size_uu, 1))

   many_cost_pp = []
   cost_pp = identity_xx
   cost_pp_next = cost_pp
   many_cost_pp.append(cost_pp)
   for _ in reversed(range(horizon)):
      cost_pp = (
         dynamics_aa_tt @ cost_pp_next @ dynamics_aa
         - dynamics_aa_tt @ cost_pp_next @ dynamics_bb
            @ NP.linalg.inv(
               dynamics_bb_tt @ cost_pp_next @ dynamics_bb
               + identity_uu
            )
            @ dynamics_bb_tt @ cost_pp_next @ dynamics_aa
         + identity_xx
      )
      many_cost_pp.append(cost_pp)
      cost_pp_next = cost_pp

   many_state_xx = [[] for _ in range(horizon)]
   many_state_yy = [[] for _ in range(horizon)]
   many_control_uu = [[] for _ in range(horizon)]
   many_value_vv = []


   for index_tt in range(horizon):
      noise_ww = NP.random.normal(0, 1, size = size_xx)
      noise_vv = NP.random.normal(0, 1, size = size_yy)
      state_xx = (
         dynamics_aa @ state_xx_last
         + dynamics_bb @ control_uu_last
         + noise_ww
      )
      state_yy = (
         projection_cc @ state_xx
         + noise_vv
      )
      cost_pp_next = many_cost_pp[index_tt + 1]
      feedback_kk = (
         - NP.linalg.inv(
            dynamics_bb_tt @ cost_pp_next @ dynamics_bb
            + identity_uu
         )
         @ dynamics_bb_tt @ cost_pp_next @ dynamics_aa
      )
      hold_cc_ss_cc = NP.linalg.inv(
         projection_cc @ variance_ss_future_last @ projection_cc_tt
         + identity_yy
      )
      mean_mm_future_last = dynamics_aa @ mean_mm_present_last
      variance_ss_future_last = (
         dynamics_aa @ variance_ss_present_last @ dynamics_aa_tt
         + identity_xx
      )
      mean_mm_present = (
         mean_mm_future_last
         + variance_ss_future_last @ projection_cc_tt
         @ hold_cc_ss_cc
         @ (state_yy - projection_cc @ mean_mm_future_last)
      )
      variance_ss_present = (
         variance_ss_future_last
         + variance_ss_future_last @ projection_cc_tt
         @ hold_cc_ss_cc
         @ projection_cc @ variance_ss_future_last
      )
      control_uu = feedback_kk @ mean_mm_present
      value_vv += NP.linalg.norm(control_uu) ** 2
      value_vv += factor_cost * NP.linalg.norm(state_xx) ** 2
      many_state_xx[index_tt].append(state_xx)
      many_state_yy[index_tt].append(state_yy)
      many_control_uu[index_tt].append(control_uu)
      state_xx_last = state_xx
      control_uu_last = control_uu
      mean_mm_present_last = mean_mm_present
      variance_ss_present_last = variance_ss_present
   many_value_vv.append(value_vv)
   return [many_state_yy, many_control_uu, many_value_vv]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

main("final-small")
main("final-medium")
main("final-large")
