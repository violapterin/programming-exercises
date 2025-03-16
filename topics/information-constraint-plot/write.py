#! /usr/bin/env python3

import os
import sys

from custom import custom

def main():
   mode = sys.argv[1]
   many_flavor = custom.get_many_flavor(mode)
   for flavor in many_flavor:
      be_truncated = flavor.endswith("truncated")
      if (flavor.startswith("transient")):
         write_transient(
            be_truncated = be_truncated,
            name_source = "main-{}.tex".format(flavor)
         )
      if (flavor.startswith("steady")):
         write_steady(
            be_truncated = be_truncated,
            name_source = "main-{}.tex".format(flavor)
         )
      os.system("rm -f ./main-{}.pdf".format(flavor))
      os.system("pdflatex main-{}.tex".format(flavor))

def write_steady(be_truncated, name_source):
   os.system("rm -f {}".format(name_source))
   os.system("touch {}".format(name_source))
   handle = open(name_source, "a")
   handle.write(give_string_preamble())
   handle.write(give_string_beginning())
   all_catalog = custom.give_all_catalog_steady(be_truncated)

   for many_many_catalog in all_catalog:
      fact_section = many_many_catalog[0]
      title_section = (
         "\\("
         + "Q = {:.2f}".format(fact_section["qq"])
         + "\\)"
      )
      handle.write(give_string_section(title_section))
      many_many_catalog.pop(0)
      for many_catalog in many_many_catalog:
         fact_subsection = many_catalog[0]
         title_subsection = (
            "\\("
            + "P = {:.2f}".format(fact_subsection["pp"])
            + "\\)"
         )
         handle.write(give_string_subsection(title_subsection))
         many_catalog.pop(0)
         for catalog in many_catalog:
            fact_subsubsection = catalog[0]
            title_subsubsection = (
               "\\("
               + "\\hat{{R}} = {:.2f}".format(fact_subsubsection["rr_hat"])
               + "\\)"
            )
            handle.write(give_string_subsubsection(title_subsubsection))
            caption_plot = custom.obtain_caption_steady(catalog)
            handle.write(caption_plot)
            name_steady = custom.obtain_name_steady(catalog)
            handle.write(give_string_graphics(name_steady))

   handle.write(give_string_ending())
   handle.close()

def write_transient(be_truncated, name_source):
   os.system("rm -f {}".format(name_source))
   os.system("touch {}".format(name_source))
   handle = open(name_source, "a")
   handle.write(give_string_preamble())
   handle.write(give_string_beginning())
   all_catalog = custom.give_all_catalog_transient(be_truncated)

   for many_many_catalog in all_catalog:
      fact_section = many_many_catalog[0]
      title_section = (
         "\\("
         + "\\hat{{R}} = {:.2f},".format(fact_section["rr_hat"])
         + "rr = {:.2f}".format(fact_section["rr"])
         + "\\)"
      )
      handle.write(give_string_section(title_section))
      many_many_catalog.pop(0)
      for many_catalog in many_many_catalog:
         fact_subsection = many_catalog[0]
         title_subsection = (
            "\\("
            + "P = {:.2f},".format(fact_subsection["pp"])
            + "Q = {:.2f}".format(fact_subsection["qq"])
            + "\\)"
         )
         handle.write(give_string_subsection(title_subsection))
         many_catalog.pop(0)
         for catalog in many_catalog:
            fact_subsubsection = catalog[0]
            title_subsubsection = (
               "\\("
               + "\\rho = {:.2f}".format(fact_subsubsection["rho"])
               + "\\)"
            )
            handle.write(give_string_subsubsection(title_subsubsection))
            caption_plot = custom.obtain_caption_transient(catalog)
            handle.write(caption_plot)
            name_transient = custom.obtain_name_transient(catalog)
            handle.write(give_string_graphics(name_transient))

   handle.write(give_string_ending())
   handle.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def give_string_preamble():
   result = """%
   \\documentclass[a4paper]{article}
   %
   \\usepackage[utf8]{inputenc}
   \\usepackage{amsmath}
   \\usepackage{amsthm}
   \\usepackage{amssymb}
   \\usepackage{mathrsfs}
   \\usepackage{graphicx}
   \\usepackage{float}
   \\usepackage{color}
   \\usepackage{multicol}
   \\usepackage[
      left = 1.40cm,
      right = 1.40cm,
      top = 1.80cm,
      bottom = 1.80cm
   ]{geometry}
   %
   \\title{Plots on bounds for linear quadratic Gaussian
   control with information constraints}
   \\author{Tzuyu Jeng}
   \\date{\\today}
   %
   \n"""
   return result

def give_string_beginning():
   result = """%
   \\begin{document}
      \\maketitle
      \\begin{multicols*}{2}
   %
   \n"""
   return result

def give_string_ending():
   result = """%
   \\end{multicols*}
   \\end{document}
   %
   \n"""
   return result

def give_string_section(name_section):
   result = """
   \\section{{{}}}
   %
   \n""".format(name_section)
   return result

def give_string_subsection(name_section):
   result = """
   \\subsection{{{}}}
   %
   \n""".format(name_section)
   return result

def give_string_subsubsection(name_section):
   result = """
   \\subsubsection{{{}}}
   %
   \n""".format(name_section)
   return result

def give_string_graphics(name_graphics):
   result = """
   \\begin{{figure}}[H]
   \\centering
   \\includegraphics[width=0.92\\linewidth]{{{}}}
   \\end{{figure}}
   %
   \n""".format(name_graphics)
   return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

main()
