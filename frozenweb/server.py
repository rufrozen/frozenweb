import http.server, mimetypes
from .builder import *
from .utils import *

mimetypes.init();

class ServerHandler(http.server.BaseHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		self.myserver = server.myserver
		super(http.server.BaseHTTPRequestHandler, self).__init__(request, client_address, server)	

	def do_GET(self):
		try:
			filepath = self.find_filepath()
			filemime = self.find_mimetype(filepath)
			content = self.myserver.builder.render_file(filepath)
			self.send_response(200)
			self.send_header('Access-Control-Allow-Origin', '*')
			self.send_header('Content-type', filemime)
			self.end_headers()
			self.wfile.write(content)
		except NotFoundError:
			self.send_error(404)

	def find_mimetype(self, filepath):
		extension = os.path.splitext(filepath)[1]
		if extension in mimetypes.types_map:
			return mimetypes.types_map[extension]
		else:
			return 'application/' + extension[1:]

	def find_filepath(self):
		filepath = os.path.join(self.myserver.config.site_root, self.path[1:])
		if os.path.isdir(filepath):
			filepath = os.path.join(filepath, 'index.html')
		return filepath

class Server:
	def __init__(self, config):
		self.config = config
		self.builder = Builder(config)
		pass

	def base_url(self):
		host, port = self.config.server_address
		return 'http://' + host + ':' + str(port)

	def run(self):
		try:
			print(self.config.site_root)
			print(self.config.template_root)
			httpd = http.server.HTTPServer(self.config.server_address, ServerHandler)
			httpd.myserver = self
			print('Started http server: ' + self.base_url())
			httpd.serve_forever()
		except KeyboardInterrupt:
			print('^C received, shutting down server')
			pass
