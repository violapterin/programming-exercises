#! /usr/bin/env python3

import control as ct
import numpy as np
import matplotlib.pyplot as plt

def vehicle_update(t, x, u, params):
   a = params.get('refoffset', 1.5)
   b = params.get('wheelbase', 3.)
   maxsteer = params.get('maxsteer', 0.5)

   delta = np.clip(u[1], -maxsteer, maxsteer)
   alpha = np.arctan2(a * np.tan(delta), b)

   return np.array([
      u[0] * np.cos(x[2] + alpha),
      u[0] * np.sin(x[2] + alpha),
      (u[0] / a) * np.sin(alpha)
   ])

def vehicle_output(t, x, u, params):
   return x

def control_output(t, x, z, params):
   K = params.get('K', np.zeros((2, 3)))
   xd_vec = z[0:3]
   ud_vec = z[3:5]
   x_vec = z[5:8]
   return ud_vec - K @ (x_vec - xd_vec)

vehicle_params={
   'refoffset': 1.5,
   'wheelbase': 3,
   'velocity': 15,
   'maxsteer': 0.5
}
vehicle = ct.NonlinearIOSystem(
   vehicle_update,
   vehicle_output,
   states=3,
   name='vehicle',
   inputs=['v', 'delta'],
   outputs=['x', 'y', 'theta'],
   params=vehicle_params,
)


timepts = np.linspace(0, 10, 1000)
Ud = np.array([10 * np.ones_like(timepts), np.zeros_like(timepts)])
Xd = np.array([10 * timepts, 0 * timepts, np.zeros_like(timepts)])
linsys = vehicle.linearize(Xd[:, 0], Ud[:, 0])
K, S, E = ct.lqr(linsys, np.diag([1, 1, 1]), np.diag([1, 1]))


control = ct.NonlinearIOSystem(
   None,
   control_output,
   name='control',
   inputs=['xd', 'yd', 'thetad', 'vd', 'deltad', 'x', 'y', 'theta'],
   outputs=['v', 'delta'],
   params={'K': K},
)
vehicle_closed = ct.interconnect(
   (vehicle, control),
   inputs=['xd', 'yd', 'thetad', 'vd', 'deltad'],
   outputs=['x', 'y', 'theta'],
)

Xd = np.array([
   10 * timepts + 2 * (timepts-5) * (timepts > 5),
   0.5 * np.sin(timepts * 2*np.pi),
   np.zeros_like(timepts)
])
Ud = np.array([10 * np.ones_like(timepts), np.zeros_like(timepts)])
resp = ct.input_output_response(
   vehicle_closed, timepts, np.vstack((Xd, Ud)), 0)
time, outputs = resp.time, resp.outputs


plt.plot(Xd[0], Xd[1], 'b--')
plt.plot(outputs[0], outputs[1])
plt.xlabel("$x$ [m]")
plt.ylabel("$y$ [m]")
plt.ylim(-1, 2)
plt.legend(['desired', 'actual'], loc='upper left')

rightax = plt.twinx()
rightax.plot(Xd[0, :-1], np.diff(Xd[0]) / np.diff(timepts), 'r--')
rightax.plot(outputs[0, :-1], np.diff(outputs[0]) / np.diff(timepts), 'r-')
rightax.set_ylim(0, 13)
rightax.set_ylabel("$x$ velocity [m/s]")
rightax.yaxis.label.set_color('red')

plt.savefig(
   "test-2.png",
   format = "png"
)