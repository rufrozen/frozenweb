import argparse
from frozenweb.builder import Builder
from frozenweb.server import Server
from frozenweb.config import Config


def create_argparser():
    parser = argparse.ArgumentParser(description="Static web server generator")
    parser.add_argument("-s", "--server", action="store_true", help="run http server")
    parser.add_argument("-p", "--port", type=int, default=8000, help="wev server port (default: 80)")
    parser.add_argument("-b", "--build", action="store_true", help="build static site")
    parser.add_argument("--no-minimise", action="store_true", help="skip minimise")
    parser.add_argument("--context", default=None, help="global context file")
    parser.add_argument("--build-folder", default="build", help="set build folder (default: build)")
    parser.add_argument("--templates-folder", default="templates", help="set templates folder (default: templates)")
    parser.add_argument("--site-folder", default="site", help="set site folder (default: site)")
    return parser


def main():
    args = create_argparser().parse_args()
    config = Config(args)
    if args.build:
        Builder(config).build()
    elif args.server:
        Server(config).run()
