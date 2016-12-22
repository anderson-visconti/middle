import os

path = r'C:\Users\Anderson\Desktop\Gerador Decks'
aqrv = r'vazoesc.dat'

file = open(os.path.join(path,aqrv),'rb')
x = file.read()
print(x)