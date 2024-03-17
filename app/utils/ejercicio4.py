import pandas as pd
import matplotlib.pyplot as plt
from utils.ejercicio2 import connector
from utils.ejercicio3 import RAINBOWTABLE


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
    media_x_usuario.plot(kind='bar', color=['blue', 'red'])
    plt.title('Media de tiempo entre cambios de contraseña por tipo de usuario')
    plt.xlabel('Tipo de usuario')
    plt.ylabel('Media de tiempo (días)')
    plt.xticks([0, 1], ['Usuarios Normales', 'Administradores'], rotation=45)
    plt.show()
    return {
        "title" : "Los 10 usuarios más críticos",
        "xlabel" : "Usernames",
        "ylabel" : "Mails clicados",
        "xdata" : critical_users['username'].to_list(),
        "values" : critical_users['cliclados'].to_list()
    }

def grafico_webs_con_mas_politicas():
    webs = pd.read_sql_query("SELECT creacion FROM legal INNER JOIN usuarios ON emails.usuario = usuarios.username ORDER BY emails.cliclados DESC", connector)



def grafico_cumplimiento_politicas_por_ano():
    webs = pd.read_sql_query("SELECT * FROM legal", connector)
    cumplen = webs[webs.proteccion_de_datos == 1][webs.aviso == 1][webs.cookies == 1]
    no_cumplen = webs[webs.proteccion_de_datos == 0][webs.aviso == 0][webs.cookies == 0]
    df = pd.DataFrame({'Cumplen': cumplen, 'No_Cumplen': no_cumplen})

    # Ordenar por año de creación
    df.sort_index(inplace=True)

    # Visualizar en un gráfico de barras
    df.plot(kind='bar', stacked=True)
    plt.title('Sitios web que cumplen vs. no cumplen las políticas de privacidad por año de creación')
    plt.xlabel('Año de creación')
    plt.ylabel('Cantidad de sitios web')
    plt.legend(title='Cumplimiento de políticas de privacidad')
    plt.show()
