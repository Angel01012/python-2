from flask import Blueprint,request,jsonify,render_template,redirect
from sqlalchemy import exc
from models import User,Tecnico
from app import db,bcrypt
from auth import tokenCheck,Verificar

appuser=Blueprint('appuser',__name__,template_folder="templates")

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

@appuser.route('/usuarios',methods=['GET'])
@tokenCheck
def getUsers(usuario):
    print(usuario)
    print(usuario['admin'])
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
    print("checkpoint")
    if(request.method=="GET"):
        token = request.args.get('token')
        print(token)
        if token:
            info = Verificar(token)
            print("info:",info)
            if info['status']!="fail":
                responseObject={
                    'status':"success",
                    'message':'valid token',
                    'info':info
                }
                return jsonify(responseObject)
            print("renderiza login")
        return render_template('log.html')
    else:
        email=request.json['email']
        password=request.json['password']
        print(email,password)
        searchUser= User.query.filter_by(email=email).first()
        print(searchUser.id)
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
        print(email,password,nombre,apellido)
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