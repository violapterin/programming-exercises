
import numpy as np
import copy


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def find_catalog():
   cc = give_constant()
   be_cut = cc["be_cut"]
   cutoff = cc["cutoff"]
   many_start = [
      np.array([1/2, 1/3, 1/6]),
      np.array([1/2, 1/6, 1/3]),
      np.array([1/3, 1/2, 1/6]),
      np.array([1/3, 1/6, 1/2]),
      np.array([1/6, 1/3, 1/2]),
      np.array([1/6, 1/2, 1/3]),
   ]
   many_rule = ["smith", "brown", "hybrid"]
   #many_alpha = [1.00] # XXX
   #many_gamma = [0.60] # XXX

   many_mu = array_signed(*cc["power_mu"])[0::2]
   many_nu = array_signed(*cc["power_nu"])[0::2]
   many_alpha = array_unsigned(*cc["power_alpha"])[0::2]
   many_gamma = array_unsigned(*cc["power_gamma"])[0::2]
   total = (
      len(many_rule) * len(many_start)
      * len(many_alpha) * len(many_alpha)
      * len(many_mu) * len(many_nu)
   )
   all_catalog = []
   count = 0
   for mu in many_mu:
      for nu in many_nu:
         for gamma in many_gamma:
            many_many_catalog = []
            title = (
               ''
               + "\\("
               + "\\mu = {},".format(convert_number(mu)) + "\\quad" + ' '
               + "\\nu = {},".format(convert_number(nu)) +  "\\quad" + ' '
               + "\\gamma = {},".format(convert_number(gamma)) +  "\\quad" + ' '
               + "\\)"
            )
            many_many_catalog.append(title)
            for start in many_start:
               many_catalog = []
               subtitle = (
                  ''
                  + "\\("
                  + "x_0 = {},".format(convert_array(start)) +  "\\quad" + ' '
                  + "\\)"
               )
               many_catalog.append(subtitle)
               for alpha in many_alpha:
                  catalog = []
                  subsubtitle = (
                     ''
                     + "\\("
                     + "\\alpha = {},".format(convert_number(alpha)) +  "\\quad" + ' '
                     + "\\)"
                  )
                  catalog.append(subsubtitle)
                  for rule in many_rule:
                     count += 1
                     if (be_cut and count > cutoff): break
                     parameter = {
                        "count": count,
                        "total": total,
                        "mu": mu,
                        "nu": nu,
                        "gamma": gamma,
                        "start": start,
                        "alpha": alpha,
                        "rule": rule,
                     }
                     catalog.append(parameter.copy())
                  many_catalog.append(catalog.copy())
               many_many_catalog.append(many_catalog.copy())
            all_catalog.append(many_many_catalog.copy())
   return all_catalog

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

def give_constant():
   constant = {
      "power_mu": (3, -2, 1),
      "power_nu": (3, -2, 1),
      "power_alpha": ((1/2), 1, 2),
      "power_gamma": ((1/2), 1, 2),
      # # # # # # # # # # # # # # # #
      "resolution_image": 150, # DPI
      "size_marker": 4.8,
      "width_error": 3.2,
      "many_color": ['b', 'r', 'g'],
      "many_style": ['-', '-.', '--', ':'],
      "many_marker": ['s', 'o', 'D', '^', 'P', 'v'],
      # # # # # # # # # # # # # # # #
      "horizon": 3,
      "step": 0.1,
      "method_solve": "BDF",
      # RK45: (default) Explicit Runge-Kutta method of order 5(4)
      # RK23: Explicit Runge-Kutta method of order 3(2)
      # DOP853: Explicit Runge-Kutta method of order 8
      # Radau: Implicit Runge-Kutta method of the Radau IIA family of order 5
      # BDF: Implicit multi-step variable-order (1 to 5) method
      # LSODA: Adams/BDF method with automatic stiffness detection and switching
      # # # # # # # # # # # # # # # #
      "be_cut": True,
      "cutoff": 24,
   }
   return constant

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_name_graphics(parameter):
   proper = (
      ''
      + "no-{}-".format(str(parameter["count"]))
      + "mu-{}-".format(convert_number(parameter["mu"]))
      + "nu-{}-".format(convert_number(parameter["nu"]))
      + "gamma-{}-".format(convert_number(parameter["gamma"]))
      + "start-{}-".format(convert_array(parameter["start"]))
      + "alpha-{}-".format(convert_number(parameter["alpha"]))
      + "rule-{}-".format(str(parameter["rule"]))
   )
   proper = proper.replace('.', '-')
   return ("plot/" + proper + '.' + "png")

def get_title(parameter):
   caption = (
      ''
      + "\\("
      + "\\mu = {},".format(convert_number(parameter["mu"])) + "\\quad" + ' '
      + "\\nu = {},".format(convert_number(parameter["nu"])) +  "\\quad" + ' '
      + "\\gamma = {},".format(convert_number(parameter["gamma"])) +  "\\quad" + ' '
      + "\\)"
   )
   return caption

def get_subtitle(parameter):
   caption = (
      ''
      # + "figure {}:".format(str(parameter["count"])) + ' '
      + "\\("
      + "x_0 = {},".format(convert_array(parameter["start"])) +  "\\quad" + ' '
      + "\\)"
   )
   return caption

def get_subsubtitle(parameter):
   caption = (
      ''
      + "\\alpha = {},".format(convert_number(parameter["alpha"])) +  "\\quad" + ' '
      + "\\mathrm{{rule}} \; \\mathrm{{{}}}".format(parameter["rule"])
   )
   return caption

def get_caption(parameter):
   caption = (
      ''
      + "figure {}:".format(str(parameter["count"])) + ' '
      + "\\("
      + "\\mu = {},".format(convert_number(parameter["mu"])) + "\\quad" + ' '
      + "\\nu = {},".format(convert_number(parameter["nu"])) +  "\\quad" + ' '
      + "\\gamma = {},".format(convert_number(parameter["gamma"])) +  "\\quad" + ' '
      + "x_0 = {},".format(convert_array(parameter["start"])) +  "\\quad" + ' '
      + "\\alpha = {},".format(convert_number(parameter["alpha"])) +  "\\quad" + ' '
      + "\\mathrm{{rule}} \; \\mathrm{{{}}}".format(parameter["rule"])
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

def convert_array(array):
   result = ""
   result += "("
   for item in array:
      result += convert_number(item)
      result += ","
   result = result[:-1]
   result += ")"
   return result

def convert_number(number):
   return ("{:.2f}".format(number))


