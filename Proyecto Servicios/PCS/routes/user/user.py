from flask import Blueprint,request,jsonify,render_template,redirect,url_for
from sqlalchemy import exc
from models import User,Tecnico,Images,Rol
from app import db,bcrypt
from auth import tokenCheck,Verificar,admin,obtenerInfo
from forms import userForm
import base64

appuser=Blueprint('appuser',__name__,template_folder="templates")
def render_imagen(data):
    render_img = base64.b64encode(data).decode('ascii')
    return render_img

@appuser.route("/auth/registro",methods=["POST"])
def registro():
    user = request.get_json()
    userExist=User.query.filter_by(email=user['email']).first()
    if not userExist:
        usuario=User(email=user['email'],password=user['password'])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario Creado"
        except exc.SQLAlchemyError as e:
            mensaje="ERROR "+e
    return jsonify({"menssage":mensaje})

@appuser.route('/auth/login',methods=["POST"])
def login():
    user = request.get_json()
    usuario = User (email=user['email'],password=user['password'])
    searchUser=User.query.filter_by(email=usuario.email).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,user["password"])
        if validation:
            auth_token=usuario.enconde_auth_token(user_id=searchUser.id)
            response ={
                'status':'success',
                'message':'Login exitoso',
                'auth_token':auth_token
            }
            return jsonify(response)
    return jsonify({"message":'Datos incorrectos'})

@appuser.route('/addimage',methods=["POST"])
@tokenCheck
def agregar_imagen(data=None):
    token = request.cookies.get('token')
    decoded_token = obtenerInfo(token)
    data = decoded_token['data']
    id_user = data['user_id']
    usuario = User.query.get_or_404(id_user)
    search_image = Images.query.filter_by(user_id=usuario.id).first()
    if search_image:
        print("sis tiene")
        file = request.files['inputFile']
        data = file.read()
        render_file = render_imagen(data)
        search_image.rendered_data = render_file
        search_image.data = data
        image = search_image.rendered_data
        db.session.commit()
        return render_template('config.html',usuario=usuario,image=image)
        #return url_for('appuser.configariones')
    else:
        print("no tiene")
        file = request.files['inputFile']
        data = file.read()
        render_file = render_imagen(data)
        newfile = Images()
        newfile.type = "Perfil"
        newfile.rendered_data = render_file
        newfile.data = data
        image =render_file.rendered_data
        newfile.user_id=usuario.id
        db.session.add(newfile)
        db.session.commit()
        return render_template('config.html',usuario=usuario,image=image)
        #return url_for('appuser.configariones')


@appuser.route('/config',methods=["POST","GET"])
@tokenCheck
def configariones(data=None):
    token = request.cookies.get('token')
    decoded_token = obtenerInfo(token)
    data = decoded_token['data']
    id_user = data['user_id']
    usuario = User.query.get_or_404(id_user)
    search_image = Images.query.filter_by(user_id=usuario.id).first()
    if search_image:
        image = search_image.rendered_data
        return render_template('config.html',usuario=usuario,image=image)
    else:
        return render_template("config.html",usuario=usuario,image={})
    #xd = jsonify({"status": "200"})
    #return xd
    #pass
@appuser.route('/usuarios',methods=['GET'])
@tokenCheck
def getUsers(usuario):

    if usuario['admin']:
        output=[]
        usuarios=User.query.all()
        for usuario in usuarios:
            usuarioData={}
            usuarioData['id']=usuario.id
            usuarioData['email']=usuario.email
            usuarioData['password']=usuario.password
            usuarioData['registered_on']=usuario.registered_on
            output.append(usuarioData)
        return jsonify({'usuarios':output})
    else:
        return jsonify({'error':'no tienes privilegios de administrador'})
    
@appuser.route('/main',methods=["POST","GET"])
@tokenCheck
def main(data=None):
    return render_template('main.html')

@appuser.route('/login',methods=["GET","POST"])
def login_post():
    if(request.method=="GET"):
        token = request.args.get('token')
        if token:
            info = Verificar(token)
            if info['status']!="fail":
                responseObject={
                    'status':"success",
                    'message':'valid token',
                    'info':info
                }
                return jsonify(responseObject)
        return render_template('log.html')
    else:
        email=request.json['email']
        password=request.json['password']
        searchUser= User.query.filter_by(email=email).first()
        usuario=User(email=email,password=password,tecnicoid=searchUser.tecnico_id,rolid=searchUser.rol_id)
        if searchUser:
            validation = bcrypt.check_password_hash(searchUser.password,password)
            if validation:
                auth_token=usuario.encode_auth_token(user_id=searchUser.id)
                responseObject={
                    'status':"success",
                    'login':'Login exitoso',
                    'auth_token':auth_token
                }
                return jsonify(responseObject)
        return jsonify({'message':"Datos incorrectos"})


@appuser.route('/sign',methods=["GET","POST"])
def sing_post():

    if request.method=="GET":
        return render_template('registrar.html')
    else:
        
        email=request.json['email']
        password=request.json['password']
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        tecnico = Tecnico(nombre=nombre,apellido=apellido)
        try:
            pass
            db.session.add(tecnico)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            responseObject={
                'status':'error',
                'message':e
            }
        tecnicoid = Tecnico.query.filter_by(nombre=nombre).first()
        id = tecnicoid.id
        idrol = 1
        usuario=User(email=email,password=password,tecnicoid=id,rolid=idrol)
        userExist=User.query.filter_by(email=email).first()
        if not userExist:
            try:
                db.session.add(usuario)
                db.session.commit()
                responseObject={
                    'status':'success',
                    'message':"registro exitoso"
                }
            except exc.SQLAlchemyError as e:
                responseObject={
                    'status':'error',
                    'message':e
                }
        else:
            responseObject={
                'status':'error',
                'message':'usuario existente'
            }
        return jsonify(responseObject)
    
@appuser.route('/listadousuarios')
@tokenCheck
def listado_usuarios(data=None):
    ad = admin()
    usuarios = User.query.all()
    return render_template('listusuarios.html',usuarios=usuarios,exit=True,admon=ad)

@appuser.route('/agregarusuario',methods=["POST","GET"])
@tokenCheck
def agregar_usuario(data=None):
    ad = admin()
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        adminn = request.form.get('admin')
        tecnico_id = request.form.get('tecnico_id')
        rol_id = request.form.get('rol_id')
        print(rol_id)
        usuario=User(email=email,password=password,tecnicoid=tecnico_id,rolid=rol_id)
        print(usuario)
        userExist=User.query.filter_by(email=email).first()
        if not userExist:
            try:
                
                db.session.add(usuario)
                db.session.commit()
                print('porque?')
            except exc.SQLAlchemyError as e:
                responseObject={
                    'status':'error',
                    'message':e
                }
                print(responseObject)
        else:
            responseObject={
                'status':'error',
                'message':'usuario existente'
            }
            print(responseObject)

        return redirect(url_for('appuser.listado_usuarios'))
    else:
        tecnicos = Tecnico.query.all()
        roles = Rol.query.all()
        return render_template('postusuario.html',roles=roles,tecnicos=tecnicos,exit=True,admon=ad)
    
@appuser.route('/detallesusuario/<int:id>')
@tokenCheck
def detalles_usuario(usuario_data,id):
    ad = admin()
    usuario = User.query.get_or_404(id)
    return render_template('getusuario.html',usuario=usuario,exit=True,admon=ad)

@appuser.route('/modificarusuario/<int:id>',methods=["POST","GET"])
@tokenCheck
def modificar_usuario(usuario_data,id):
    ad = admin()
    usuario = User.query.get_or_404(id)
    roles = Rol.query.all()

    tecnicos = Tecnico.query.all()
    formausuario = userForm(obj=usuario)
    if request.method=="POST":
        formausuario.populate_obj(usuario)
        db.session.commit()
        return redirect(url_for('appuser.listado_usuarios'))
    return render_template('putusuarios.html',roles = roles,usuario = usuario,tecnicos=tecnicos,exit=True,admon=id)