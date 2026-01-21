from pymongo import MongoClient
from pymongo.errors import PyMongoError

class ConexionBD:

    def __init__(self, url: str, user: str, password: str, db_name: str):
        self.url = url
        self.user = user
        self.password = password
        self.db_name = db_name

        uri = f"mongodb://{url}"
        self.client = MongoClient(uri)
        self.db = self.client[self.db_name]

    # -- Funcional -- #
    def crear_coleccion(self, nombre: str):
        if nombre in self.db.list_collection_names():
            return False
        self.db.create_collection(nombre)
        return True
    
    # -- Funciona -- # 
    def insertar_datos(self, coleccion: str, datos: dict):
        if not isinstance(datos, dict):
            raise ValueError("datos debe ser un diccionario")

        try:
            return self.db[coleccion].insert_one(datos).inserted_id
        except PyMongoError as e:
            raise RuntimeError(f"Error insertando datos: {e}")

    # -- Funcional -- #
    def buscar(self, coleccion: str, filtro: dict):
        return list(self.db[coleccion].find(filtro))
    
    # -- Funcional -- #
    def actualizar(self, coleccion: str, filtro: dict, nuevos_valores: dict):
        resultado = self.db[coleccion].update_one(filtro, {"$set": nuevos_valores})
        return resultado.modified_count

    # -- Funcional -- #
    def eliminar(self, coleccion: str, filtro: dict):
        resultado = self.db[coleccion].delete_one(filtro)
        return resultado.deleted_count

    def limite(self, coleccion: str, filtro: dict, limite: int):
        return list(
            self.db[coleccion].find(filtro).limit(limite)
        )
