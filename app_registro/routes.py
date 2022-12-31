from app_registro import app
from flask import render_template,request,redirect
import csv
from datetime import date

@app.route("/")
def index():
    #llama al archivo
    fichero = open("data/movimientos.csv","r")
    #accede a cada registro de arhivo y lo formatea
    csvReader = csv.reader(fichero,delimiter=",",quotechar='"')
    #creo un array datos vacio para cargar los registros del archivo
    datos=[]
    #recorrer el objeto csvReader y cargar cada registro al array datos
    for item in csvReader:
        datos.append(item)
    fichero.close()    
    return render_template("index.html",pageTitle="Listas",lista=datos)


@app.route("/new",methods=["GET","POST"])
def create():
    if request.method == "GET":#esto puede ser POST o GET
        return render_template("new.html",pageTitle="Alta",typeAction="Alta",typeButon="Guardar",dataForm={})   
    else:

        error = validateForm(request.form)#validamos los datos de formulario

        if error:
            #hay error
            return render_template("new.html",pageTitle="Alta",typeAction="Alta",typeButon="Guardar",msgError=error,dataForm=request.form, ruta = '/new')
        else: 

           
            mifichero =  open('data/movimientos.csv','a',newline='')
            lectura= csv.writer(mifichero, delimiter=',',quotechar='"')
            
            #crear id
            fichero = open("data/last_id.csv","r")
            registro = fichero.read()
            if registro == "":
                new_id = 1
            else:    
                new_id = int(registro)+1
            
            fichero.close()

            ficheroG = open('data/last_id.csv','w')
            ficheroG.write(str(new_id))
            ficheroG.close()

            lectura.writerow([new_id,request.form['date'],request.form['concept'],request.form['quantity']])    

        mifichero.close()

    return redirect('/')


        
   
@app.route("/update/<int:id>",methods=["GET","POST"])
def edit(id):
    if request.method == "GET":

        mifichero =  open('data/movimientos.csv','r')
        lectura= csv.reader(mifichero, delimiter=',',quotechar='"')
        registro_buscado=[]#len 0
        for registro in lectura:
            if registro[0] == str(id):
                #aqui encuentra el dato
                registro_buscado = registro
        mifichero.close()
        dataForm = {'date':registro_buscado[1], 'concept':registro_buscado[2], 'quantity':registro_buscado[3]}
            
        
        return render_template("update.html",pageTitle="Modificación",typeAction="Modificación",typeButon="Editar",dataForm=dataForm, ruta = '/update/'+str(id)) 
    #return f"este es el id={id} del registro a modificar"
    else:
        registros = []
        mifichero =  open('data/movimientos.csv','r')
        
        lectura= csv.reader(mifichero, delimiter=',',quotechar='"')
        for registro in lectura:
            if registro[0] == str(id):
                registros.append([id,request.form['date'],request.form['concept'],request.form['quantity']])
            else:
                registros.append(registro)
        mifichero_new =  open('data/movimientos.csv','w')
        csvWriter = csv.writer( mifichero_new , delimiter=',',quotechar='"')
        for registro in registros:
            csvWriter.writerow(registro)
            
        mifichero_new.close()
        
        return redirect('/')   
        
@app.route("/delete/<int:id>", methods=["GET","POST"])
def remove(id):

    #1-consultar en data/movimientos.csv y recuperar el registro con id de la peticion
    #2-devolver al formulario html para borrar que los campos no sean modificables
    #3-tendria un boton para confirmar el borrado, si da accion a este boton borrar el registro dado
    if request.method == "GET":

        mifichero =  open('data/movimientos.csv','r')
        lectura= csv.reader(mifichero, delimiter=',',quotechar='"')
        registro_buscado=[]#len 0
        for registro in lectura:
            if registro[0] == str(id):
                #aqui encuentra el dato
                registro_buscado = registro
        mifichero.close()
        #que hacemos si no encuentra registro

        if len(registro_buscado) > 0:
            return render_template("delete.html",pageTitle="Eliminar",registros=registro_buscado)
        else:
           return redirect("/")
    else:#aqui seria post
        #return f"Debemos de borrar el archivo con este id={id}"
        registros = []
        mifichero =  open('data/movimientos.csv','r')
        
        lectura= csv.reader(mifichero, delimiter=',',quotechar='"')
        
        for registro in lectura:
            if registro[0] != str(id):#mientras el id sea distinto del proporcionado para borrar que escriba en fichero
                registros.append(registro)
        mifichero.close()
        mifichero_new =  open('data/movimientos.csv','w')
        csvWriter = csv.writer( mifichero_new , delimiter=',',quotechar='"')
        for registro in registros:
            csvWriter.writerow(registro)
            
        mifichero_new.close()
        
        return redirect('/')
        '''
        fichero_old =  open('data/movimientos.csv','r')
        fichero = open('data/movimientos_new.csv','w',newline="")
        csvReader= csv.reader(fichero_old, delimiter=',',quotechar='"')
        csvWriter = csv.writer( fichero , delimiter=',',quotechar='"')
        for registro in csvReader:
            if registro[0] != str(id):#mientras el id sea distinto del proporcionado para borrar que escriba en fichero
                csvWriter.writerow(registro)
        fichero_old.close()
        fichero.close()    
        return redirect("/")     
        '''




#crear una funcion para validar formulario de registro donde controlemos lo siguiente:
#1-que la fecha no sea mayor a la actual
#2-que el concepto no vaya vacio
#3-que la cantidad sea distinto de 0 y de vacio

def validateForm(requestForm):
    hoy = date.today().isoformat()
    errores=[]
    if requestForm['date'] > hoy:
        errores.append("fecha invalida: La fecha introducida es futura")
    if requestForm['concept'] == "":
        errores.append("concepto vacio: Introduce un concepto para el registro")
    if requestForm['quantity'] == "" or float(requestForm['quantity']) == 0.0:
        errores.append("cantidad vacio o cero: Introduce una cantidad positiva o negativa")   
    return errores