import os
import configparser
from frozenweb.utils import read_text_file


class NotFoundError(Exception):
    def __init__(self, path):
        Exception.__init__(self, path)


class Config:
    def __init__(self, args):
        self.args = args
        self.build_root = os.path.abspath(args.build_folder)
        self.site_root = os.path.abspath(args.site_folder)
        self.template_root = os.path.abspath(args.templates_folder)
        self.context = {}
        if args.context:
            contextpath = os.path.abspath(args.context)
            self.context = eval(read_text_file(contextpath))
        self.server_address = ('0.0.0.0', args.port)

    def root_folder(self):
        return FolderConfig(self.site_root)

    def get_config(self, path):
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:1]
        root = self.root_folder()
        for name in path.split("/"):
            if isinstance(root, FileConfig):
                raise NotFoundError(path)
            root = root.get_child(name)
        if isinstance(root, FolderConfig):
            return root.get_index()
        return root


class FileConfig:
    def __init__(self, path, config):
        if not os.path.exists(path):
            raise NotFoundError(path)
        self.path = path
        self.config = config

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def extension(self):
        return os.path.splitext(self.path)[1]

    def get_bool(self, key):
        fallback = self.config.config.getboolean(self.extension, key, fallback=False)
        return self.config.config.getboolean(self.basename, key, fallback=fallback)

    @property
    def minimise(self):
        return self.get_bool("minimise")

    @property
    def jinja(self):
        return self.get_bool("jinja")


class FolderConfig:
    def __init__(self, path, config_paths=None):
        self.path = path
        self.config_paths = config_paths.copy() if config_paths else []
        self.config = configparser.ConfigParser()

        # read config
        config_path = os.path.join(path, ".frozen")
        if os.path.exists(config_path):
            self.config_paths.append(config_path)
        if self.config_paths:
            self.config.read(self.config_paths)

    @property
    def basename(self):
        return os.path.basename(self.path)

    def iterate(self):
        for name in os.listdir(self.path):
            if name == ".frozen":
                continue
            yield self.get_child(name)

    def get_child(self, name):
        full_path = os.path.join(self.path, name)
        if os.path.isdir(full_path):
            return FolderConfig(full_path, self.config_paths)
        else:
            return FileConfig(full_path, self)

    def get_index(self):
        return FileConfig(os.path.join(self.path, "index.html"), self)
