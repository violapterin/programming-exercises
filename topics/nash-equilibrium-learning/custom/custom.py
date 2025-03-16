
import numpy as NP
import copy

# eta, rho, rr, rr_hat, pp, qq
def give_all_catalog_steady(be_truncated):
   cc = give_constant()
   truncated = cc["truncated_steady"]
   
   #many_eta = array_unsigned(*cc["power_eta"])
   #many_rho = array_unsigned(*cc["power_rho"])
   many_rr = array_unsigned(*cc["power_rr"])
   many_rr_hat = array_unsigned(*cc["power_rr_hat"])
   many_pp = array_signed(*cc["power_pp"])
   many_qq = array_signed(*cc["power_qq"])
   total_section = len(many_qq)
   total_subsection = len(many_pp) * total_section
   total_subsubsection = len(many_rr_hat) * total_subsection
   count_subsubsection = 0
   count_subsection = 0
   count_section = 0

   all_catalog = []
   many_many_catalog = []
   many_catalog = []
   catalog = []
   for qq in many_qq:
      if (be_truncated and count_subsubsection >= truncated):
         break
      count_section += 1
      fact_section = {
         "total": total_section,
         "count": count_section,
         "qq": qq,
      }
      many_many_catalog.append(copy.deepcopy(fact_section))
      for pp in many_pp:
         if (be_truncated and count_subsubsection > truncated):
            break
         count_subsection += 1
         fact_subsection = {
            "total": total_subsection,
            "count": count_subsection,
            "qq": qq,
            "pp": pp,
         }
         many_catalog.append(copy.deepcopy(fact_subsection))
         for rr_hat in many_rr_hat:
            if (be_truncated and count_subsubsection > truncated):
               break
            count_subsubsection += 1
            fact_subsubsection = {
               "total": total_subsubsection,
               "count": count_subsubsection,
               "qq": qq,
               "pp": pp,
               "rr_hat": rr_hat,
            }
            catalog.append(copy.deepcopy(fact_subsubsection))
            for rr in many_rr:
               parameter = {
                  "total": total_subsubsection,
                  "count": count_subsubsection,
                  "qq": qq,
                  "pp": pp,
                  "rr_hat": rr_hat,
                  "rr": rr,
               }
               catalog.append(copy.deepcopy(parameter))
            many_catalog.append(copy.deepcopy(catalog))
            catalog = []
         many_many_catalog.append(copy.deepcopy(many_catalog))
         many_catalog = []
      all_catalog.append(copy.deepcopy(many_many_catalog))
      many_many_catalog = []
   return all_catalog

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# eta, rho, pp, qq, rr, rr_hat
def give_all_catalog_transient(be_truncated):
   cc = give_constant()
   truncated = cc["truncated_transient"]
   
   many_eta = array_unsigned(*cc["power_eta"])
   many_rho = array_unsigned(*cc["power_rho"])
   many_rr = array_unsigned(*cc["power_rr"])[0::2]
   many_rr_hat = array_unsigned(*cc["power_rr_hat"])[0::2]
   many_pp = array_signed(*cc["power_pp"])
   many_qq = array_signed(*cc["power_qq"])
   total_section = len(many_rr_hat) * len(many_rr)
   total_subsection = len(many_pp) * len(many_qq) * total_section
   total_subsubsection = len(many_rho) * total_subsection
   count_subsubsection = 0
   count_subsection = 0
   count_section = 0

   all_catalog = []
   many_many_catalog = []
   many_catalog = []
   catalog = []
   for rr_hat in many_rr_hat:
      for rr in many_rr:
         if (be_truncated and count_subsubsection >= truncated):
            break
         count_section += 1
         fact_section = {
            "total": total_section,
            "count": count_section,
            "rr_hat": rr_hat,
            "rr": rr,
         }
         many_many_catalog.append(copy.deepcopy(fact_section))
         for pp in many_pp:
            for qq in many_qq:
               if (be_truncated and count_subsubsection > truncated):
                  break
               count_subsection += 1
               fact_subsection = {
                  "total": total_subsection,
                  "count": count_subsection,
                  "rr_hat": rr_hat,
                  "rr": rr,
                  "pp": pp,
                  "qq": qq,
               }
               many_catalog.append(copy.deepcopy(fact_subsection))
               for rho in many_rho:
                  if (be_truncated and count_subsubsection > truncated):
                     break
                  count_subsubsection += 1
                  fact_subsubsection = {
                     "total": total_subsubsection,
                     "count": count_subsubsection,
                     "rr_hat": rr_hat,
                     "rr": rr,
                     "pp": pp,
                     "qq": qq,
                     "rho": rho,
                  }
                  catalog.append(copy.deepcopy(fact_subsubsection))
                  for eta in many_eta:
                     parameter = {
                        "total": total_subsubsection,
                        "count": count_subsubsection,
                        "rr_hat": rr_hat,
                        "rr": rr,
                        "pp": pp,
                        "qq": qq,
                        "rho": rho,
                        "eta": eta,
                     }
                     catalog.append(copy.deepcopy(parameter))
                  many_catalog.append(copy.deepcopy(catalog))
                  catalog = []
               many_many_catalog.append(copy.deepcopy(many_catalog))
               many_catalog = []
         all_catalog.append(copy.deepcopy(many_many_catalog))
         many_many_catalog = []
   return all_catalog

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def obtain_name_transient(catalog):
   fact = catalog[0]
   proper = (
      ''
      + "no-{}-".format(str(fact["count"]))
      + "rr-hat-{}-".format(convert_number(fact["rr_hat"]))
      + "rr-{}-".format(convert_number(fact["rr"]))
      + "pp-{}-".format(convert_number(fact["pp"]))
      + "qq-{}-".format(convert_number(fact["qq"]))
      + "rho-{}-".format(convert_number(fact["rho"]))
   )
   proper = proper.replace('.', '-')
   return ("plot/" + proper + "transient" + '.' + "png")

def obtain_caption_transient(catalog):
   fact = catalog[0]
   caption = (
      "figure {}:".format(str(fact["count"])) + ' '
      + "\\("
      + "\\hat{{R}} = {},".format(convert_number(fact["rr_hat"]))
      + "R = {},".format(convert_number(fact["rr"]))
      + "P = {},".format(convert_number(fact["pp"]))
      + "Q = {},".format(convert_number(fact["qq"]))
      + "\\rho = {}".format(convert_number(fact["rho"]))
      + "\\)"
   )
   return caption

def obtain_name_steady(catalog):
   fact = catalog[0]
   proper = (
      ''
      + "no-{}-".format(str(fact["count"]))
      + "qq-{}-".format(convert_number(fact["qq"]))
      + "pp-{}-".format(convert_number(fact["pp"]))
      + "rr-hat-{}-".format(convert_number(fact["rr_hat"]))
   )
   proper = proper.replace('.', '-')
   return ("plot/" + proper + "steady" + '.' + "png")

def obtain_caption_steady(catalog):
   fact = catalog[0]
   caption = (
      "figure {}:".format(str(fact["count"])) + ' '
      + "\\("
      + "Q = {},".format(convert_number(fact["qq"]))
      + "P = {},".format(convert_number(fact["pp"]))
      + "\\hat{{R}} = {}".format(convert_number(fact["rr_hat"]))
      + "\\)"
   )
   return caption

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def array_unsigned(base, min_exponent, max_exponent):
   many_power_unsigned = [
      base ** index
      for index in range(min_exponent, max_exponent + 1)
   ]
   return many_power_unsigned

def array_signed(base, min_exponent, max_exponent):
   many_power_unsigned = array_unsigned(base, min_exponent, max_exponent)
   many_power_signed = (
      [(-1) * value for value in many_power_unsigned]
      + many_power_unsigned
   )
   many_power_signed.sort()
   return many_power_signed

def give_constant():
   constant = {
      "power_eta": (2, -3, 2),
      "power_rho": (2, -4, 2),
      "power_rr": (3, -2, 2),
      "power_rr_hat": (3, -2, 2),
      "power_pp": ((3/2), -2, 2),
      "power_qq": ((3/2), -2, 2),
      # # # # # # # # # # # # # # # #
      "horizon_transient": 36,
      "horizon_steady": 64,
      "resolution_image": 150, # DPI
      "size_marker": 4.8,
      "width_error": 3.2,
      "many_color": ['b', 'r', 'g'],
      "many_style": ['-', '-.', '--', ':'],
      "many_marker": ['s', 'o', 'D', '^', 'P', 'v'],
      # # # # # # # # # # # # # # # #
      "truncated_transient": 24,
      "truncated_steady": 8,
   }
   return constant

def convert_number(number):
   return ("{:.2f}".format(number))

def get_many_flavor(mode):
   many_flavor = {
      "ALL": ["transient", "steady"],
      "TRANSIENT": ["transient"],
      "STEADY": ["steady"],
      "ALL_TEST": ["transient-truncated", "steady-truncated"],
      "TRANSIENT_TEST": ["transient-truncated"],
      "STEADY_TEST": ["steady-truncated"],
   }[mode]
   return many_flavor

