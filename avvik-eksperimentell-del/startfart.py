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
    første = list(map(float, lines[0].strip().split(",")))
    nestførste = list(map(float, lines[1].strip().split(",")))
    speedx = (første[1] - nestførste[1]) / (første[0] - nestførste[0])
    speedy = (første[2] - nestførste[2]) / (første[0] - nestførste[0])
    speed = np.sqrt(speedx**2 + speedy**2)
    data.append(speed)

data = list(map(float, data))

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
