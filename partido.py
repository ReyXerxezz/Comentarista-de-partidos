import assistant
import time
import schedule
import sqlite3

connection = sqlite3.connect('futbol')
cursor = connection.cursor()

class Partido:
    def __init__(self):
        self.tiempo_inicio = time.time()
        self.partido_terminado = False

    def calcular_minuto(self):
        tiempo_actual = time.time()
        diferencia_segundos = tiempo_actual - self.tiempo_inicio
        minuto = int(diferencia_segundos // 60)
        return minuto
    
    def marcar_gol(self, autor_gol, asistente):
        minuto_gol = self.calcular_minuto()
        # Buscar el documento del autor del gol y del asistente
        self.cursor.execute("SELECT documento FROM jugador WHERE nombre = ?", (autor_gol,))
        documento_autor_gol = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT documento FROM jugador WHERE nombre = ?", (asistente,))
        documento_asistente = self.cursor.fetchone()[0]
        # Registrar el gol en la base de datos
        self.cursor.execute("INSERT INTO gol (goleador, minuto, asistidor) VALUES (?, ?, ?)", (documento_autor_gol, minuto_gol, documento_asistente))
        # Actualizar las estadísticas del autor del gol y del asistente
        self.cursor.execute("UPDATE jugador SET goles = goles + 1 WHERE documento = ?", (documento_autor_gol,))
        self.cursor.execute("UPDATE jugador SET asistencias = asistencias + 1 WHERE documento = ?", (documento_asistente,))
        self.conn.commit()

    def cometer_falta(self, autor_falta, victima_falta, tarjeta):
        minuto_falta = self.calcular_minuto()
        # Buscar el documento del autor de la falta y de la víctima
        self.cursor.execute("SELECT documento FROM jugador WHERE nombre = ?", (autor_falta,))
        documento_autor_falta = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT documento FROM jugador WHERE nombre = ?", (victima_falta,))
        documento_victima_falta = self.cursor.fetchone()[0]
        # Registrar la falta en la base de datos
        self.cursor.execute("INSERT INTO falta (actor, receptor, minuto, tarjeta) VALUES (?, ?, ?, ?)", (documento_autor_falta, documento_victima_falta, minuto_falta, tarjeta))
        # Actualizar las estadísticas del autor de la falta
        if tarjeta == 'amarilla':
            self.cursor.execute("UPDATE jugador SET tarjetas_amarillas = tarjetas_amarillas + 1 WHERE documento = ?", (documento_autor_falta,))
        elif tarjeta == 'roja':
            self.cursor.execute("UPDATE jugador SET tarjetas_rojas = tarjetas_rojas + 1 WHERE documento = ?", (documento_autor_falta,))
        self.conn.commit()

    def terminar_partido(self):
        self.partido_terminado = True
        self.conn.close()
