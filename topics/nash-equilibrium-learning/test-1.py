#! /usr/bin/env python3

import control as ct
import numpy as np
import matplotlib.pyplot as plt


handle_evolution = ct.NonlinearIOSystem(
   lambda tt, xx, uu, table: uu[0],
   lambda tt, xx, uu, table: - uu[0] + 1,
   inputs = 1,
   outputs = 1,
   states = 1,
   name = 'evolution',
)
handle_payoff = ct.NonlinearIOSystem(
   lambda tt, xx, uu, table: uu[0],
   lambda tt, xx, uu, table: xx[0] + uu[0],
   inputs = 1,
   outputs = 1,
   states = 1,
   name = 'payoff',
)
handle_closed = ct.interconnect(
   [handle_evolution, handle_payoff],
   #connections = [
   #   ['evolution.u[0]', 'payoff.y[0]'],
   #   ['payoff.u[0]', 'evolution.y[0]'],
   #],
   inputs = [],
   outputs = ['evolution.y[0]'],
   name = 'closed',
)

# Simulate the system
tt = np.linspace(0, 10, 200)
yy = ct.input_output_response(
   sys = handle_closed,
   T = tt,
   X0 = 0,
)

# Plot the response
plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(tt, yy[0])
plt.savefig(
   "test-1.png",
   format = "png"
)



