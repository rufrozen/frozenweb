import os, argparse
from .builder import *
from .server import *

class Config:
	def __init__(self):
		self.build_root = os.path.join(os.getcwd(), 'build')
		self.site_root = os.path.join(os.getcwd(), 'site')
		self.template_root = os.path.join(os.getcwd(), 'templates')
		self.jinja_file = '.jtpl'
		self.ignore = []
		self.context = {}
		self.minimise = True
		self.server_address = ('0.0.0.0', 8000)
		pass

	def parse(self):
		parser = argparse.ArgumentParser(description='Static web server generator')
		parser.add_argument('-s', '--server', action='store_true', help='run http server')
		parser.add_argument('-p', '--port',  default=8000, help='wev server port (default: 80)')
		parser.add_argument('-b', '--build', action='store_true', help='build static site')
		parser.add_argument('-c', '--context',  default=None, help='global context file')
		parser.add_argument('--nominimise', action='store_true', help='do not minimise')
		parser.add_argument('--build_folder', default='build', help='set build folder (default: build)')
		parser.add_argument('--templates_folder', default='templates', help='set templates folder (default: templates)')
		parser.add_argument('--site_folder', default='site', help='set site folder (default: site)')
		parser.add_argument('--jinja', default='.jtpl', help='jinja file extension (default: .jtpl)')
		args = parser.parse_args()

		self.parser = parser
		self.build_root = os.path.join(os.getcwd(), args.build_folder)
		self.site_root = os.path.join(os.getcwd(), args.site_folder)
		self.template_root = os.path.join(os.getcwd(), args.templates_folder)
		self.jinja_file = args.jinja
		if args.nominimise:
			self.minimise = False
		if args.context:
			contextpath = os.path.join(os.getcwd(), args.context)
			self.context = eval(read_text_file(contextpath))
		self.run_server = args.server
		self.run_build = args.build
		self.server_address = ('0.0.0.0', int(args.port))

	def run(self):
		if self.run_build:
			Builder(self).build();
		elif self.run_server:
			Server(self).run();
		else:
			self.parser.print_help()
