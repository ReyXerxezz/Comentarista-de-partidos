import assistant

import mysql.connector
from mysql.connector import errorcode

# Configura los detalles de conexión

conn = mysql.connector.connect(user='admin_futbol', password='futbol123', host='localhost', port='33306', database='futbol')
cursor = conn.cursor()


def main():
    # Ejecutar una consulta simple
    cursor.execute("SELECT * FROM jugador")
    rows = cursor.fetchall()

    # Imprimir los resultados
    for row in rows:
        print(row)

    # Cerrar la conexión
    conn.close()

if __name__ == "__main__":
    main()