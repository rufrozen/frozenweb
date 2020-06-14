from setuptools import setup

setup(
    name='FrozenWeb',
    version='1.0',
    description='Static web server generator',
    author='Igor Timurov',
    author_email='t051200@yandex.ru',
    url='https://rufrozen.com',
    install_requires = ['Jinja2','htmlmin','jsmin','cssmin'],
    packages=['frozenweb']
)
