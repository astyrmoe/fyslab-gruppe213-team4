import numpy as np

file_object  = open("sluttfarter.txt", "r")

data=[]

for line in file_object:
    data.append(int(line))

gjennomsnitt=sum(data)/len(data)

sumsum=0
for i in range(len(data)):
    sumsum+=(i-gjennomsnitt)**2

standardavvik=np.sqrt(1/(len(data)-1)*sumsum)

standardfeil=standardavvik/np.sqrt(len(data))

print("Gjennomsnitt: "+str(gjennomsnitt))
print("Standardavvik: "+str(standardavvik))
print("Standardfeil: "+str(standardfeil))