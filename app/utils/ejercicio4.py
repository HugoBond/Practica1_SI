import pandas as pd
import matplotlib.pyplot as plt
from ejercicio2 import connector
from ejercicio3 import RAINBOWTABLE


def grafico_usuarios_mas_criticos():
    users = pd.read_sql_query("SELECT username,contrasena,cliclados FROM emails INNER JOIN usuarios ON emails.usuario = usuarios.username ORDER BY emails.cliclados DESC",connector)
    critical_users = users[users['contrasena'].isin(RAINBOWTABLE.keys())][['cliclados','username']][:10]
    # plt.figure(figsize=(16, 6))
    # plt.bar(critical_users['username'], critical_users['cliclados'])
    # plt.xlabel("Usernames")
    # plt.ylabel("Mails clicados")
    # plt.title("Los 10 usuarios más críticos")
    # plt.show()
    return {
        "title" : "Los 10 usuarios más críticos",
        "xlabel" : "Usernames",
        "ylabel" : "Mails clicados",
        "xdata" : critical_users['username'].to_list(),
        "values" : critical_users['cliclados'].to_list()
    }


def grafico_media_tiempo_cambio_cont():
    users = pd.read_sql_query("SELECT * FROM fechas INNER JOIN usuarios ON fechas.usuario=usuarios.username", connector)
    users['fecha'] = pd.to_datetime(users['fecha'],dayfirst=True)  
    media_x_usuario = users.groupby(['usuario', 'permisos'])['fecha'].mean().dt.day
    media_x_usuario = media_x_usuario.groupby('permisos').mean()
    # media_x_usuario.plot(kind='bar', color=['blue', 'red'])
    # plt.title('Media de tiempo entre cambios de contraseña por tipo de usuario')
    # plt.xlabel('Tipo de usuario')
    # plt.ylabel('Media de tiempo (días)')
    # plt.xticks([0, 1], ['Usuarios Normales', 'Administradores'], rotation=45)
    # plt.show()
    return {
        "title" : "Media de tiempo entre cambios de contraseña por tipo de usuario",
        "xlabel" : "Tipo de usuario",
        "ylabel" : "Media de tiempo (dias)",
        "xdata" : ['Usuarios Normales', 'Administradores'],
        "values" : media_x_usuario.to_list()
    }

def grafico_webs_con_mas_politicas():
    webs = pd.read_sql_query("SELECT creacion FROM legal INNER JOIN usuarios ON emails.usuario = usuarios.username ORDER BY emails.cliclados DESC", connector)




def grafico_cumplimiento_politicas_por_ano():
    webs = pd.read_sql_query("SELECT * FROM legal", connector)
    cumplen = webs[webs.proteccion_de_datos == 1][webs.aviso == 1][webs.cookies == 1]
    no_cumplen = pd.read_sql_query("SELECT * FROM legal WHERE cookies = 0 OR proteccion_de_datos = 0 OR aviso = 0", connector)
    lista_años =  list(set(webs['creacion'].sort_values()))
    lista_años.sort()

    cumplen = cumplen.groupby('creacion')['web'].count().to_dict()
    no_cumplen = no_cumplen.groupby('creacion')['web'].count().to_dict()
    
    for ano in lista_años:
        if ano not in cumplen.keys():
            cumplen[ano] = 0
        if ano not in no_cumplen.keys():
            no_cumplen[ano] = 0
    

grafico_cumplimiento_politicas_por_ano()