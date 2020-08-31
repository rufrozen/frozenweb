import http.server
import mimetypes
from frozenweb.builder import Builder
from frozenweb.config import NotFoundError

mimetypes.init()
mimetypes.types_map["otf"] = "font/otf"
mimetypes.types_map["ttf"] = "font/ttf"
mimetypes.types_map["woff"] = "font/woff"
mimetypes.types_map["woff2"] = "font/woff2"


def find_mimetype(extension):
    if extension in mimetypes.types_map:
        return mimetypes.types_map[extension]
    else:
        return "application/octet-stream"


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.myserver = server.myserver
        super(http.server.BaseHTTPRequestHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        try:
            path = self.path.split("?")[0]
            file_config = self.myserver.config.get_config(path)
            filemime = find_mimetype(file_config.extension)
            content = self.myserver.builder.render_file(file_config)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', filemime)
            self.end_headers()
            self.wfile.write(content)
        except NotFoundError as err:
            self.send_error(404, str(err))


class Server:
    def __init__(self, config):
        self.config = config
        self.builder = Builder(config)

    def base_url(self):
        host, port = self.config.server_address
        return 'http://' + host + ':' + str(port)

    def run(self):
        try:
            print("site_root", self.config.site_root)
            print("template_root", self.config.template_root)
            httpd = http.server.HTTPServer(self.config.server_address, ServerHandler)
            httpd.myserver = self
            print('Started http server: ' + self.base_url())
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('^C received, shutting down server')
