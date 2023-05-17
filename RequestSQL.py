import mysql.connector
from pyspark.sql import SparkSession
import csv
import random
from pyspark.sql.functions import lit, col, when

import json

class Request_SQL:
    
    DFs = {}
    
    def __init__(self, spark = "temp_spark", files = None, ):
        self.spark = SparkSession.builder.appName(spark).getOrCreate()
        self.read_files(files)
        
        
    def select(self, table, columns='*', where="", join=""):
        
        if columns == "":
            columns = "*"
        ###JOIN NEED ARRAY AND LOOP
        joins = None
        if join != "":
            joins=f"JOIN "+"JOIN ".join([ f"{element} on {table}.id = {element}.id " for element in join])
        if where != "":
            where = f"WHERE {where}"
        
        query = f'''
                SELECT {columns}
                FROM {table} 
                {joins}
                {where}
                '''
        print(query)
        # Exécution d'une requête SQL
        result = self.spark.sql(query)
        print(result.show())

        json_data = []
        for rows in result.toJSON().collect():
            json_data.append(json.loads(rows))

        # Affichage des résultats
        print(json_data)

        return json_data
    
        


    def update(self, table, column, conditon):
                
        updated_df = self.DFs[table].withColumn(f'{column}_updated', conditon.otherwise(col(column)))
        # Mettre à jour la colonne "column" avec les valeurs de la colonne "column_updated"
        updated_df = updated_df.withColumn(column, col(f'{column}_updated'))
        # Supprimer la colonne "column_updated"
        updated_df = updated_df.drop(f'{column}_updated')
        # updated_df.show()
        self.DFs[table] = updated_df
        self.DFs[table].createOrReplaceTempView(table)

    
    def set_DFs(self, file_name):
        # print(self.get_name_file(file_name))
        if "csv" in file_name.split('.')[-1:]:
            self.DFs[self.get_name_file(file_name)] = self.spark.read.csv(f"assets/csv/{self.get_name_file(file_name)}.csv", header=True, inferSchema=True)
            self.DFs[self.get_name_file(file_name)].createOrReplaceTempView(self.get_name_file(file_name))
            
    
    def read_files(self, files):         
        if files is not None:            
            if isinstance(files, list):
                for key, val in enumerate(files):                 
                    self.set_DFs(val)
            else:                            
                self.set_DFs(files)                   
    
    
    #############################
    ########### UTILS ###########
    #############################
    def get_name_file(self, file):
        return file.split('.')[-2:-1:][0].split('/')[-1:][0]
    
    def print_DF(self, name):
        print(self.DFs[name], "\n")
        
    
    def show_DF(self, name, n=50):
        self.DFs[name].show(n=n)
        
    def show_DFs(self,n=50):
        for table in self.DFs:
            self.DFs[table].show(n=n)
                    
    def print_DFs(self):
        for key,  df in self.DFs.items():
            print(df, "\n")
    
    def print_names_DFs(self):
        for df in self.DFs:
            print(df, "\n")
            
    def print_table(self, name):
        print(self.spark.table(name), "\n")
                    
    def print_tables(self):
        for table in self.spark.catalog.listTables():
            print(table, "\n")
            
    def print_name_tables(self):
        return json.dumps(self.spark.catalog.listTables())

    def get_tables_columns(self):
        tables_columns = {}
        for table in self.spark.catalog.listTables():
            table_name = table.name
            columns = [col.name for col in self.spark.catalog.listColumns(table_name)]
            tables_columns[table_name] = columns
        return json.dumps(tables_columns)


                    
    