# Voici les différentes fonctions que l'api de Woody pourrait utiliser
#
# Il y a beacoup de "sleep", et de ralentissement qui ont pour but de simuler une grosse charge et/ou
# pour simuler des requètes qui seraient (dans un cas réel) plus lourde..
#
# Ce fichier ne peut pas être modifié (du moins pas pour "fixer" les limitations qu'il introduit ;)
# ( ce fichier sera, à terme dans une lib externe pour rendre plus clair la séparation)


from werkzeug.serving import run_simple
from mysql.connector import connect, Error
from time import sleep

LONG_WAIT_TIME = 5  # seconds
SHORT_WAIT_TIME = 5


def my_connect():
    # note, c'est une mauvaise idée de recréer la connection à chaque requète
    # (c'est surtt pour une question de performance)
    # Mais ici, ce n'est pas la performance qu'on cherche ;)

    try:
        mydb = connect(host='db', user='root', password='pass', database='woody', port=3306)
        mycursor = mydb.cursor()
    except Error as e:
        print(e)
        return None, None
    return mydb, mycursor


def make_some_heavy_computation(param=""):
    sleep(LONG_WAIT_TIME)
    return f"Woody -{param}- Woody"


def launch_server(app, host='0.0.0.0', port=5000):
    # voici ce qui rend le serveur si limité ...
    run_simple(host, port, app, use_reloader=True, threaded=False)