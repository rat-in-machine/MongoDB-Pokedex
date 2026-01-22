import os
import streamlit as st
import json

from dotenv import load_dotenv

from classes.database.conector_bd import ConexionBD
from classes.pokemon import * 

# ------------------------------------- #
# --- Carga de variables de entorno --- #
# ------------------------------------- #

def crear_base_de_datos():
    st.subheader("Crear base de datos y colección")

    nombre_bd = st.text_input(
        "Nombre de la base de datos",
        placeholder="Ej: pokedex_db"
    )

    nombre_coleccion = st.text_input(
        "Nombre de la colección",
        placeholder="Ej: Pokemon"
    )

    if st.button("Crear base de datos"):
        if not nombre_bd or not nombre_coleccion:
            st.error("Debes indicar el nombre de la base de datos y la colección")
            return

        try:
            # Llamada a tu lógica real
            conexion.crear_bd_y_coleccion(nombre_bd, nombre_coleccion)

            st.success(
                f"Base de datos '{nombre_bd}' y colección '{nombre_coleccion}' creadas correctamente"
            )

        except Exception as e:
            st.error(f"Error creando la base de datos: {e}")

def buscar_datos():
    st.subheader("Buscar datos en la base de datos")

    # Selección de base de datos
    database = st.text_input(
        "Nombre de la base de datos",
        placeholder="Ej: pokedex_db"
    )

    coleccion = st.text_input(
        "Nombre de la colección",
        placeholder="Ej: Pokemon"
    )

    filtro_str = st.text_area(
        "Filtro de búsqueda (JSON)",
        placeholder='Ej: {"nombre": "Pikachu"}'
    )

    if st.button("Buscar"):
        if not database or not coleccion:
            st.error("Debes indicar la base de datos y la colección")
            return

        try:
            # Si no se escribe nada, usamos filtro vacío
            filtro = json.loads(filtro_str) if filtro_str.strip() else {}

        except json.JSONDecodeError:
            st.error("El filtro no es un JSON válido")
            return

        try:
            resultados = conexion.buscar(database, coleccion, filtro)

            if not resultados:
                st.warning("No se encontraron resultados")
                return

            st.success(f"Resultados encontrados: {len(resultados)}")
            st.json(resultados)

        except Exception as e:
            st.error(f"Error realizando la búsqueda: {e}")

def insertar_desde_json():
    st.subheader("Insertar datos desde JSON")

    nombre_bd = st.text_input(
        "Nombre de la base de datos",
        placeholder="Ej: pokedex_db"
    )

    nombre_coleccion = st.text_input(
        "Nombre de la colección",
        placeholder="Ej: Pokemon"
    )

    json_input = st.text_area(
        "JSON a insertar",
        placeholder='Ej:\n{\n  "nombre": "Pikachu",\n  "nivel": 5\n}\n\nO una lista de documentos'
    )

    if st.button("Insertar datos"):
        if not nombre_bd or not nombre_coleccion or not json_input:
            st.error("Debes completar todos los campos")
            return

        try:
            datos = json.loads(json_input)

            db = conexion.client[nombre_bd]
            coleccion = db[nombre_coleccion]

            if isinstance(datos, list):
                coleccion.insert_many(datos)
            elif isinstance(datos, dict):
                coleccion.insert_one(datos)
            else:
                st.error("El JSON debe ser un objeto o una lista de objetos")
                return

            st.success("Datos insertados correctamente")

        except json.JSONDecodeError:
            st.error("El JSON no es válido")
        except Exception as e:
            st.error(f"Error insertando datos: {e}")

def eliminar_base_de_datos():
    st.subheader("Eliminar base de datos")

    nombre_bd = st.text_input(
        "Nombre de la base de datos a eliminar",
        placeholder="Ej: pokedex_db"
    )

    confirmacion = st.checkbox(
        "Entiendo que esta acción es irreversible"
    )

    if st.button("Eliminar base de datos"):
        if not nombre_bd:
            st.error("Debes indicar el nombre de la base de datos")
            return

        if not confirmacion:
            st.warning("Debes confirmar que entiendes las consecuencias")
            return

        try:
            conexion.client.drop_database(nombre_bd)
            st.success(f"Base de datos '{nombre_bd}' eliminada correctamente")

        except Exception as e:
            st.error(f"Error eliminando la base de datos: {e}")


def eliminar_ataque():
    """
    Interfaz que permite deshacerse un ataque de un Pokemon.
    """
    
    st.subheader("Eliminar ataque")

    nombre_pokemon = st.text_input("Nombre del Pokémon")
    nombre_ataque = st.text_input("Nombre del ataque")

    if st.button("Eliminar ataque"):
        modificados = pokemon_dao.eliminar_ataque(nombre_pokemon, nombre_ataque)
        st.warning(f"Ataques eliminados: {modificados}")

def eliminar_pokemon():
    """
    Interfaz que permite deshacerse de un Pokemon registrado.
    """
    
    st.subheader("Eliminar Pokémon")

    nombre = st.text_input("Nombre del Pokémon a eliminar")

    if st.button("Eliminar"):
        eliminados = pokemon_dao.eliminar({"nombre": nombre})
        st.warning(f"Pokémon eliminados: {eliminados}")

def actualizar_ataque():
    """
    Interfaz que permite actualizar el ataque de un Pokemon.
    """
    
    st.subheader("Actualizar ataque")

    nombre_pokemon = st.text_input("Nombre del Pokémon")
    nombre_ataque = st.text_input("Nombre del ataque")
    nuevo_tipo = st.text_input("Nuevo tipo del ataque")

    if st.button("Actualizar ataque"):
        modificados = pokemon_dao.actualizar_ataque(
            nombre_pokemon,
            nombre_ataque,
            {"tipo": nuevo_tipo},
        )
        st.success(f"Ataques modificados: {modificados}")

def actualizar_nivel():
    """
    Interfaz que permite cambiar el nivel de un Pokemon.
    """
    
    st.subheader("Actualizar nivel")

    nombre = st.text_input("Nombre del Pokémon")
    nuevo_nivel = st.number_input("Nuevo nivel", min_value=1, step=1)

    if st.button("Actualizar"):
        modificados = pokemon_dao.actualizar(
            {"nombre": nombre}, {"nivel": nuevo_nivel}
        )
        st.success(f"Documentos modificados: {modificados}")

def buscar_pokemon():
    """
    Interfaz que permite realizar búsquedas de Pokemones.
    """
    
    st.subheader("Buscar Pokémon")

    nombre = st.text_input("Nombre")
    region = st.text_input("Región")

    if st.button("Buscar"):
        filtro = {}
        if nombre:
            filtro["nombre"] = nombre
        if region:
            filtro["region"] = region

        resultados = pokemon_dao.buscar(filtro)

        if not resultados:
            st.info("No se encontraron resultados")
        else:
            for p in resultados:
                st.markdown(f"### {p.nombre}")
                st.write(
                    f"Región: {p.region} | Nivel: {p.nivel} | Tipos: {p.tipo_primario}/{p.tipo_secundario}"
                )
                if p.ataques:
                    st.write("Ataques:")
                    for a in p.ataques:
                        st.write(f"- {a.nombre} ({a.tipo})")

def insertar_pokemon():
    """
    Interfáz que permite la inserción de un Pokemon.
    """
    
    st.subheader("Insertar Pokémon")

    nombre = st.text_input("Nombre")
    region = st.text_input("Región")
    pokedex = st.number_input("Pokédex nacional", min_value=1, step=1)
    tipo1 = st.text_input("Tipo primario")
    tipo2 = st.text_input("Tipo secundario (opcional)")
    nivel = st.number_input("Nivel", min_value=1, step=1)

    ataques_str = st.text_area("Ataques (formato nombre:tipo, uno por línea)")

    if st.button("Insertar"):
        ataques: List[Ataque] = []
        for linea in ataques_str.splitlines():
            if ":" in linea:
                n, t = linea.split(":", 1)
                ataques.append(Ataque(nombre=n.strip(), tipo=t.strip()))

        pokemon = Pokemon(
            nombre=nombre,
            region=region,
            pokedex_nacional=pokedex,
            tipo_primario=tipo1,
            tipo_secundario=tipo2 or None,
            nivel=nivel,
            ataques=ataques or None,
        )

        pokemon_dao.insertar(pokemon)
        st.success(f"Pokémon {nombre} insertado")

# Cargo las variables de entorno.
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
url = os.getenv("DB_URL")
db_name = os.getenv("DB_NAME")

if  not url or not db_name:
    raise Exception("No se han detectado variables de entorno.")
if not user or not password:
    user = password = ""

conexion = ConexionBD(url, user, password, db_name)
pokemon_dao = PokemonDAO(conexion=conexion)

if not pokemon_dao:
    raise Exception("MongoDB no ha sido instanciado.")
else:
    print("Conexión con la base de datos establecida.")

# -------------------------------- #
# --- Formación de la interfáz --- #
# -------------------------------- #

st.set_page_config(page_title="Pokédex MongoDB", layout="wide")
st.title("Interfaz Pokédex MongoDB")

menu = st.sidebar.selectbox(
    "Acción",
    [
        "Crear base de datos",
        "Eliminar base de datos",
        "Buscar datos",
        "Insertar JSON",
        "Insertar Pokémon",
        "Buscar Pokémon",
        "Actualizar nivel",
        "Actualizar ataque",
        "Eliminar Pokémon",
        "Eliminar ataque",
    ],
)

if menu == "Insertar Pokémon":
    insertar_pokemon()

elif menu == "Crear base de datos":
    crear_base_de_datos()
elif menu == "Buscar datos":
    buscar_datos()
    
elif menu == "Insertar JSON":
    insertar_desde_json()
    
elif menu == "Eliminar base de datos":
    eliminar_base_de_datos()
    
elif menu == "Buscar Pokémon":
    buscar_pokemon()

elif menu == "Actualizar nivel":
    actualizar_nivel()

elif menu == "Actualizar ataque":
    actualizar_ataque()

elif menu == "Eliminar Pokémon":
    eliminar_pokemon()

elif menu == "Eliminar ataque":
    eliminar_ataque()

