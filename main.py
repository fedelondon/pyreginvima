import os

import cherrypy
import db
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('template'))


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
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
        # for i in range(len(lst)):
        #     return ' \n'.join(map(str, lst))
        templ = env.get_template('consulta.html')
        return templ.render(lts=lst)


# Press the green button in the gutter to run the script.
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
    cherrypy.quickstart(StringGenerator(), '/', conf)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
