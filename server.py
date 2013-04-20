from flask import Flask, request
from player import *

VERSION = "0.1"
DEFAULT_PORT = 5000

server = Flask(__name__)

players = {}

# /: print server info
@server.route('/')
def server_info():
	return 'pyCraftr server version ' + VERSION +	\
				'<br>currently online: ' + ' '.join([key for key in players.keys()])

# /player/login?username=username
@server.route('/player/login')
def player_login():
	username = request.args['username']
	players[username] = Player((0, 0, 0), (0, 0))
	server.logger.info(username + '(' + request.remote_addr + ') has logged in')
	return 'OK'

# /player/logout?username=username
@server.route('/player/logout')
def player_logout():
	username = request.args['username']
	# save player first
	players[username] = None
	server.logger.info(username + '(' + request.remote_addr + ') has disconnected')
	return 'OK'

if __name__ == '__main__':
    server.run(port=DEFAULT_PORT, debug=True)