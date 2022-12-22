#lectura de archivos
#with open ('data/movimientos.txt','r') as resultado:
    #leer = resultado.read()
    #print(leer)

#otra manera
#result = open('data/movimientos.txt','r')
#lectura = result.read()
#print(lectura)

import csv
miFichero = open('data/movimientos.txt','r')
miFichero = csv.reader(miFichero,delimiter=',',quotechar='"')

for registros in miFichero:
    print(registros)
    
print('esto es')

