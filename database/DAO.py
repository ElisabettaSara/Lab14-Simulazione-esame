from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getCromosomi(zero):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select Chromosome 
                    from genes g 
                    where Chromosome != %s"""
        cursor.execute(query, (zero,) )
        for row in cursor:
            result.append(row["Chromosome"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select g1.Chromosome as ch1, g2.Chromosome as ch2, sum(i.Expression_Corr) as peso
                    from(select Chromosome , g.GeneID as gid1
                        from genes g, classification c , interactions i 
                        where Chromosome != 0 and  g.GeneID = c.GeneID 
                                and i.GeneID1 = g.GeneID 
                        group by gid1 ) as g1,
                                
                                
                        (select Chromosome ,  g.GeneID as gid2
                        from genes g, classification c , interactions i 
                        where Chromosome != 0 and  g.GeneID = c.GeneID 
                                and i.GeneID2 = g.GeneID 
                        group by gid2) as g2,
                        
                        interactions i
                    where   i.GeneID1 = g1.gid1 and i.GeneID2 = g2.gid2  and g1.Chromosome != g2.Chromosome
                    group by g1.Chromosome, g2.Chromosome"""
        cursor.execute(query, )
        for row in cursor:
            result.append((row["ch1"], row["ch2"], row["peso"]))

        cursor.close()
        conn.close()
        return result


