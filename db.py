import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

class DB():
    def __init__(self):
        self.path_db = 'db-com.db'
        self.conn = sqlite3.connect(self.path_db)
        self.cursor = self.conn.cursor()
        
    def createConnection(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.path_db)

        if not db.open():
            QMessageBox.warning(self, 'PyQt5 APP', 
                'Error:{}'.format(db.lastError().text()))
            sys.exit(1)

    def add_oid(self, name, value, id_model):
        self.cursor.execute(f"INSERT INTO OIDs (name_OID, OID, id_model) VALUES ('{name}', '{value}', '{id_model}')")
        self.conn.commit()
        
    def get_list_models_devices(self):
        models = self.cursor.execute("SELECT model_name FROM Model").fetchall()
        return models

    def get_list_devices(self):
        names = self.cursor.execute("SELECT name FROM Device").fetchall()
        return names

    def get_name_models_devices(self):
        name_models = self.cursor.execute("SELECT id_model FROM Device").fetchall()
        list_names = []
        for i in name_models:
            index = i[0]
            list_names.append(self.cursor.execute(f"SELECT model_name FROM Model WHERE id = '{index}'").fetchone())
        return list_names

    def get_ip_device(self, id_device):
        ip_device = self.cursor.execute(f"SELECT IP FROM Device WHERE id_device = '{id_device}'").fetchone()
        return ip_device

    def get_id_devices(self):
        id_devices = self.cursor.execute("SELECT id_device FROM Device").fetchall()
        return id_devices

    def get_names_oids(self, id_model):
        names_oids = self.cursor.execute(f"SELECT name_OID FROM OIDs WHERE id_model = '{id_model}'").fetchall()
        return names_oids
    
    def get_oids(self, id_model):
        data = self.cursor.execute(f"SELECT OID FROM OIDs WHERE id_model = '{id_model}'").fetchall()
        return data

    def get_id_models(self):
        data = self.cursor.execute(f"SELECT id FROM Model").fetchall()
        return data

    def get_id_model_device(self, id_device):
        id_model = self.cursor.execute(f"SELECT id_model FROM Device WHERE id_device = '{id_device}'").fetchone()
        return id_model

    def delete_model(self, id_model):
        self.cursor.execute(f"DELETE FROM Device WHERE id_model = '{id_model}'")
        self.cursor.execute(f"DELETE FROM OIDs WHERE id_model = '{id_model}'")
        self.cursor.execute(f"DELETE FROM Model WHERE id = '{id_model}'")
        self.conn.commit()

