import os, shutil, jsmin, htmlmin, cssmin
from .renderer import *
from .utils import *

class NotFoundError(Exception):
    pass

class Builder:
	def __init__(self, config):
		self.config = config
		self.renderer = Renderer(config)

	def render_file(self, filepath):
		if os.path.exists(filepath):
			if self.need_minimise(filepath):
				return to_bytes(self.minimise(read_text_file(filepath)))
			else:
				return read_binary_file(filepath)
		jtplpath = filepath + self.myserver.config.jinja_file
		if os.path.exists(jtplpath):
			content = self.renderer.render(jtplpath)
			return to_bytes(self.minimise(content))
		raise NotFoundError

	def need_minimise(self, filepath):
		if not self.config.minimise: return False
		if filepath.endswith('.html'): return True
		if filepath.endswith('.js'): return True
		if filepath.endswith('.css'): return True
		return False

	def minimise(self, content, filepath):
		if not self.config.minimise: 
			return content
		if filepath.endswith('.html'):
			return htmlmin.minify(content, 
				remove_comments = True, 
				remove_empty_space = True, 
				remove_all_empty_space = True, 
				remove_optional_attribute_quotes = False,
				keep_pre = True
			)
		elif filepath.endswith('.js'):
			return jsmin.jsmin(content)
		elif filepath.endswith('.css'):
			return cssmin.cssmin(content)
		return content

	def build_file(self, filepath):
		src_file = os.path.join(self.config.site_root, filepath)
		dst_file = os.path.join(self.config.build_root, filepath)
		ensure_folder(os.path.dirname(dst_file))
		if src_file.endswith(self.config.jinja_file):
			dst_file = dst_file[:-len(self.config.jinja_file)]
			content = self.renderer.render(src_file)
			content = self.minimise(content, dst_file)
			write_binary_file(dst_file, to_bytes(content))
		elif self.need_minimise(dst_file):
			content = read_text_file(src_file)
			content = self.minimise(content, dst_file)
			write_binary_file(dst_file, to_bytes(content))
		else:
			shutil.copy(src_file, dst_file)

	def build(self):
		shutil.rmtree(self.config.build_root, True)
		for filepath in allfiles(self.config.site_root):
			print(filepath)
			self.build_file(filepath)