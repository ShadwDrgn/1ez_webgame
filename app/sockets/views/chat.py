from app import socketio
from flask_socketio import emit, join_room
from flask_login import current_user


@socketio.on('loggedin')
def loggedin(json):
    print('received json: ' + str(json))


@socketio.on('chat')
def chat(json):
    json['data'] = json['data'][:100]
    if current_user.is_authenticated:
        room = 'in'
        json['data'] = current_user.username + ': ' + json['data']
    else:
        json['data'] = 'Guest: ' + json['data']
        room = 'out'
    join_room(room)
    emit('chat', json, room=room)
