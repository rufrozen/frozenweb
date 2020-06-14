import os
import shutil
import htmlmin
import cssmin
import jsmin
from frozenweb.renderer import Renderer
from frozenweb.utils import read_text_file, read_binary_file, ensure_folder, to_bytes, write_binary_file
from frozenweb.config import FileConfig, FolderConfig


class Builder:
    def __init__(self, config):
        self.config = config
        self.renderer = Renderer(config)

    def render_file(self, config: FileConfig):
        if config.jinja:
            content = self.renderer.render(config.path)
            if config.minimise:
                content = self.minimise(content, config.extension)
            return to_bytes(content)
        elif config.minimise:
            content = read_text_file(config.path)
            content = self.minimise(content, config.extension)
            return to_bytes(content)
        else:
            return read_binary_file(config.path)

    def minimise(self, content, extension):
        if self.config.args.no_minimise:
            return content
        if extension == '.html':
            return htmlmin.minify(
                content,
                remove_comments=True,
                remove_empty_space=True,
                remove_all_empty_space=True,
                remove_optional_attribute_quotes=False,
                keep_pre=True
            )
        elif extension == '.js':
            return jsmin.jsmin(content)
        elif extension == '.css':
            return cssmin.cssmin(content)
        return content

    def target_path(self, config):
        relpath = os.path.relpath(config.path, self.config.site_root)
        return os.path.join(self.config.build_root, relpath)

    def build_file(self, config: FileConfig):
        content = self.render_file(config)
        write_binary_file(self.target_path(config), content)

    def build_folder(self, config: FolderConfig):
        ensure_folder(self.target_path(config))
        for item in config.iterate():
            if isinstance(item, FileConfig):
                self.build_file(item)
            else:
                self.build_folder(item)

    def build(self):
        shutil.rmtree(self.config.build_root, True)
        self.build_folder(self.config.root_folder())
