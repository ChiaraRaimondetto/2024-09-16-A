from database.DB_connect import DBConnect
from model.arco import Arco
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getRangeLat():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.Lat  as lat
                    from state s
                    order by s.Lat asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["lat"])
            cursor.close()
            cnx.close()
        return result[0],result[len(result)-1]

    @staticmethod
    def getRangeLng():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    select distinct s.Lng as lng 
                    from state s
                    order by s.Lng  asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["lng"])
            cursor.close()
            cnx.close()
        return result[0],result[len(result)-1]
    @staticmethod
    def getAllShape():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(s.shape ) as shape
                        from sighting s 
                        where s.shape is not null 
                        order by s.shape desc 
                    """
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(lat,log,forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s2.*
                from sighting s ,state s2 
                where s.state =s2.id and s2.Lat >%s and s2.Lng >%s and s.shape =%s
                group by s2.id 
                      """
            cursor.execute(query,(lat,log,forma))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(lat, log, forma,idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
            
                select t1.id as s1,t2.id as s2,t1.durata +t2.durata as peso
                from (select s2.id ,s2.Neighbors ,sum(s.duration ) as  durata
                from sighting s ,state s2 
                where s.state =s2.id and s2.Lat > %s and s2.Lng > %s and s.shape = %s
                group by s2.id ,s2.Neighbors )t1,
                (select s2.id ,s2.Neighbors ,sum(s.duration ) as  durata
                from sighting s ,state s2 
                where s.state =s2.id and s2.Lat > %s and s2.Lng > %s and s.shape = %s
                group by s2.id ,s2.Neighbors ) t2
                where FIND_IN_SET(t1.id ,replace(t2.neighbors,' ',',') )>0 
                group by t1.id,t2.id
                        """
            cursor.execute(query, (lat, log, forma,lat, log, forma))

            for row in cursor:
                result.append(Arco(idMap[row["s1"]],idMap[row["s2"]],row["peso"]))
            cursor.close()
            cnx.close()
        return result









