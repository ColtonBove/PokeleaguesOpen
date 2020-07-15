import os

from app import app
from app import socketio

@app.shell_context_processor
def make_shell_context():
	return {'db': db}

if __name__ == '__main__':
	socketio.run(app)