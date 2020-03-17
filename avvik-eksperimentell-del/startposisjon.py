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
    data.append(lines[0].strip().split(",")[1])

data = list(map(float, data))

# Regne data

gjennomsnitt = sum(data)/observations

SEE = 0
for i in range(observations):
    SEE += (data[i]-gjennomsnitt)**2

standardavvik = np.sqrt(1/(observations-1)*SEE)
standardfeil = standardavvik / np.sqrt(observations)

# Skrive data

print("Gjennomsnitt:", gjennomsnitt)
print("Standardavvik:", standardavvik)
print("Standardfeil:", standardfeil)
