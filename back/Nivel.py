class Nivel:
    def __init__(self, db):
        self.db = db

    def add_nivel(self, nivel, nome_nivel, id_versao_modelo):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Insere um novo nível no banco de dados
            cursor.execute(
                "INSERT INTO nivel_maturidade_mpsbr (Nivel, Nome_Nivel, id_versao_modelo) VALUES (%s, %s, %s)", 
                (nivel, nome_nivel, id_versao_modelo)
            )
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao adicionar nível ao banco de dados: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado
            
    def get_niveis(self, id_versao_modelo):
        cursor = self.db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nivel_maturidade_mpsbr where ID_Versao_Modelo = %s ORDER BY Nivel", (id_versao_modelo,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def get_niveis_limitado(self, id_versao_modelo, id_nivel_solicitado):
        cursor = self.db.conn.cursor(dictionary=True)
        # Busca os níveis da versão do modelo limitados até o ID do nível solicitado
        cursor.execute("""
            SELECT * FROM nivel_maturidade_mpsbr 
            WHERE ID_Versao_Modelo = %s AND Nivel >= 
                (SELECT Nivel FROM nivel_maturidade_mpsbr WHERE ID = %s)
            ORDER BY Nivel ASC
        """, (id_versao_modelo, id_nivel_solicitado))
        result = cursor.fetchall()
        cursor.close()
        return result

    def delete_nivel(self, nivel_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Remove o nível com base no ID fornecido
            cursor.execute("DELETE FROM nivel_maturidade_mpsbr WHERE ID = %s", (nivel_id,))
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao deletar nível: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def update_nivel(self, nivel_id, novo_nivel, novo_nome_nivel):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Atualiza os campos do nível com base no ID
            cursor.execute(
                "UPDATE nivel_maturidade_mpsbr SET Nivel = %s, Nome_Nivel = %s WHERE ID = %s", 
                (novo_nivel, novo_nome_nivel, nivel_id)
            )
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar nível: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado