#!/usr/bin/python3

from app import app
from app import socketio

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
