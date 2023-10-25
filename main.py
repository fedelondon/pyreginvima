import os

import cherrypy
import db
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('template'))

def readf(filename):
    file = open(filename)
    read = file.read()
    return read

class InvimaGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet" type="text/css">
            <title>Consulta codigo invima</title>
          </head>
          <body>
            <form method="get" action="generate">
              <h2>Digite el codigo invima a buscar</h2>
              <input type="text" value="" name="codigo" />
              <button type="submit">buscar</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate(self, codigo):
        query = f"select inventarios_productos.codigo_producto, inventarios_productos.descripcion, inventarios_productos.codigo_invima, medicamentos.codigo_cum from inventarios_productos left join medicamentos on inventarios_productos.codigo_producto = medicamentos.codigo_medicamento where codigo_invima like '%{codigo}%';"

        lst = db.connection_db(query)
        templ = env.get_template('consulta.html')
        return templ.render(lts=lst)


    @cherrypy.expose
    def loadfile(self):
        return open('./template/uploadfile.html')

    @cherrypy.expose
    def store(self, myFile):
      readfile = readf(myFile)
      return readfile
        
        

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.config.update({'server.socket_port': 5320})
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    
    cherrypy.quickstart(InvimaGenerator(), '/', conf)

