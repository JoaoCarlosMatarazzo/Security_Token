from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = 'sua_chave_secreta_aqui'

# Usuários fictícios (Podendo melhorar automatizando com o DB)
users = {
    "user1": "password1",
    "user2": "password2"
}

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token válido por 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return 'Token expirado. Faça login novamente.'
    except jwt.InvalidTokenError:
        return 'Token inválido. Faça login novamente.'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        token = generate_token(username)
        return jsonify({'token': token})

    return jsonify({'message': 'Credenciais inválidas'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if token:
        token = token.split(" ")[1]  
        username = verify_token(token)
        if username:
            return jsonify({'message': f'Olá, {username}! Você acessou uma rota protegida.'})
        else:
            return jsonify({'message': username}), 401 

    return jsonify({'message': 'Token não fornecido'}), 401

if __name__ == '__main__':
    app.run(debug=True)

