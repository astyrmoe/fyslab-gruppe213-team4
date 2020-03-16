#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from sys import argv

headless = False
saveFile = True
ball = False

for arg in argv[1:]:
    if "=" in argv:
        key, value = arg.split("=", 2)
        if "headless".startswith(key.lower()):
            headless = value[0] in ["t", "1", "y"]
        if "savefile".startswith(key.lower()):
            saveFile = value[0] in ["t", "1", "y"]
        if "ball".startswith(key.lower()):
            ball = value[0] in ["t", "1", "y"]

print(f"[*] headless = {headless}")
print(f"[*] saveFile = {saveFile}")
print(f"[*] ball = {ball}")

# -------------------------------------------------
# Innstillinger:

# --------------------
# Banepunkter:
# Bane fra PDF
y_feste = np.asarray([0.270, 0.230, 0.155, 0.090, 0.100, 0.160, 0.130, 0.150])
# Vår bane
# y_feste = np.asarray([0.262, 0.194, 0.219, 0.142, 0.075, 0.131, 0.093, 0.146])
# Vår bane endre litt slik at ballen ikke letter
# y_feste = np.asarray([0.262, 0.194, 0.219, 0.142, 0.090, 0.131, 0.093, 0.146])
# --------------------

# --------------------
# Type objekt:
# c = 1/2                       # kompakt skive
if ball:
    c = 2/5                     # kompakt kule
else:
    r = 0.0215                  # vår målte indre radius
    R = 0.025                   # vår målte ytre radius
    c = (1 + r**2 / R**2)/2     # ring, r = indre radius, R = ytre radius
# --------------------

# --------------------
# Masse:
# Vekt i oppgave PDF
# M = 0.100
if ball:
    # Vår målte vekt av kule
    M = 0.030
else:
    # Vår målte vekt av ring
    M = 0.0132
# --------------------

# -------------------------------------------------
# Data:
# Tyngdekraft:
g = 9.81

# Punkter
xmin = 0.000
xmax = 1.401
dx = 0.001
x = np.arange(xmin, xmax, dx)   # verdier [0.001, 0.002, 0.003, ..., 1.397, 1.398, 1.399, 1.400]

# Horisontal avstand mellom festepunktene er 200 mm
h = 0.200
x_feste = np.asarray([0, h, 2*h, 3*h, 4*h, 5*h, 6*h, 7*h])

# Generer bane fra punkter
cs = CubicSpline(x_feste, y_feste, bc_type='natural')
# bane
y = cs(x)
# bane derivert
dy = cs(x, 1)
# bane dobbelt derivert
d2y = cs(x, 2)
# ---------------------------------------------------
# Utregninger

# beta = banens helningsvinkel
beta = np.arctan(dy)
beta_deg = np.degrees(beta)     # beta i grader/degrees

# k = banens kruming
k = d2y / (1 + (dy**2))**(3 / 2)

# v = hastighet i hvert punkt
v = np.sqrt((2 * g * (y[0] - y)) / (1 + c))

# a = sentripedalakselerasjon
a = v**2 * k

# N = normalkraft
N = M * (g * np.cos(beta) + a)

# f = statisk friksjonskraft
f = (c * M * g * np.sin(beta)) / (1 + c)
fN = np.abs(f / N)

# v_x = hastighet i x retning
v_x = v * np.cos(beta)

# v_x_mean = 0.5 * (v_x[n-1] + v_x[n]) = parvis gjennomsnitt mellom alle v_x punkter
v_x_mean = (v_x[1:] + v_x[:-1]) / 2

# t_delta = tid objektet har brukt mellom hvert punkt
t_delta = dx / v_x_mean
# bytt ut inf med 0
t_delta[t_delta == np.inf] = 0

# t_x = kummulativ sum = tid objektet brukte til hvert punkt
t_x = np.cumsum(t_delta)

# ---------------------------------------------------
# Plotting:


def fig(title, y, y_unit, x='x', x_unit='m'):
    plt.figure(title, figsize=(12, 6))
    plt.title(title)
    plt.xlabel(f"${x}$ [{x_unit}]", fontsize=20)
    plt.ylabel(f"${y}$ [{y_unit}]", fontsize=20)
    plt.grid()


def plot(x, y, show=True, *args, **kw):
    plt.plot(x, y, *args, **kw)
    plt.plot(x[::200], y[::200], '*', label='festepunkter')
    plt.legend()
    if show and not headless:
        plt.show()


orig_round = round


def round(num, digits=0):
    if digits < 0:
        num *= 10**(-digits)
    num = orig_round(num, digits)
    if digits < 0:
        num /= 10**(-digits)
    if digits <= 0:
        num = int(num)
    return num

# - - -
# Plot banens form


print(f'Start høyde, y[0] = {y[0] * 1000}mm')
print(f'Laveste festepunkt, y[{np.argmin(y_feste)}] = {np.min(y_feste) * 1000}mm')
print(f'Laveste punkt, y({np.argmin(y)}mm) = {round(np.min(y) * 1000)}mm')

fig('Banens form', 'y(x)', 'm')
plt.ylim(0, 0.350)
plot(x, y)

# - - -
# Plot banens helningsvinkel
print()

beta_max = round(np.max(np.abs(np.rad2deg(beta))), 1)
print(f'Banens absolutte helningsvinkel <= {beta_max} grader')

fig('Banens helningsvinkel', 'beta', 'grader')
plot(x, np.rad2deg(beta))

# - - -
# Plot banens krumning
print()

k_min = round(np.min(k))
k_max = round(np.max(k))
kr_min = round(np.min(np.abs(k[200:-200:200])), 3) * 100 	# TODO: Noe virke file her muligens..?
print(f'Banens krumning ligger mellom {k_min} og {k_max} per meter, slikt at minste krumningsradius er {kr_min / 10}cm')

fig('Banens krumning', 'k(x)', '1/m')
plot(x, k)

# - - -
# Plot fartsgrafen
print()

print(f'Maksimal hastighet oppnås ved x = {np.argmax(v) / 1000}m')
print(f'Maksimal fart = {round(np.max(v), 2)} m/s')
print(f'Laveste punkt, y({np.argmin(y)}mm) = {round(np.min(y) * 1000)}mm')

fig('Objektets fartsgraf', 'v', 'm/s')
plot(x, v)

# - - -
# Plot normalkraften
print()

print(f'Laveste normalkraft: {round(np.min(N), 2)}N')
print(f'Største normalkraft: {round(np.max(N), 2)}N')
fig('Normalkraft', 'N', 'N')
plot(x, N)

# - - -
# Plot forholdet mellom friksjonskraft og normalkraft
print()

print(f'Forholdet mellom friksjonskraften f og normalkraften N overstiger ikke verdien {round(np.max(fN), 2)}')

fig('Forholdet mellom friksjonskraft og normalkraft', '|f/N|', '')
plot(x, fN)

# - - -
# Horisontal posisjon som funksjon av tid
print()

print(f'Hele reisen tok ca {round(t_x[-1], 2)} sekunder')

fig('Horisontal posisjon som funksjon av tid', 'x', 'm', 't', 's')
plot(t_x, x[1:])

# - - -
# Plot hastigheten som funksjon av tid
print()

bunnpunkt_n = np.argmin(y)
bunnpunkt_y = round(y[bunnpunkt_n] * 1000)
print(f'Bunnpunktet (x, y) = ({bunnpunkt_n}mm, {bunnpunkt_y}mm) nås etter {round(t_x[bunnpunkt_n], 2)} sekunder')

fig('Hastighet som funksjon av tid', 'v', 'm/s', 't', 's')
plot(t_x, v_x_mean)

if saveFile:
    if ball:
        path = "analyse/ball.numeric.csv"
    else:
        path = "analyse/ring.numeric.csv"
    with open(path, 'w') as f:
        for t, tx, ty in zip(t_x, x, y):
            f.write(f'{t},{tx},{ty}\n')
        print(f'Done writing {path}')
