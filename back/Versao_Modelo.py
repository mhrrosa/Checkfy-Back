class Versao_Modelo:
    def __init__(self, db):
        self.db = db

    def add_versao_modelo(self, nome, status):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("INSERT INTO versao_modelo (Nome, Status) VALUES (%s, %s)", (nome, status))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Reverte em caso de erro
            print(f"Erro ao adicionar versão do modelo ao banco de dados: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def get_versao_modelo(self):
        cursor = self.db.conn.cursor(dictionary=True)
        query = "SELECT * FROM versao_modelo ORDER BY Nome DESC"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def delete_versao_modelo(self, versao_modelo_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("DELETE FROM versao_modelo WHERE ID = %s", (versao_modelo_id,))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Reverte em caso de erro
            print(f"Erro ao deletar versão do modelo: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado
    def update_versao_modelo(self, nome, status, id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE versao_modelo SET Nome = %s, Status = %s WHERE ID = %s", (nome, status, id))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Reverte em caso de erro
            print(f"Erro ao atualizar versão do modelo: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado
