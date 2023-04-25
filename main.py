import cherrypy
import db


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
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
        for i in range(len(lst)):
            return ' \n'.join(map(str, lst))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.config.update({'server.socket_port': 5320})
    cherrypy.quickstart(StringGenerator())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
