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
    def getAllEdgesPesati():  # seleziona tutte le connessioni e conta quante volte si ripetono
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select id_stazP, id_stazA, count(*) as peso
                    from connessione c 
                    group by id_stazP, id_stazA 
                    order by peso desc"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["peso"]))
        cursor.close()
        conn.close()
        return result #ritorna una tupla

    @staticmethod
    def getAllEdgesVelocita():  # seleziona tutte le connessioni e la loro velocità massima
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.id_stazP, c.id_stazA, max(velocita) as v
                    from connessione c, linea l
                    where c.id_linea=l.id_linea 
                    group by c.id_stazP, c.id_stazA
                    order by v asc"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["v"]))
        cursor.close()
        conn.close()
        return result #ritorna una tupla

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
