import sqlite3 
import pandas as pd

connector = sqlite3.connect("etl.db", check_same_thread=False)

def get_mean_and_standard_deviation(sample: pd.DataFrame,isDate=False):
    if isDate:
        sample = sample.apply(lambda x: pd.Series(x).astype('datetime64[ns]'))

    return (sample.mean(axis=0),sample.std(axis=0))

def get_min_max(sample: pd.DataFrame,isDate=False):
    if isDate:
        sample = sample.apply(lambda x: pd.Series(x).astype('datetime64[ns]'))
    return (sample.min(axis=0), sample.max(axis=0))


def ejercicio2_data():
    # Numero de muestras 
    sample = pd.read_sql_query("SELECT * from usuarios INNER JOIN emails ON emails.usuario = usuarios.username INNER JOIN fechas ON fechas.usuario = usuarios.username INNER JOIN ips ON ips.usuario=usuarios.username",connector)
    sample.replace('None', None, inplace=True)
    sample.dropna(subset=sample.columns, axis=0, inplace=True)
    # print(len(sample))
    ret_data = [ {"Numero de muestras": len(sample)} ]

    # Media y desviación estándar del total de fechas en las que se ha cambiado la contraseña
    dates = pd.read_sql_query("SELECT length(fecha) from fechas GROUP BY usuario",connector)
    media,de = get_mean_and_standard_deviation(dates)
    # print(f"Desviación Estandar del total de fechas: {de.to_string().strip().split(' ')[-1]}")
    # print(f"Media: { media.to_string().strip().split(' ')[-1]}\n")
    tmp = { 
        "Total de fechas en las que se ha cambiado la contraseña" : [
            {"Desviacion estándard" : de.to_string().strip().split(' ')[-1]},
            {"Media" : media.to_string().strip().split(' ')[-1] },
        ]
    }
    ret_data.append(tmp)

    # Media y desviación estándar del total de IPs que se han detectado.
    ips = pd.read_sql_query("SELECT LENGTH(ip) as IP FROM ips GROUP BY usuario",connector)
    media,de = get_mean_and_standard_deviation(ips)
    # print(f"Desviación Estandar del total de IPs: {de.to_string().strip().split(' ')[-1]}")
    # print(f"Media del total de IPs: {media.to_string().strip().split(' ')[-1]}\n")
    tmp = {
        "Total de IPs que se han detectado" : [
            {"Desviación estandard" : de.to_string().strip().split(' ')[-1]},
            {"Media" : media.to_string().strip().split(' ')[-1] },
        ]
    }
    ret_data.append(tmp)

    # Media y desviación estándar del número de email recibidos de phishing en los que ha interactuado
    click_mails = pd.read_sql_query("SELECT cliclados from emails",connector)
    media,de = get_mean_and_standard_deviation(click_mails)
    # print(f"Desviación Estandar: {de.to_string().strip().split(' ')[-1]}")
    # print(f"Media: { media.to_string().strip().split(' ')[-1]}\n")
    tmp = {
        "Numero de email recibidos de phishing en los que se ha interactuado" : [
            {"Desviación estandard" : de.to_string().strip().split(' ')[-1]},
            {"Media" : media.to_string().strip().split(' ')[-1] },
        ]
    }
    ret_data.append(tmp)

    # Valor mínimo y valor máximo del total de emails recibidos.
    total_mails = pd.read_sql_query("SELECT total from emails",connector)
    min_mail, max_mail = get_min_max(total_mails)
    # print(f"Mínimo de mails que ha recibido un usuario: {min_mail.to_string().strip().split(' ')[-1]}")
    # print(f"Máximo de mails que ha recibido un usuario: {max_mail.to_string().strip().split(' ')[-1]}\n")
    tmp = {
        "Emails recibidos" : [
            {"Minimo de emails recibidos" : min_mail.to_string().strip().split(' ')[-1]},
            {"Maximo de emails recibidos" : max_mail.to_string().strip().split(' ')[-1] },
        ]
    }
    ret_data.append(tmp)

    # Valor mínimo y valor máximo del número de emails de phishing en los que ha interactuado un
    admin_mails = pd.read_sql_query("SELECT cliclados FROM emails INNER JOIN usuarios ON emails.usuario = usuarios.username WHERE usuarios.permisos = 1",connector)
    admin_min_mail, admin_max_mail = get_min_max(admin_mails)
    # print(f"Mínimo de mails que ha clicado un administrador: {admin_min_mail.to_string().strip().split(' ')[-1]}")
    # print(f"Máximo de mails que ha clicado un administrador: {admin_max_mail.to_string().strip().split(' ')[-1]}\n")
    tmp = {
        "Emails de phishing clicados por un administrador" : [
            {"Minimo de emails recibidos" : admin_min_mail.to_string().strip().split(' ')[-1]},
            {"Maximo de emails recibidos" : admin_max_mail.to_string().strip().split(' ')[-1] },
        ]
    }
    ret_data.append(tmp)

    return ret_data