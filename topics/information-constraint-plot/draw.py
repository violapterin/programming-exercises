#! /usr/bin/env python3

import sys
import time
import copy
import numpy as NP
import matplotlib.pyplot as Plot

from custom import custom

def main():
   mode = sys.argv[1]
   many_flavor = custom.get_many_flavor(mode)
   for flavor in many_flavor:
      if (flavor.startswith("transient")):
         be_truncated = flavor.endswith("truncated")
         all_catalog = custom.give_all_catalog_transient(be_truncated)
         minute_start = time.time()
         for many_many_catalog in all_catalog:
            many_many_catalog.pop(0)
            for many_catalog in many_many_catalog:
               many_catalog.pop(0)
               for catalog in many_catalog:
                  total = catalog[0]["total"]
                  count = catalog[0]["count"]
                  catalog.pop(0)
                  draw_transient(catalog)
                  minute_remaining = (
                     ((total - count) / count)
                     * (time.time() - minute_start) / 60
                  )
                  print("({:.2f} minutes remaining)".format(minute_remaining))
      if (flavor.startswith("steady")):
         be_truncated = flavor.endswith("truncated")
         all_catalog = custom.give_all_catalog_steady(be_truncated)
         minute_start = time.time()
         for many_many_catalog in all_catalog:
            many_many_catalog.pop(0)
            for many_catalog in many_many_catalog:
               many_catalog.pop(0)
               for catalog in many_catalog:
                  total = catalog[0]["total"]
                  count = catalog[0]["count"]
                  catalog.pop(0)
                  draw_steady(catalog)
                  minute_remaining = (
                     ((total - count) / count)
                     * (time.time() - minute_start) / 60
                  )
                  print("({:.2f} minutes remaining)".format(minute_remaining))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def draw_steady(catalog):
   cc = custom.give_constant()
   many_curve = []
   many_error = []
   many_legend = []
   many_eta = custom.array_unsigned(*cc["power_eta"])
   many_rho = custom.array_unsigned(*cc["power_rho"])

   for parameter in catalog:
      curve = []
      error = []
      for rho in many_rho:
         many_series = []
         for eta in many_eta:
            horizon = cc["horizon_steady"] - 1
            series = []
            aa_up_new = parameter["rr_hat"]
            bb_up_new = 0
            cc_up_new = 0
            aa_down_new = parameter["rr_hat"]
            bb_down_new = 0
            cc_down_new = 0
            up_new = (aa_up_new, bb_up_new, cc_up_new)
            down_new = (aa_down_new, bb_down_new, cc_down_new)
            gap = evaluate_for_gaussian(*up_new, *down_new)
            series.append(gap)
            up_old = up_new
            down_old = down_new
            horizon -= 1
            while (horizon >= 0):
               tuning = (
                  parameter["rr"],
                  parameter["pp"],
                  parameter["qq"],
                  rho,
                  eta,
               )
               aa_up_new = aa_up_original(*tuning)(*up_old)
               bb_up_new = bb_up_original(*tuning)(*up_old)
               cc_up_new = cc_up_original(*tuning)(*up_old)
               aa_down_new = aa_down_original(*tuning)(*down_old)
               bb_down_new = bb_down_original(*tuning)(*down_old)
               cc_down_new = cc_down_original(*tuning)(*down_old)
               up_new = (aa_up_new, bb_up_new, cc_up_new)
               down_new = (aa_down_new, bb_down_new, cc_down_new)
               gap = evaluate_for_gaussian(*up_new, *down_new)
               series.append(gap)
               up_old = up_new
               down_old = down_new
               horizon -= 1
            many_series.append(copy.deepcopy(series))
         (steady, bar) = extract_steady(many_series)
         curve.append(steady)
         error.append(bar)
      many_curve.append(copy.deepcopy(curve))
      many_error.append(copy.deepcopy(error))
      many_legend.append("r = {:.3f}".format(parameter["rr"]))

   name_steady = custom.obtain_name_steady(catalog)
   print(
      ">>> plot", catalog[0]["count"],
      "of", catalog[0]["total"],
      ":", name_steady
   )

   for index in range(len(many_curve)):
      Plot.errorbar(
         many_rho,
         many_curve[index],
         yerr = many_error[index],
         label = many_legend[index % len(many_legend)],
         color = cc["many_color"][index % len(cc["many_color"])],
         linestyle = cc["many_style"][index % len(cc["many_style"])],
         marker = cc["many_marker"][index % len(cc["many_marker"])],
         elinewidth = cc["width_error"],
         ecolor = 'y',
         markersize = cc["size_marker"],
      )

   Plot.xlabel("information constraint ρ")
   Plot.ylabel("relative gap in steady state")
   Plot.title("gap between upper and lower bounds")
   Plot.xscale("log")
   Plot.yscale("log")
   Plot.subplots_adjust(top = 0.75)
   Plot.legend(
      loc = "center left",
      bbox_to_anchor = (0.0, 1.14),
      ncol = 3,
      fontsize = "x-small",
   )
   Plot.grid(
      linestyle = "dotted",
      which = "both",
      axis = "both",
      linewidth = 0.6,
   )
   Plot.savefig(
      name_steady,
      dpi = cc["resolution_image"],
      format = "png"
   )
   Plot.clf()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def draw_transient(catalog):
   cc = custom.give_constant()
   many_curve = []
   many_legend = []

   for parameter in catalog:
      horizon = cc["horizon_transient"] - 1
      curve = []
      aa_up_new = parameter["rr_hat"]
      bb_up_new = 0
      cc_up_new = 0
      aa_down_new = parameter["rr_hat"]
      bb_down_new = 0
      cc_down_new = 0
      up_new = (aa_up_new, bb_up_new, cc_up_new)
      down_new = (aa_down_new, bb_down_new, cc_down_new)
      gap = evaluate_for_gaussian(*up_new, *down_new)
      curve.append(gap)
      up_old = up_new
      down_old = down_new
      horizon -= 1
      while (horizon >= 0):
         tuning = (
            parameter["rr"],
            parameter["pp"],
            parameter["qq"],
            parameter["rho"],
            parameter["eta"],
         )
         aa_up_new = aa_up_original(*tuning)(*up_old)
         bb_up_new = bb_up_original(*tuning)(*up_old)
         cc_up_new = cc_up_original(*tuning)(*up_old)
         aa_down_new = aa_down_original(*tuning)(*down_old)
         bb_down_new = bb_down_original(*tuning)(*down_old)
         cc_down_new = cc_down_original(*tuning)(*down_old)
         up_new = (aa_up_new, bb_up_new, cc_up_new)
         down_new = (aa_down_new, bb_down_new, cc_down_new)
         gap = evaluate_for_gaussian(*up_new, *down_new)
         curve.append(gap)
         up_old = up_new
         down_old = down_new
         horizon -= 1
      many_curve.append(copy.deepcopy(curve))
      many_legend.append("η = {:.3f}".format(parameter["eta"]))

   name_transient = custom.obtain_name_transient(catalog)
   print(
      ">>> plot", catalog[0]["count"],
      "of", catalog[0]["total"],
      ":", name_transient
   )

   array_time = list(range(cc["horizon_transient"]))
   for index in range(len(many_curve)):
      Plot.plot(
         array_time,
         many_curve[index],
         label = many_legend[index % len(many_legend)],
         color = cc["many_color"][index % len(cc["many_color"])],
         linestyle = cc["many_style"][index % len(cc["many_style"])],
         marker = cc["many_marker"][index % len(cc["many_marker"])],
         markersize = cc["size_marker"],
      )

   Plot.xlabel("time index")
   Plot.ylabel("relative gap")
   Plot.title("gap between upper and lower bounds")
   Plot.xscale("log")
   Plot.subplots_adjust(top = 0.75)
   Plot.legend(
      loc = "center left",
      bbox_to_anchor = (0.0, 1.14),
      ncol = 3,
      fontsize = "x-small",
   )
   Plot.grid(
      linestyle = "dotted",
      which = "both",
      axis = "both",
      linewidth = 0.6,
   )
   Plot.savefig(
      name_transient,
      dpi = cc["resolution_image"],
      format = "png"
   )
   Plot.clf()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def evaluate_for_gaussian(aa_up, bb_up, cc_up, aa_down, bb_down, cc_down):
   variance = 1 # without loss of generality under scaling
   mean = 0
   entropy_power = 2 * NP.pi * NP.e * variance
   cost_up = variance * aa_up + mean * bb_up + cc_up
   cost_down = variance * aa_down + entropy_power * bb_down + cc_down
   gap_relative = (cost_up - cost_down) / cost_down
   return gap_relative

def aa_up_original(rr, pp, qq, rho, eta):
   ee = NP.exp(-2 * rho)
   return (
      lambda aa_old, bb_old, cc_old:
      (pp ** 2) * aa_old
      * (((qq ** 2) * ee * aa_old + 1)/ ((qq ** 2) * aa_old + 1)) 
      + rr
   )

def bb_up_original(rr, pp, qq, rho, eta):
   ee = NP.exp(-2 * rho)
   return (
      lambda aa_old, bb_old, cc_old:
      - (pp ** 2) * aa_old
      * (((qq ** 2) * ee * aa_old)/ ((qq ** 2) * aa_old + 1)) 
      + (pp ** 2) * bb_old
      * (((qq ** 2) * ee * aa_old + 1)/ ((qq ** 2) * aa_old + 1)) ** 2
   )

def cc_up_original(rr, pp, qq, rho, eta):
   return (
      lambda aa_old, bb_old, cc_old:
      (eta ** 2) * aa_old
      + cc_old
   )

def aa_down_original(rr, pp, qq, rho, eta):
   return (
      lambda aa_old, bb_old, cc_old:
      (pp ** 2) * aa_old
      * (1/ ((qq ** 2) * aa_old + 1)) 
      + rr
   )

def bb_down_original(rr, pp, qq, rho, eta):
   ee = NP.exp(-2 * rho)
   return (
      lambda aa_old, bb_old, cc_old:
      (1 / (2 * NP.pi * NP.e)) * (pp ** 2) * aa_old
      * (((qq ** 2) * ee * aa_old)/ ((qq ** 2) * aa_old + 1)) 
      + (pp ** 2) * bb_old
      * ee
   )

def cc_down_original(rr, pp, qq, rho, eta):
   return (
      lambda aa_old, bb_old, cc_old:
      (eta ** 2) * aa_old
      + 2 * NP.pi * NP.e * (eta ** 2) * bb_old
      + cc_old
   )

def extract_steady(many_series):
   window = 8
   big = []
   small = []
   for series in many_series:
      big.append(max(series[-window:]))
      small.append(min(series[-window:]))
   bar_up = max(big)
   bar_down = min(small)
   steady = (bar_up + bar_down) / 2
   bar = (bar_up - bar_down) / 2
   return (steady, bar)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
