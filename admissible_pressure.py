import matplotlib
import numpy as np
#matplotlib.use("module://matplotlib.backends.html5_canvas_backend")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
from shapely.geometry import Polygon, Point
from matplotlib.patches import Polygon as mpl_polygon

# Example values for variables
p1, p2, p3, p4, p5 = 1, 2, 3, 4, 5
va1, va2, va3 = 10, 15, 20
va4, va5, va6 = 25, 30, 35
va7, va8, va9 = 40, 45, 50
va10, va11, va12 = 55, 60, 65
va13, va14, va15 = 70, 75, 80

A = 100
Ixx = 2000
Iyy = 3000

# Create load matrix
Mload = np.zeros((3, 6))
Mload[:, p1 - 1] = [va1, va2, va3]
Mload[:, p2 - 1] = [va4, va5, va6]
Mload[:, p3 - 1] = [va7, va8, va9]
Mload[:, p4 - 1] = [va10, va11, va12]
Mload[:, p5 - 1] = [va13, va14, va15]
Mload = Mload[:, 1:6]

# Load types
Pm = Mload[0, 0]
MXm = Mload[1, 0]
MYm = Mload[2, 0]
Pv = Mload[0, 1]
MXv = Mload[1, 1]
MYv = Mload[2, 1]
PS = Mload[0, 2]
MXS = Mload[1, 2]
MYS = Mload[2, 2]

P = Pm + Pv
MX = MXm + MXv
MY = MYm + MYv

# Load combinations
Co = np.array([
    [Pm + Pv, MXm + MXv, MYm + MYv, P, MX, MY],
    [Pm + 0.7 * PS, MXm + 0.7 * MXS, MYm, P + PS, MX + MXS, MY],
    [Pm + 0.7 * PS, MXm - 0.7 * MXS, MYm, P + PS, MX - MXS, MY],
    [Pm + 0.7 * PS, MXm, MYm + 0.7 * MYS, P + PS, MX, MY + MYS],
    [Pm + 0.7 * PS, MXm, MYm - 0.7 * MYS, P + PS, MX, MY - MYS],
    [Pm + 0.75 * Pv + 0.7 * 0.75 * PS, MXm + 0.75 * MXv + 0.7 * 0.75 * MXS, MYm + 0.75 * MYv, 0, 0, 0],
    [Pm + 0.75 * Pv + 0.7 * 0.75 * PS, MXm + 0.75 * MXv - 0.7 * 0.75 * MXS, MYm + 0.75 * MYv, 0, 0, 0],
    [Pm + 0.75 * Pv + 0.7 * 0.75 * PS, MXm + 0.75 * MXv, MYm + 0.75 * MYv + 0.7 * 0.75 * MYS, 0, 0, 0],
    [Pm + 0.75 * Pv + 0.7 * 0.75 * PS, MXm + 0.75 * MXv, MYm + 0.75 * MYv - 0.7 * 0.75 * MYS, 0, 0, 0],
    [0.6 * Pm + 0.7 * PS, 0.6 * MXm, 0.6 * MYm + 0.7 * MYS, 0, 0, 0],
    [0.6 * Pm + 0.7 * PS, 0.6 * MXm, 0.6 * MYm - 0.7 * MYS, 0, 0, 0]
])

# Polygon vertices
xv = np.array([-1.285, 1.215, 1.215, -1.285, -1.285])
yv = np.array([-4.49, -4.49, 4.49, 4.49, -4.49])
polygon = Polygon(zip(xv, yv))
limit = max(max(abs(xv)), max(abs(yv)))

# Create grid
x = np.arange(-limit, limit + 0.1, 0.1)
y = x
X, Y = np.meshgrid(x, y)
points = np.vstack([X.ravel(), Y.ravel()]).T
inside_polygon = np.array([polygon.contains(Point(p)) for p in points])
XL = points[inside_polygon, 0]
YL = points[inside_polygon, 1]

# Plotting
fig, axs = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
axs = axs.flatten()

for i in range(6):
    P, M2, M3 = Co[i, :3]
    k = P / A + M2 * XL / Iyy + M3 * YL / Ixx
    vmin, vmax = np.min(k), np.max(k)

    sc = axs[i].scatter(XL, YL, c=k, cmap='viridis', s=5)
    axs[i].add_patch(mpl_polygon(list(zip(xv, yv)), closed=True, fill=False, edgecolor='k'))
    axs[i].set_title(f'Comb {i + 1}\nσ_min = {vmin:.2f} Tn/m\nσ_max = {vmax:.2f} Tn/m')
    axs[i].set_xlim([min(xv) - 0.5, max(xv) + 0.5])
    axs[i].set_ylim([min(yv) - 0.5, max(yv) + 0.5])
    axs[i].set_aspect('equal', 'box')

fig.colorbar(sc, ax=axs, orientation='horizontal', pad=0.1, label='Admissible Pressure (Tn/m)')
plt.show()

# Plotting for combinations 7 to 11
fig, axs = plt.subplots(2, 3, figsize=(18, 10), constrained_layout=True)
axs = axs.flatten()

for i in range(6, 11):
    P, M2, M3 = Co[i, :3]
    k = P / A + M2 * XL / Iyy + M3 * YL / Ixx
    vmin, vmax = np.min(k), np.max(k)

    sc = axs[i - 6].scatter(XL, YL, c=k, cmap='viridis', s=5)
    axs[i - 6].add_patch(mpl_polygon(list(zip(xv, yv)), closed=True, fill=False, edgecolor='k'))
    axs[i - 6].set_title(f'Comb {i + 1}\nσ_min = {vmin:.2f} Tn/m\nσ_max = {vmax:.2f} Tn/m')
    axs[i - 6].set_xlim([min(xv) - 0.5, max(xv) + 0.5])
    axs[i - 6].set_ylim([min(yv) - 0.5, max(yv) + 0.5])
    axs[i - 6].set_aspect('equal', 'box')

fig.colorbar(sc, ax=axs, orientation='horizontal', pad=0.1, label='Admissible Pressure (Tn/m)')
plt.show()
