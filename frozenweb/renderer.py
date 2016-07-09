import os, jinja2
from .utils import *

class Renderer:
	def  __init__(self, config):
		self.config = config
		self.env = jinja2.Environment(loader=jinja2.FunctionLoader(self.load_tpl), cache_size=0)

	def load_tpl(self, template):
		path = os.path.join(self.config.template_root, template)
		source = read_text_file(path)
		return source, path, lambda: False

	def render(self, filepath):
		source = read_text_file(filepath)
		template = self.env.from_string(source)
		return template.render(self.config.context)
