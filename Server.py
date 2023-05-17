import json

from flask import Flask, request, render_template, jsonify, redirect
from jinja2 import TemplateNotFound

from RequestSQL import Request_SQL

from pyspark.sql.functions import lit, col, when



data_sql = Request_SQL(spark = "temp_hero_test", files = ["hero.csv", "armor.csv", "weapon.csv"])

class Server:
    def __init__(self ,data_sql, hote='localhost', port=5000):
        self.hote = hote
        self.port = port
        self.app = Flask("cheat spark", template_folder='./front/templates', static_folder='./front/static/')
        # Instanciation de la classe Request_SQL
        self.data = data_sql
        condition = when(col('id') == 18, 18)
        self.data.update('hero','armor', condition)


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
                    #########
                    ###JOIN exemple checbkbox select armor and weapon to hero
                    ### auto checkbox with table selection
                    ### from select with check box in right of legend ? and auto joins hmmm possible
                    ########
                    joins = []
                    table = None

                    str_columns = ', '.join([str(element) for element in columns])

                    # jointures = []
                    # jsonTables = json.loads(self.data.get_tables_columns())
                    # print(jsonTables)
                    # for tbl, clmns in jsonTables.items():
                    #     for clmn in clmns:
                    #         jointures.append(f"{tbl}_{clmn}")
                    # print(jointures)
                    # self.trouver_relations(jsonTables, tables)

                    return jsonify(self.data.select(table, str_columns, where , joins))
                except :
                    return "data not found."


        # @self.app.route('/requete', methods=['POST'])
        # def traiter_requete():
        #     data = request.get_json()
        #     # Traitez ici la requête reçue
        #     return 'Requête traitée avec succès'

    def trouver_relations(self, tables, jointures):
        joins = []  # Liste des jointures

        for i in range(len(jointures) - 1):
            table = jointures[i]
            next_table = jointures[i + 1]

            common_columns = set(tables[table]) & set(tables[next_table])
            if 'id' in common_columns:
                join_condition = f"{next_table}.{table} = {table}.id"
                joins.append(join_condition)

        if joins:
            query = "JOIN " + "\nJOIN ".join(joins) + "\n"

            print("Requête SQL avec jointures :")
            print(query)
        else:
            print("Aucune relation trouvée.")



    def demarrer(self):
        self.app.run(host=self.hote, port=self.port)

server = Server(data_sql)
server.demarrer()
