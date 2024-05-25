import mysql.connector
from prettytable import PrettyTable


connection = mysql.connector.connect(user='admin_futbol', password='futbol123', host='localhost', port='33306', database='futbol')
cursor = connection.cursor()

class Estadisticas:
    
    def __init__(self):
        self.connection = connection
        self.cursor = cursor

    def mostrar_maximo_goleador(self):
        self.cursor.execute("""
            SELECT j.nombre, c.nombre, COUNT(g.id) as goles
            FROM gol g
            JOIN jugador j ON g.goleador = j.documento
            JOIN club c ON j.club = c.nit
            GROUP BY j.nombre, c.nombre
            ORDER BY goles DESC 
            LIMIT 5
        """)
        resultados = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Jugador", "Club", "Goles"]
        for row in resultados:
            table.add_row(row)
        print("Máximo goleador:")
        print(table)

    def mostrar_maximo_asistente(self):
        self.cursor.execute("""
            SELECT j.nombre, c.nombre, COUNT(g.id) as asistencias
            FROM gol g
            JOIN jugador j ON g.asistidor = j.documento
            JOIN club c ON j.club = c.nit
            GROUP BY j.nombre, c.nombre
            ORDER BY asistencias DESC 
            LIMIT 5
        """)
        resultados = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Jugador", "Club", "Asistencias"]
        for row in resultados:
            table.add_row(row)
        print("Máximo asistente:")
        print(table)

    def mostrar_equipo_mas_victorias(self):
        self.cursor.execute("""
            SELECT nombre, W 
            FROM club 
            ORDER BY W DESC 
            LIMIT 1
        """)
        resultados = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Equipo", "Victorias"]
        for row in resultados:
            table.add_row(row)
        print("Equipo con más victorias:")
        print(table)

    def mostrar_puntos(self):
        self.cursor.execute("""
            SELECT nombre, W, D, L, (W * 3) + (D * 1) + (L * 0) AS puntos
            FROM club
            ORDER BY puntos DESC
        """)
        resultados = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Equipo", "Victorias", "Empates", "Derrotas", "Puntos"]
        for row in resultados:
            table.add_row(row)
        print("Tabla de puntos:")
        print(table)


