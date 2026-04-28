from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result #ritorna una lista di oggetti Fermata

    @staticmethod
    def getAllEdges(): #seleziona tutte le connessioni
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def has_connection(u:Fermata, v:Fermata) -> bool:
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c
                where id_stazP=%s and id_stazA = %s"""
        cursor.execute(query, (u.id_fermata, v.id_fermata,))
        #non passo l'intero oggetto fermata ma solo l'id per il controllo nel db

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result)>0

    @staticmethod
    def get_vicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c 
                    where id_stazP=%s"""
        cursor.execute(query, (u.id_fermata,))
        # non passo l'intero oggetto fermata ma solo l'id per il controllo nel db

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result
