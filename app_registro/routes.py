from app_registro import app
from flask import render_template


@app.route("/")
def index():
    #prueba de diccionario a vista html
    datos = [
        { 
            'fecha':'18/12/2022',
            'concepto':'Regalo de Reyes',
            'cantidad':-275.50
        },
        { 
            'fecha':'19/12/2022',
            'concepto':'Cobro de Trabajo',
            'cantidad':1200
        },
        { 
            'fecha':'18/12/2022',
            'concepto':'Ropa de Navidad',
            'cantidad':-355.50
        }
    ]
    return render_template("index.html",pageTitle="Listas",lista=datos)

@app.route('/new')
def create():
    return render_template('new.html', pageTitle='Altas')

@app.route('/update')
def edit():
    return render_template('update.html', pageTitle='Modificacion')

@app.route('/delete')
def remove():
     return render_template('delete.html', pageTitle='Eliminar')