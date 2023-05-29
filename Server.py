import json

from flask import Flask, request, render_template, jsonify, redirect

from jinja2 import TemplateNotFound

from RequestSQL import Request_SQL

from pyspark.sql.functions import lit, col, when

data_sql = Request_SQL(spark="temp_hero_test", files=["hero.csv", "armor.csv", "weapon.csv"])


class Server:
    def __init__(self, data_sql, hote='localhost', port=5000):
        self.hote = hote
        self.port = port
        self.app = Flask("cheat spark", template_folder='./front/templates', static_folder='./front/static/')
        self.app.debug = True
        # Instanciation de la classe Request_SQL
        self.data = data_sql

        @self.app.route('/', methods=['GET', 'POST'])
        def accueil():
            if request.method == "GET":
                # If the request method is GET, render the sign_up.html template
                try:
                    return render_template("index.html")
                except TemplateNotFound:
                    return "Template not found."

        @self.app.route('/select_data', methods=['GET', 'POST'])
        def select_data():
            if request.method == "GET":
                # If the request method is GET, render the sign_up.html template
                try:
                    json_to_send = self.data.get_tables_columns()
                    return render_template("select_form.html", data=json.loads(json_to_send))
                except TemplateNotFound:
                    return "Template not found."
            if request.method == "POST":
                try:
                    selected_tables = [key for key in request.form.keys() if 'tables' in key]
                    tables = []
                    columns = []
                    for table in selected_tables:
                        table_name = table.split('-')[-1:][0].replace("[]", "")
                        tables.append(table_name)
                        for column in request.form.getlist(table):
                            columns.append(f"{table_name}.{column} as {table_name}_{column}")

                    where = request.form['where']
                    joins = json.loads(self.data.get_tables_columns())



                    return jsonify(self.data.select(columns, tables, joins, where))
                except:
                    return "data not found."

        # @self.app.route('/requete', methods=['POST'])
        # def traiter_requete():
        #     data = request.get_json()
        #     # Traitez ici la requête reçue
        #     return 'Requête traitée avec succès'

        @self.app.route('/get_tables', methods=['GET'])
        def get_tables():
            # Traitez ici la requête reçue
            return jsonify(self.data.get_tables())

        @self.app.route('/add_csv', methods=['GET'])
        def add_csv():
            # Traitez ici la requête reçue
            return render_template("add_csv.html")

        @self.app.route('/upload', methods=['POST'])
        def upload():
            files = request.files.getlist('file')
            for file in files:
                file.save('assets/csv/' + file.filename)
            # Effectuez ici d'autres opérations avec les fichiers si nécessaire

            return 'Fichiers téléchargés et traités avec succès'
    def demarrer(self):
        self.app.run(host=self.hote, port=self.port)


server = Server(data_sql)
server.demarrer()


