import assistant
import time
import schedule
import mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable


connection = mysql.connector.connect(user='admin_futbol', password='futbol123', host='localhost', port='33306', database='futbol')
cursor = connection.cursor()

class Partido:
    def __init__(self, club_local, club_visitante):
        self.tiempo_inicio = time.time()
        self.partido_terminado = False
        self.tiempo_extra = 0
        self.goles_local = 0
        self.goles_visitante = 0
        self.club_local = club_local
        self.club_visitante = club_visitante
        cursor.execute(f"SELECT nit FROM club WHERE nombre = '{club_local}'")
        self.nit_local = cursor.fetchone()[0]
        cursor.execute(f"SELECT nit FROM club WHERE nombre = '{club_visitante}'")
        self.nit_visitante = cursor.fetchone()[0]

    def calcular_minuto(self):
        tiempo_actual = time.time()
        diferencia_segundos = tiempo_actual - self.tiempo_inicio
        minuto = int(diferencia_segundos // 60)
        return minuto
    
    def marcar_gol(self, autor_gol, asistente):
        minuto_gol = self.calcular_minuto()
        # Buscar el documento del autor del gol y del asistente
        cursor.execute(f"SELECT documento, club FROM jugador WHERE nombre = '{autor_gol.lower()}'")
        documento_autor_gol, club_autor_gol = cursor.fetchone()
        cursor.execute(f"SELECT documento FROM jugador WHERE nombre = '{asistente.lower()}'")
        documento_asistente = cursor.fetchone()[0]
        # Registrar el gol en la base de datos
        cursor.execute(f"INSERT INTO gol (goleador, minuto, asistidor) VALUES ('{documento_autor_gol}', {minuto_gol}, '{documento_asistente}')")
        # Actualizar las estadísticas del autor del gol y del asistente
        cursor.execute(f"UPDATE jugador SET goles = goles + 1 WHERE documento = '{documento_autor_gol}'")
        cursor.execute(f"UPDATE jugador SET asistencias = asistencias + 1 WHERE documento = '{documento_asistente}'")
        # Comparar el club del autor del gol con los clubes del partido
        if club_autor_gol == self.nit_local:
            self.goles_local += 1
        elif club_autor_gol == self.nit_visitante:
            self.goles_visitante += 1
        connection.commit()


    def cometer_falta(self, autor_falta, victima_falta, tarjeta):
        minuto_falta = self.calcular_minuto()
        # Buscar el documento del autor de la falta y de la víctima
        cursor.execute(f"SELECT documento FROM jugador WHERE nombre = '{autor_falta.lower()}'")
        documento_autor_falta = cursor.fetchone()[0]
        cursor.execute(f"SELECT documento FROM jugador WHERE nombre = '{victima_falta.lower()}'")
        documento_victima_falta = cursor.fetchone()[0]
        # Registrar la falta en la base de datos
        cursor.execute(f"INSERT INTO falta (actor, receptor, minuto, tarjeta) VALUES ('{documento_autor_falta}', '{documento_victima_falta}', {minuto_falta}, '{tarjeta}')")
        # Actualizar las estadísticas del autor de la falta
        if tarjeta == 'amarilla':
            cursor.execute(f"UPDATE jugador SET tarjetas_amarillas = tarjetas_amarillas + 1 WHERE documento = '{documento_autor_falta}'")
        elif tarjeta == 'roja':
            cursor.execute(f"UPDATE jugador SET tarjetas_rojas = tarjetas_rojas + 1 WHERE documento = '{documento_autor_falta}'")
        connection.commit()
        

        
    def terminar_partido(self):
        self.partido_terminado = True
        cursor.execute(f"""
        INSERT INTO partido (club_local, club_visitante, goles_local, goles_visitante, nombre_local, nombre_visitante) 
        VALUES ('{self.nit_local}', '{self.nit_visitante}', {self.goles_local}, {self.goles_visitante}, '{self.club_local}', '{self.club_visitante}')
        """)
        if self.goles_local > self.goles_visitante:
            cursor.execute(f"UPDATE club SET W = W + 1 WHERE nit = '{self.nit_local}'")
            cursor.execute(f"UPDATE club SET L = L + 1 WHERE nit = '{self.nit_visitante}'")
        elif self.goles_local < self.goles_visitante:
            cursor.execute(f"UPDATE club SET W = W + 1 WHERE nit = '{self.nit_visitante}'")
            cursor.execute(f"UPDATE club SET L = L + 1 WHERE nit = '{self.nit_local}'")
        else:
            cursor.execute(f"UPDATE club SET D = D + 1 WHERE nit = '{self.nit_local}'")
            cursor.execute(f"UPDATE club SET D = D + 1 WHERE nit = '{self.nit_visitante}'")
        connection.commit()
        connection.close()
