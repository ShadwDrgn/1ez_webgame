from app import socketio
from flask_socketio import emit
from flask_login import current_user


@socketio.on('loggedin')
def loggedin(json):
    print('received json: ' + str(json))


@socketio.on('chat')
def chat(json):
    if current_user.is_authenticated:
        json['data'] = current_user.username + ': ' + json['data']
    else:
        json['data'] = 'Guest: ' + json['data']
    emit('chat', json, broadcast=True)
