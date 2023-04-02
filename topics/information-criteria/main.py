#!/usr/bin/env python3

import matplotlib.pyplot as PL
import numpy as NP

x = NP.linspace(0, 10, 100)
y_1 = 4 + 2 * NP.sin(2 * x)
y_2 = 2 + 3 * NP.sin(4 * x)

PL.plot(x, y_1)
PL.plot(x, y_2)
PL.xlabel("X-axis data")
PL.ylabel("Y-axis data")
PL.title('Information Criteria')
PL.savefig('foo.png', dpi=300)

