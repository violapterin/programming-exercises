#! /usr/bin/env python3

import os
import sys

from custom import custom

def main():
   mode = sys.argv[1]
   write(name_source = "main-{}.tex".format(mode))
   os.system("rm -f ./main-{}.pdf".format(mode))
   os.system("pdflatex main-{}.tex".format(mode))

def write(name_source):
   os.system("rm -f {}".format(name_source))
   os.system("touch {}".format(name_source))
   handle = open(name_source, "a")
   handle.write(give_string_preamble())
   handle.write(give_string_beginning())
   catalog = custom.give_catalog()
   for parameter in catalog:
      caption = custom.obtain_caption(parameter)
      name_graphics = custom.obtain_name_graphics(parameter)
      handle.write(give_string_subsection(caption))
      handle.write(give_string_graphics(name_graphics))

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
