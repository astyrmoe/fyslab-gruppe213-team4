import numpy as np
import sys

# 'ball' eller 'ring' skal gis som argument!!!
# argument nummer to er ant forsøk gjort

program=sys.argv[1]
observations=int(sys.argv[2])

# Samle data

data=[]

for observation in range(observations):
    filename="målinger/"+program+"/"+str(observation+1)+".csv"
    file_object=open(filename,"r")
    lines=file_object.readlines()
    siste=lines[-1].strip().split(",")
    nestsiste=lines[-2].strip().split(",")
    speedx=(float(siste[1])-float(nestsiste[1]))/(float(siste[0])-float(nestsiste[0]))
    speedy=(float(siste[2])-float(nestsiste[2]))/(float(siste[0])-float(nestsiste[0]))
    speed=np.sqrt(speedx**2+speedy**2)
    data.append(speed)

# Regne data

gjennomsnitt=sum(data)/observations

sumsum=0
for i in range(observations):
    sumsum+=(i-gjennomsnitt)**2

standardavvik=np.sqrt(1/(observations-1)*sumsum)

standardfeil=standardavvik/np.sqrt(observations)

# Skrive data

print("Gjennomsnitt: "+str(gjennomsnitt))
print("Standardavvik: "+str(standardavvik))
print("Standardfeil: "+str(standardfeil))