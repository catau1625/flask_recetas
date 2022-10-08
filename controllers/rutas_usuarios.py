from __init__ import app,bcrypt
from flask import render_template,redirect,request,session,flash
from models import usuario
from models import receta

@app.route('/')
def inicio():
    if 'user_id' not in session:
        return render_template('home.html')
    else:
        flash('Ya estas logueado','info')
        return redirect('/inicio_sesion')

@app.route('/process1',methods=['POST'])
def process1():
    if not usuario.Usuario.validacion(request.form):
        return redirect('/')
    elif request.form['password'] == request.form['confirm_password']:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    else:
        flash('Las contraseñas no coinciden','error')
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    usuario.Usuario.save(data)
    flash('Usuario creado correctamente','success')
    return redirect('/')

@app.route('/process2',methods=['POST'])
def process2():
    data = {
        "email": request.form['email']
    }
    user_data = usuario.Usuario.get_user_by_email(data)
    if not user_data:
        flash('Usuario invalido','error')
        return redirect('/')
    if not bcrypt.check_password_hash(user_data[0].password,request.form['password']):
        flash('Email/Contraseña invalidos','error')
        return redirect('/')
    session['user_id'] = user_data[0].id
    session['user_first_name'] = user_data[0].first_name
    session['user_last_name'] = user_data[0].last_name
    session['user_email'] = user_data[0].email
    return redirect('/inicio_sesion')

@app.route('/inicio_sesion')
def inicio_sesion():
    if not 'user_id' in session:
        flash('Debes primero iniciar sesion','error')
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template('user.html',
            nombre = session['user_first_name'],
            apellido = session['user_last_name'],
            user_id = session['user_id'],
            recetas = receta.Receta.show_all(),
            recetas_agregadas = usuario.Usuario.recetas_por_usuario(data))

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    flash('Sesion cerrada','info')
    return redirect('/')

@app.route('/actualizar_datos_usuario')
def actualizar_datos_usuario():
    data = {
        "id": session['user_id']
    }
    user_data = usuario.Usuario.get_user_by_id(data)
    return render_template('actualizar_usuario.html',user_data=user_data[0])
    
@app.route('/actualizar_usuario_process',methods=['POST'])
def actualizar_usuario_process():
    data = {
        "id": session['user_id']
    }
    user_data = usuario.Usuario.get_user_by_id(data)
    if not bcrypt.check_password_hash(user_data[0].password,request.form['password']):
        flash('Contraseña incorrecta','error')
        return redirect('/actualizar_datos_usuario')
    if not usuario.Usuario.validacion(request.form):
        return redirect('/actualizar_datos_usuario')
    new_data = {
        "id": user_data[0].id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
        }
    flash('Informacion actualizada','success')
    usuario.Usuario.update(new_data)
    return redirect('/inicio_sesion')
    