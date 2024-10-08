class Atividade:
    def __init__(self, db):
        self.db = db

    def get_atividades(self):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT ID, Descricao FROM atividade")
            result = cursor.fetchall()
            atividades_list = [
                {"ID": atividade["ID"], "Descricao": atividade[ "Descricao"]} for atividade in result
            ]
            cursor.close()
            return atividades_list
        except Exception as e:
            print(f"Erro ao buscar atividades: {e}")
            cursor.close()
            raise e
