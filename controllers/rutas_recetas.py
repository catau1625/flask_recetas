from __init__ import app
from flask import render_template,flash,redirect,session,request
from models import receta

@app.route('/show/receta/<int:receta_id>')
def show_receta(receta_id):
    data = {
        "id": receta_id
    }
    receta_info = receta.Receta.show_receta_by_id(data)[0]
    return render_template('show_receta.html',
                           receta_info = receta_info,
                           usuarios_suscritos = receta.Receta.usuarios_suscritos(data))

@app.route('/agregar_receta')
def agregar_receta():
    return render_template('agregar_receta.html')

@app.route('/agregar_receta_process',methods=['POST'])
def agregar_receta_process():
    if not receta.Receta.validacion(request.form):
        return redirect('/agregar_receta')
    data = {
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion'],
        "instruccion": request.form['instruccion'],
        "less_30min": request.form['less_30min']
    }
    receta.Receta.save(data)
    flash('Receta agregada exitosamente','success')
    return redirect('/inicio_sesion')

@app.route('/agregar/like/<int:receta_id>')
def agregar_like(receta_id):
    data = {
        "usuario_id": session['user_id'],
        "receta_id": receta_id
    }
    receta.Receta.agregar_like(data)
    flash('Like agregado','success')
    return redirect('/inicio_sesion')