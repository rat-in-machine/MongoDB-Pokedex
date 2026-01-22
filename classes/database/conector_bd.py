from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import List, Optional

class ConexionBD:
    """
        Clase que establece conexión con la base de datos y proporciona funciones básicas de MongoDB.
    """
    
    def __init__(self, url: str, user: str, password: str, db_name: str):
        self.url = url
        self.user = user
        self.password = password
        self.db_name = db_name

        uri = f"mongodb://{url}"
        self.client = MongoClient(uri)
        self.db = self.client[self.db_name]

    
    def crear_bd_y_coleccion(self, nombre_bd : str, nombre_coleccion : str, datos : Optional[List[dict]] = None ):
        try:
            db = self.client[nombre_bd]

            if nombre_coleccion not in db.list_collection_names():
                coleccion = db[nombre_coleccion]

                # Documento temporal para forzar la creación real
                resultado = coleccion.insert_one({"_init": True})

                # Limpieza inmediata
                coleccion.delete_one({"_id": resultado.inserted_id})

        except PyMongoError as e:
            raise RuntimeError(f"Error creando base de datos o colección: {e}")
            self.client[nombre_bd]
            pass

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

    # --    Funcional    -- #
    def eliminar(self, coleccion: str, filtro: dict):
        resultado = self.db[coleccion].delete_one(filtro)
        return resultado.deleted_count

    # --  Probar -- #
    def limite(self, coleccion: str, filtro: dict, limite: int):
        return list(
            self.db[coleccion].find(filtro).limit(limite)
        )
