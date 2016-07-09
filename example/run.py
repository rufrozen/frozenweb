import os, sys

# for testing frozenweb without install
sys.path.insert(1, '..')
from frozenweb import *

config = Config()
config.context = {
	'test_int': 123,
	'test_str': 'hello',
}

server = Server(config)
builder = Builder(config)

if __name__ == "__main__":
	builder.build()
	server.run()
	pass