#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, session, request

from cabinet import Cabinet
from rpc import FixedJSONRPC, authenticate, token_urlsafe

app = Flask(__name__)


jsonrpc = FixedJSONRPC(app, '/api/v1', auth_backend=authenticate)

account_id = 'my-name@my-company.com'
password = b'asdfasdf'

name = 'test-vault'
temp_config_path = os.path.join(os.getcwd(), 'test.data', 'secrets')
test_vault_path = os.path.join(os.getcwd(), 'test.data', 'vaults')
cab = Cabinet(account_id, password, temp_config_path)
cab.open(name, test_vault_path)


# Generate a global token. This server will respond only to the process that
# has this token.
token = token_urlsafe(32)


def check_auth(client_token):
    client_token = request.headers.get('token')
    return token == client_token


@jsonrpc.method('App.login(username=str, password=str, vault_path=str) -> str')
def login(username, password, vault_path):
    # TODO: For now, the user and password is not being validated for now.
    session['username'] = username
    session['vault_path'] = vault_path
    session['token'] = token
    return token


@jsonrpc.method('App.get_all')
def get_all():
    return cab.get_all()


@jsonrpc.method('App.get(name=str)')
def get(name):
    return cab.get(name)


@jsonrpc.method('App.add(item=dict)')
def add(item):
    return cab.add(item)


@jsonrpc.method('Cabinet.test', authenticated=check_auth)
def index():
    return u'hello world!'


@jsonrpc.method('App.echo(name=str) -> str', validate=True,
                authenticated=check_auth)
def echo(name='Flask JSON-RPC'):
    return u'Hello {0}'.format(name)


def get_random_open_port():
    # # serve on a random port:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


if __name__ == '__main__':
    app.secret_key = token_urlsafe(32)
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(port=5000, debug=True)  # only localhost, default port

    # port = get_random_open_port()
    # app.run(port=port)
