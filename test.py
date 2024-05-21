import assistant
from unidecode import unidecode
import mysql.connector
from mysql.connector import errorcode

# Configura los detalles de conexión

conn = mysql.connector.connect(user='admin_futbol', password='futbol123', host='localhost', port='33306', database='futbol')
cursor = conn.cursor()


def main():
    # Ejecutar una consulta simple
    assistant.speak('Hello')
    lectura = unidecode(assistant.listen())
    print(lectura)
    # Cerrar la conexión
    conn.close()

if __name__ == "__main__":
    main()