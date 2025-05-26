#! /usr/bin/env python3

import os

from custom import custom

mode = "ALL"
#mode = "TRANSIENT"
#mode = "STEADY"
#mode = "ALL_TEST"
#mode = "TRANSIENT_TEST"
#mode = "STEADY_TEST"

os.system("rm -rf ./{}".format("plot"))
os.system("mkdir {}".format("plot"))
os.system("python3 ./draw.py {}".format(mode))

os.system("rm -f ./*.aux")
os.system("rm -f ./*.log")
os.system("python3 ./write.py {}".format(mode))
