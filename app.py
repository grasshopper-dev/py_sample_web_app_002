from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage

# load html file.
with open('index.html', mode='r') as f:
    index = f.read()

with open('next.html', mode='r') as f:
    next = f.read()

routes = []

def route(path, method):
    routes.append((path, method))

# add route setting.
route('/', 'index')
route('/index', 'index')
route('/next', 'next')
route('/xml', 'xml')

class HelloServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if (r[0] == _url.path):
                eval('self.' + r[1] + '()')
                break
        else:
            self.error()
        return
    
    def do_POST(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'}
        )
        if 'radio1' in form:
            r1 = form['radio1'].value
        else:
            r1 = 'not selected'

        # res = form['textfield'].value
        res = 'Radio:' + str(r1)
        self.send_response(200)
        self.end_headers()
        html = next.format(
            # message='you typed: ' + res,
            message = res,
            data=form
        )
        self.wfile.write(html.encode('utf-8'))
        return

    # index action
    def index(self):
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title='Hello',
            message='Form送信'
        )
        self.wfile.write(html.encode('utf-8'))
        return
    
    def next(self):
        _url = urlparse(self.path)
        query = parse_qs(_url.query)
        id = query['id'][0]
        password = query['pass'][0]
        msg = 'id=' + id + ', password=' + password
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message=msg,
            data=query
        )
        self.wfile.write(html.encode('utf-8'))
        return
    
    def error(self):
        self.send_error(404, "CANNOT ACCESS!!")
        return
    
    def xml(self):
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <person>
                 <name>Taro</name>
                 <mail>taro@yamada</mail>
                 <age>39</age>
            </person>
            <message>Hello Python!!</message>
        </data>'''
        self.send_response(200)
        self.send_header('Content-Type', 'application/xml; charset=utf-8')
        self.end_headers()
        self.wfile.write(xml.encode('utf-8'))

HTTPServer(('',8000), HelloServerHandler).serve_forever()