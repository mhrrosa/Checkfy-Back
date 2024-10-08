class Instituicao:
    def __init__(self, db):
        self.db = db

    def add_instituicao(self, nome_instituicao, cnpj):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Insere a instituição
            cursor.execute(
                "INSERT INTO instituicao (Nome, Cnpj) VALUES (%s, %s)", 
                (nome_instituicao, cnpj)
            )
            # Confirma a transação no banco de dados
            self.db.conn.commit()
            
            # Obtém o último ID inserido
            value = cursor.lastrowid
            return value
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao adicionar instituição ao banco de dados: {e}")
            raise e
        finally:
            cursor.close()
        
    def get_instituicoes(self):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM instituicao ORDER BY Nome")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Erro ao obter instituições do banco de dados: {e}")
            cursor.close()
            raise e
    def instituicao_avaliacao_insert(self, avaliacao_id, instituicao_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Atualiza a avaliação com o ID da instituição
            cursor.execute(
                "UPDATE avaliacao SET ID_Instituicao = %s WHERE ID = %s", 
                (instituicao_id, avaliacao_id)
            )
            # Confirma a transação no banco de dados
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar instituição na avaliação: {e}")
            raise e
        finally:
            cursor.close()