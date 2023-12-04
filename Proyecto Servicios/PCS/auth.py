from models import User
from functools import wraps
from flask import jsonify,request,render_template

def admin()->bool:
    token = request.cookies.get('token')
    decoded_token = obtenerInfo(token)
    #print(decoded_token)
    data = decoded_token['data']
    id_user = data['admin']
    return id_user

def obtenerInfo(token):
    if token:
        resp = User.decode_auth_token(token)
        user=User.query.filter_by(id=resp['sub']).first()
        if user:
            usuario = {
                'status':'success',
                'data': {
                    'user_id':user.id,
                    'email' : user.email,
                    'admin': user.admin,
                    'registered_on':user.registered_on
                }
            }
            return usuario
    else:
        error =  {
            'status': 'fail',
            'message':resp
        }
        return error

def tokenCheck(f):
    @wraps(f)
    def verificar(*args,**kwargs):
        token = request.cookies.get('token')
        if not token:
            
            return render_template('log.html')
            #jsonify({'message':'Token no encontrado'})
        try:
            info = obtenerInfo(token)
            if info['status']=='fail':
                return render_template('log.html')
                #return jsonify({'message':'Token invalido'})
        except Exception as e:
            print(e)
            #return jsonify({'message':'Error'})
            return render_template('log.html')
        return f(info['data'],*args,**kwargs)
    return verificar

def Verificar(token):
        if not token:
            return jsonify({'message':'Token no encontrado'})
        try:
            info = obtenerInfo(token)
            print(info['status'])
            if info['status']=='fail':
                return jsonify({'message':'Token invalido'})
        except Exception as e:
            print(e)
            return jsonify({'message':'Error'})
        return info