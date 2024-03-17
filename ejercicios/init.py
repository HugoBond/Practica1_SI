from __future__ import annotations
import json
import sqlite3

LEGAL_DATA_PATH = '../datos/legal_data_online.json'
USERS_DATA_PATH = '../datos/users_data_online.json'

class ETL:
    def __init__(self) -> None:
        self.connector = sqlite3.connect("etl.db")
        self.cursor = self.connector.cursor()
        
        if self.__create_tables():
            self.__insert_data()
            self.connector.commit()

    
    def __create_tables(self) -> bool:
        """
        Private: Create the tables if they are not created
        """
        query_find_tables = "SELECT name FROM sqlite_master WHERE \
            name='usuarios';"
        res = self.cursor.execute(query_find_tables)
        if res.fetchone() is None:
            # Tabla legal
            self.cursor.execute('''CREATE TABLE legal (
                web TEXT PRIMARY KEY,
                cookies INTEGER,
                aviso INTEGER,
                proteccion_de_datos INTEGER,
                creacion INTEGER
                )''')

            # Tabla usuarios
            self.cursor.execute('''CREATE TABLE usuarios (
                username TEXT PRIMARY KEY,
                telefono INTEGER,
                contrasena TEXT,
                provincia TEXT,
                permisos INTEGER
                )''')

            self.cursor.execute('''CREATE TABLE emails (
                id INTEGER PRIMARY KEY,
                usuario TEXT,
                total INTEGER,
                phishing INTEGER,
                cliclados INTEGER,
                FOREIGN KEY (usuario) REFERENCES usuarios(username)
                )''')

            self.cursor.execute('''CREATE TABLE fechas (
                id INTEGER PRIMARY KEY,
                usuario TEXT,
                fecha TEXT,
                FOREIGN KEY (usuario) REFERENCES usuarios(username)
                )''')

            self.cursor.execute('''CREATE TABLE ips (
                id INTEGER PRIMARY KEY,
                usuario TEXT,
                ip TEXT,
                FOREIGN KEY (usuario) REFERENCES usuarios(username)
                )''')
            return True
        else:
            return False

    def __insert_data(self) -> None:
        """
        Private: Insert the data from the json files
        """
        with open(LEGAL_DATA_PATH, 'r') as legal_data_online:
            legal = json.load(legal_data_online)['legal']

            for item in legal:
                for website, data in item.items():
                    self.cursor.execute('''INSERT INTO legal (web, \
                        cookies, aviso, proteccion_de_datos, creacion)
                        VALUES (?, ?, ?, ?, ?);''',
                        (website, data['cookies'], data['aviso'], \
                         data['proteccion_de_datos'], data['creacion'])
                    )
        
        with open(USERS_DATA_PATH, 'r') as users_data_online:
            users = json.load(users_data_online)['usuarios']
            for item in users:
                for username, data in item.items():
                    self.cursor.execute('''INSERT INTO usuarios (username, \
                        telefono, contrasena, provincia, permisos)
                        VALUES (?, ?, ?, ?, ?);''',
                        (username, data['telefono'], data['contrasena'],
                         data['provincia'], data['permisos'])
                    )

                    self.cursor.execute('''INSERT INTO emails (usuario, \
                        total, phishing, cliclados)
                        VALUES (?, ?, ?, ?);''',
                        (username, data['emails']['total'], \
                         data['emails']['phishing'], \
                         data['emails']['cliclados'])
                    )

                    for fecha in data['fechas']:
                        self.cursor.execute('''INSERT INTO fechas (usuario, \
                            fecha)
                            VALUES (?, ?);''',
                            (username, fecha)
                        )

                    if data['ips'] != "None":
                        for ip in data['ips']:
                            self.cursor.execute('''INSERT INTO ips\
                                (usuario, ip)
                                VALUES (?, ?);''',
                                (username, ip)
                            )

if __name__ == "__main__":
    etl = ETL()

    print(etl.cursor.execute('SELECT emails FROM usuarios;').fetchall())