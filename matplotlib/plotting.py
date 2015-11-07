#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, np.pi*6, np.pi/100)

sin, = plt.plot(x, np.sin(x), label='sin')
cos, = plt.plot(x, np.cos(x), label='cos')
plt.legend(handles=(sin, cos))
plt.show()
