import os
import streamlit as st

from dotenv import load_dotenv
from dataclasses import asdict

from classes.database.conector_bd import ConexionBD
from classes.pokemon import * 

# ------------------------------------- #
# --- Carga de variables de entorno --- #
# ------------------------------------- #

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

pokemon_dao = PokemonDAO(ConexionBD(url, user, password, db_name))
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

