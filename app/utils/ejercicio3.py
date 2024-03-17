import hashlib
import pandas as pd
from os import path
from utils.ejercicio2 import get_min_max, connector

filepath = path.dirname(path.abspath(__file__))

def create_rainbow_table(fname: str):
    rainbowtable = {}
    md5 = hashlib.md5
    with open(fname,"r") as file:
        for line in file:
            hash= md5(line.strip().encode()).hexdigest()
            rainbowtable[hash] = line.strip()
    return rainbowtable

def get_analysis(sample: pd.DataFrame):
    totalDeMuestras = len(sample)
    valoresAusentes = len(sample[sample.isnull()])
    mediana = sample.median()
    media = sample.mean()
    varianza = sample.var(ddof=0)
    m,M = get_min_max(sample)
    # print(f"Numero de Observaciones: {totalDeMuestras}\nNumero de valores ausentes: {valoresAusentes}\nMediana: {mediana}\nMedia: {media}\nVarianza: {varianza}\nMáximo: {M}\nMínimo: {m}\n\n")
    ret_data = [
        {"Numero de Observaciones" : totalDeMuestras},
        {"Numero de valores ausentes" : valoresAusentes},
        {"Mediana" : mediana,},
        {"Media" : media,},
        {"Varianza" : varianza,},
        {"Maximo" : M,},
        {"Minimo" : m,},
    ]
    return ret_data

RAINBOWTABLE = create_rainbow_table(f"{filepath}/rockyou-20.txt")

def ejercicio3_data():
    # Grupos
    # Grupo 1: Usuarios con contraseñas débiles
    users = pd.read_sql_query("SELECT contrasena,phishing FROM emails INNER JOIN usuarios ON emails.usuario = usuarios.username WHERE usuarios.permisos=0",connector)
    group1 = users[users['contrasena'].isin(RAINBOWTABLE.keys())]['phishing']
    ret_data = [{"Usuarios con contraseñas débiles" : get_analysis(group1)}]

    # Grupo 2: Usuarios con contraseñas robustas
    group2 = users[~users['contrasena'].isin(RAINBOWTABLE.keys())]['phishing']
    ret_data.append({"Usuarios con contraseñas robustas" : get_analysis(group2)})

    # Grupo 3: Administradores con contraseñas débiles
    admins = pd.read_sql_query("SELECT contrasena,phishing FROM emails INNER JOIN usuarios ON emails.usuario = usuarios.username WHERE usuarios.permisos=1",connector)
    group3 = admins[admins['contrasena'].isin(RAINBOWTABLE.keys())]['phishing']
    ret_data.append({"Administradores con contraseñas débiles" : get_analysis(group3)})

    # Grupo 4: Administradores con contraseñas robustas 
    group4 = admins[~admins['contrasena'].isin(RAINBOWTABLE.keys())]['phishing']
    ret_data.append({"Administradores con contraseñas robustas" : get_analysis(group4)})

    return ret_data