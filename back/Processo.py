class Processo:
    def __init__(self, db):
        self.db = db

    def add_processo(self, descricao, tipo, id_versao_modelo):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Insere um novo processo no banco de dados
            cursor.execute(
                "INSERT INTO processo (Descricao, Tipo, ID_Versao_Modelo) VALUES (%s, %s, %s)", 
                (descricao, tipo, id_versao_modelo)
            )
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao adicionar processo ao banco de dados: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def get_processos(self, id_versao_modelo: int):
        cursor = self.db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM processo where ID_Versao_Modelo = %s ORDER BY id", (id_versao_modelo,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def delete_processo(self, processo_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Remove o processo com base no ID fornecido
            cursor.execute("DELETE FROM processo WHERE ID = %s", (processo_id,))
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao deletar processo: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def update_processo(self, processo_id, nova_descricao, novo_tipo):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Atualiza os campos do processo com base no ID
            cursor.execute(
                "UPDATE processo SET Descricao = %s, Tipo = %s WHERE ID = %s", 
                (nova_descricao, novo_tipo, processo_id)
            )
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar processo: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado