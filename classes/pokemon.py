from .database.conector_bd import ConexionBD
from dataclasses import dataclass, asdict  
from typing import List, Optional

#----------------------#
# ESTRUCTURAS DE DATOS #
#----------------------#

@dataclass # Etiqueta de estructura de datos.
class Ataque:
    """ 
    Representa un ataque capaz de ser efectuado por un Pokemon 
    
    Attributes:
        nombre (str):   Nombre del ataque.
        tipo (str):     Elemento del ataque.
    """
    nombre: str
    tipo: str

@dataclass # Etiqueta de estructura de datos.
class Pokemon:
    """
    Representa un Pokemon del set de datos.
    
    Attributes:
        nombre (str):                       Nombre del Pokemon.
        region (str):                       Región en la que habita el Pokemon.
        pokedex_nacional (int):             Número de registro en la pokedex.
        tipo_primario (str):                Elemento principal del Pokemon.
        tipo_secundario (Optional[str])     Elemento secundario del Pokemon.
        nivel (int):                        Nivel del Pokemon.
        ataques (Optional[List[Ataque]])    Ataques disponibles.
    """
    
    nombre: str
    region: str
    pokedex_nacional: int
    tipo_primario: str
    tipo_secundario: Optional[str] = None
    nivel: int = 1
    ataques: Optional[List[Ataque]] = None

class PokemonDAO:
    """
    Objeto de acceso a datos (DAO) para la colección de Pokémon en MongoDB.
    
    Esta clase encapsula todas las operaciones CRUD relacionadas con Pokémon,
    aislando la lógica de persistencia del resto de la aplicación.
    """
    
    def __init__(self, conexion : ConexionBD):
        """
        Inicializa el DAO con la conexión a MongoDB.
        
        :param conexion: Instancia de la clase de conexión a la base de datos.
        """
        self.conexion = conexion
        self.coleccion = "Pokemon"

    def insertar(self, pokemon: Pokemon):
        """
        Inserta un Pokémon en la colección
        
        :param pokemon: Pokemon a insertar.
        """
        
        datos = asdict(pokemon)                                                 # "asdict", permite convertir un dataclass en un diccionario. 
        
        if datos["ataques"]:
            datos["ataques"] = [asdict(a) for a in (pokemon.ataques or [])]     # Convierto los dataclasses 'Ataque' a diccionarios.
        
        return self.conexion.insertar_datos(self.coleccion, datos)              # Inserto los datos dentro de la conexión de MongoDB.

    def buscar(self, filtro: dict) -> List[Pokemon]:
        """
        Devuelve lista de Pokémon según filtro
        
        :param filtro: Filtro de MongoDB. e.g: { "nombre": "pepe" } o { $and ["alumnos.$.nombre": "pepe", "alumnos.$.edad": 21 ]}
        
        Returns:
            List[Pokemon]: Resultado de la búsqueda de Pokemones. 
        """
        pokes = []
        
        resultados = self.conexion.buscar(self.coleccion, filtro)
        
        for poke in resultados:
            
            poke.pop("_id", None)                                               # MongoDB agrega _id, y tuve que quitarlo porque rompía mi dataclass.
            ataques = [Ataque(**a) for a in poke.get("ataques", [])]            
            poke["ataques"] = ataques
            pokes.append(Pokemon(**poke))
            
        return pokes

    def actualizar(self, filtro: dict, nuevos_valores: dict) -> int:
        """
        Actualiza campos de Pokémon
        
        :param filtro:              Filtro de MongoDB. e.g: { "nombre": "pepe" } o { $and ["alumnos.$.nombre": "pepe", "alumnos.$.edad": 21 ]}
        :param nuevos_valores:      Valor a actualizar. e.g: { "alumnos.$.nombre": "pepe" }
        
        Returns:
            int: Cantidad de documentos actualizados.
        """
        return self.conexion.actualizar(self.coleccion, filtro, nuevos_valores)

    def actualizar_ataque(self, nombre_pokemon: str, nombre_ataque: str, nuevos_valores: dict) -> int:
        """
        Actualiza un ataque específico de un Pokémon usando $ y arrayFilters
        
        :param nombre_pokemon: Nombre del Pokemon.
        :param nombre_ataque: Nombre de ataque.
        :param nuevos_valores: 
        """
        
        filtro = { "nombre": nombre_pokemon, "ataques.nombre": nombre_ataque }
        
        update = {"$set": {f"ataques.$.{k}": v for k, v in nuevos_valores.items()} }
        
        return self.conexion.db[self.coleccion].update_one(filtro, update).modified_count

    def eliminar(self, filtro: dict) -> int:
        """Elimina Pokémon completos según filtro"""
        return self.conexion.eliminar(self.coleccion, filtro)

    def eliminar_ataque(self, nombre_pokemon: str, nombre_ataque: str) -> int:
        """Elimina un ataque específico del array ataques"""
        filtro = {"nombre": nombre_pokemon}
        update = {"$pull": {"ataques": {"nombre": nombre_ataque}}}
        return self.conexion.db[self.coleccion].update_one(filtro, update).modified_count
