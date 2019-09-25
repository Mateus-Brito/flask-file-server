from app import create_app
from app.socketio import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, port=5000)