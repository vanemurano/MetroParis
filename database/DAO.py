from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    def __init__(self):
        pass

    @staticmethod
    def getAllNodes():
        try:
            conn=DBConnect.get_connection()
            cursor=conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione al database")
            return

        query="""select distinct Chromosome 
                from genes 
                where chromosome!=0"""

        res=[]

        cursor.execute(query,)

        for row in cursor:
            res.append(row["Chromosome"])

        cursor.close()
        conn.close()

        return res # lista di interi cromosoma

    @staticmethod
    def getAllEdges():
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione al database")
            return

        query = """select distinct g1.Chromosome as c1, g2.chromosome as c2
                from interactions i, genes g1, genes g2
                where i.GeneId1=g1.GeneId 
                and i.GeneId2=g2.GeneID 
                and g1.Chromosome!=0 and g2.Chromosome!=0
                and g1.Chromosome!=g2.Chromosome"""

        res = []

        cursor.execute(query, )

        for row in cursor:
            res.append((row["c1"], row["c2"])) # tupla cromosoma1, cromosoma2

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getEdgeWeight(crom1: int, crom2: int):
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
        except ConnectionError:
            print("Errore di connessione al database")
            return

        query = """select sum(correlazione) as peso
                from (select distinct g1.GeneId as g1, g2.GeneId as g2, i.Expression_Corr as correlazione
                from interactions i, genes g1, genes g2
                where i.GeneId1=g1.GeneId
                and i.GeneId2=g2.GeneID 
                and g1.Chromosome=%s and g2.Chromosome=%s) as tab"""

        res = 0

        cursor.execute(query, (crom1, crom2,))

        for row in cursor:
            res=row["peso"] # restituisce direttamente un float

        cursor.close()
        conn.close()

        return res
