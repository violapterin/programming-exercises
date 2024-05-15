#!/usr/bin/env python3

import numpy as NP
import scipy as SP
import matplotlib.pyplot as Plot
import datetime

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main(situation):
   horizon = 64
   size_xx = 16
   size_uu = 12
   size_yy = 8
   identity_xx = NP.eyes(size = (size_xx, size_xx))
   identity_uu = NP.eyes(size = (size_uu, size_uu))
   identity_yy = NP.eyes(size = (size_yy, size_yy))
   mean_mm_present_last = NP.zeros(size = size_xx)
   variance_ss_present_last = NP.zeros(size = (size_xx, size_xx))
   number_experiment = 32

   state_xx_last = NP.zeros((size_xx, 1))
   control_uu_last = NP.zeros((size_uu, 1))
   dynamics_aa = NP.random.normal(0, 1, size = (size_xx, size_xx))
   dynamics_bb = NP.random.normal(0, 1, size = (size_xx, size_uu))
   projection_cc = NP.random.normal(0, 1, size = (size_xx, size_yy))
   dynamics_aa_tt = NP.transpose(dynamics_aa)
   dynamics_bb_tt = NP.transpose(dynamics_bb)
   projection_cc_tt = NP.transpose(projection_cc)
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
   many_control_uu = [[] for _ in range(horizon)]
   for _ in range(number_experiment):
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
         feedback = (
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
         control_uu = feedback @ mean_mm_present
         many_state_xx[index_tt].append(state_xx)
         many_control_uu[index_tt].append(control_uu)
         state_xx_last = state_xx
         control_uu_last = control_uu
         mean_mm_present_last = mean_mm_present
         variance_ss_present_last = variance_ss_present

   variance_ll_xx = NP.cov(many_state_xx[index_tt], many_state_xx[index_tt])
   variance_ll_yy_xx = NP.cov(many_state_yy[index_tt], many_state_xx[index_tt])
   variance_ll_yy = NP.cov(many_state_yy[index_tt], many_state_yy[index_tt])
   unitary_gg, singular_ss, unitary_ff_tt = numpy.linalg.svd(
      NP.linalg.inv(variance_ll_yy)
      @ variance_ll_yy_xx
      @ NP.linalg.inv(variance_ll_xx)
   )
   unitary_gg_tt = NP.transpose(unitary_gg)
   unitary_ff = NP.transpose(unitary_ff_tt)

   for index_tt in range(horizon):

   count_line = 0
   count_marker = 0
   many_line = ['-', '--', '-.', ':']
   many_marker = ['o', 's', 'D', 'P', '^', 'v']
   for curve in result:
      many_pair = curve[1:]
      array_first = [pair[0] for pair in many_pair]
      array_second = [pair[1] for pair in many_pair]
      Plot.plot(
         array_first,
         array_second,
         label = curve[0],
         linestyle = many_line[count_line],
         marker = many_marker[count_marker],
      )
      count_line = (count_line + 1) % len(many_line)
      count_marker = (count_marker + 1) % len(many_marker)

   Plot.xlabel("edge squared over sample (log)")
   Plot.ylabel("squared loss squared (log)")
   Plot.title("Attention Mechanism")
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


# # # # # # # # # # # # # # # # # # # # # # # #


main("final-small")
main("final-medium")
main("final-large")
