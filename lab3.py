import numpy as np
import sys

# 'ball' eller 'ring' skal gis som argument!!!
# argument nummer to er ant forsøk gjort

program = sys.argv[1]
observations = int(sys.argv[2])

# Samle data

data = []

for observation in range(observations):
    filename = "målinger/" + program + "/" + str(observation + 1) + ".csv"
    file_object = open(filename, "r")
    lines = file_object.readlines()
    siste = list(map(float, lines[-1].strip().split(",")))
    nestsiste = list(map(float, lines[-2].strip().split(",")))
    speedx = (siste[1] - nestsiste[1]) / (siste[0] - nestsiste[0])
    speedy = (siste[2] - nestsiste[2]) / (siste[0] - nestsiste[0])
    speed = np.sqrt(speedx**2 + speedy**2)
    data.append(speed)

# Regne data

gjennomsnitt = sum(data) / observations

SEE = 0
for i in range(observations):
    SEE += (data[i] - gjennomsnitt)**2

standardavvik = np.sqrt(1 / (observations - 1) * SEE)

standardfeil = standardavvik / np.sqrt(observations)

# Skrive data

print("Gjennomsnitt:", gjennomsnitt)
print("Standardavvik:", standardavvik)
print("Standardfeil:", standardfeil)
