import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Matriz de carga sismica
SISMO = np.array([
    [11, 0.2262, 0.3598, 0.8705],
    [14, 0.1165, 0.2561, 0.8809],
    [17, 0.2262, 0.3598, 0.8705],
    [20, 0.1165, 0.2561, 0.8809]
])

# Matriz de carga muerta mas carga viva
PDPL = np.array([
    [11, 6.3254, 0.0926, 1.583],
    [14, 6.7403, -0.1768, 1.5337],
    [17, 6.3254, 0.0926, -1.583],
    [20, 6.7403, -0.1768, -1.5337]
])

# Matriz de posiciones
a = np.array([
    [11, 0.4, 0.4],
    [14, 0.4, 4.15],
    [17, 6, 0.4],
    [20, 6, 4.15]
])

# Codigo para el calculo de combinaciones de carga
Co = np.zeros((5, 3 * len(a)))

for PO in range(len(a)):
    # CARGAS sismicas
    PS, MXS, MYS = SISMO[PO, 1:]
    # cargas muertas
    Pm, MXm, MYm = PDPL[PO, 1:]
    # cargas vivas
    Pv, MXv, MYv = 0, 0, 0
    P = Pm + Pv
    MX = MXm + MXv
    MY = MYv + MYm
    # Combinacion de cargas
    Co[:, 0 + 3 * PO] = [P, P + PS, P + PS, P + PS, P + PS]
    Co[:, 1 + 3 * PO] = [MX, MX + MXS, MX - MXS, MX, MX]
    Co[:, 2 + 3 * PO] = [MY, MY, MY, MY + MYS, MY - MYS]

# Codigo para calcular el tamaño de la zapata
DIM = np.zeros((len(a), 3))

plt.figure()
for PO in range(len(a)):
    presion = 20  # presion admisible del suelo en tn/m2
    Bx = 1  # minima dimension de la zapata
    Ly = 1  # minima dimension de la zapata

    for i in range(5):
        vmin = -1
        vmax = np.inf
        for zz in np.arange(0, 3.1, 0.1):
            if vmin < 0 or vmax > presion:
                Bx += zz
                Ly += zz
                # PROPIEDADES
                A = Bx * Ly
                Ixx = Bx * Ly**3 / 12
                Iyy = Ly * Bx**3 / 12
                # VERTICES DEL POLIGONO
                xv = np.array([-Bx/2, Bx/2, Bx/2, -Bx/2])
                yv = np.array([Ly/2, Ly/2, -Ly/2, -Ly/2])
                # IDENTIFICAR LOS PUNTOS QUE CAEN DENTRO DEL POLIGONO
                ja = max(Bx, Ly) / 2
                x = np.arange(-ja, ja + 0.1, 0.1)
                y = x
                X, Y = np.meshgrid(x, y)
                xq = X.flatten()
                yq = Y.flatten()
                in_poly = np.array([Polygon(np.column_stack((xv, yv))).contains_point((xi, yi)) for xi, yi in zip(xq, yq)])
                XL = xq[in_poly]
                YL = yq[in_poly]
                ZL = np.zeros((len(XL), 5))

                P = Co[i, 0 + 3 * PO]
                M2 = Co[i, 1 + 3 * PO]
                M3 = Co[i, 2 + 3 * PO]
                k = P / A + M2 * XL / Iyy + M3 * YL / Ixx
                ZL[:, i] = k
                vmin = k.min()
                vmax = k.max()

    DIM[PO, 1] = Bx
    DIM[PO, 2] = Ly

    x = [a[PO, 1] - Bx/2, a[PO, 1] + Bx/2, a[PO, 1] + Bx/2, a[PO, 1] - Bx/2, a[PO, 1] - Bx/2]
    y = [a[PO, 2] + Ly/2, a[PO, 2] + Ly/2, a[PO, 2] - Ly/2, a[PO, 2] - Ly/2, a[PO, 2] + Ly/2]
    plt.plot(a[:, 1], a[:, 2], 's')
    plt.plot(x, y)
    plt.axis([-5, 40, -5, 100])  # using 100 as a large number instead of np.inf
    plt.text(a[PO, 1], a[PO, 2], f'  {Bx:.1f}x{Ly:.1f}m')

plt.show()

ZL = np.zeros((1681, 5 * len(a)))  # ESTE ES EL PROBLEMA DE DIMENSIONAR

for klk in range(1, 6):
    plt.figure()
    for PO in range(len(a)):
        Bx = DIM[PO, 1]
        Ly = DIM[PO, 2]
        # PROPIEDADES
        A = Bx * Ly
        Ixx = Bx * Ly**3 / 12
        Iyy = Ly * Bx**3 / 12
        # VERTICES DEL POLIGONO
        xv = np.array([-Bx/2, Bx/2, Bx/2, -Bx/2])
        yv = np.array([Ly/2, Ly/2, -Ly/2, -Ly/2])
        # IDENTIFICAR LOS PUNTOS QUE CAEN DENTRO DEL POLIGONO
        ja = max(Bx, Ly) / 2
        JJJ = ja / 20
        x = np.arange(-ja, ja + JJJ, JJJ)
        y = x
        X, Y = np.meshgrid(x, y)
        xq = X.flatten()
        yq = Y.flatten()
        in_poly = np.array([Polygon(np.column_stack((xv, yv))).contains_point((xi, yi)) for xi, yi in zip(xq, yq)])
        XL = xq[in_poly]
        YL = yq[in_poly]

        P = Co[klk - 1, 0 + 3 * PO]
        M2 = Co[klk - 1, 1 + 3 * PO]
        M3 = Co[klk - 1, 2 + 3 * PO]
        k = P / A + M2 * XL / Iyy + M3 * YL / Ixx
        ZL[:, PO + len(a) * (klk - 1)] = k
        vmin = k.min()
        vmax = k.max()

        # PLOT
        plt.plot(xv + a[PO, 1], yv + a[PO, 2], 'k-', linewidth=1)
        plt.scatter(XL + a[PO, 1], YL + a[PO, 2], c=ZL[:, PO + len(a) * (klk - 1)], marker='.')
        plt.colorbar(label='Presion Admisible (Tn/m)')
        plt.view(0, 90)
        plt.axis([-5, 100, -5, 100])  # using 100 as a large number instead of np.inf
        plt.title(f'Comb {klk}\nσ_min = {vmin:.2f} Tn/m\nσ_max = {vmax:.2f} Tn/m')

plt.show()
