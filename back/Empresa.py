class Empresa:
    def __init__(self, db):
        self.db = db

    def add_empresa(self, nome_empresa, cnpj):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "INSERT INTO empresa (Nome, Cnpj) VALUES (%s, %s)", 
                (nome_empresa, cnpj)
            )
            empresa_id = cursor.lastrowid  # Recuperar o ID da empresa inserida
            self.db.conn.commit()  # Confirmar a operação
            return empresa_id
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao adicionar empresa ao banco de dados: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'
        
    def get_empresas(self):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM empresa ORDER BY Nome")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Erro ao obter empresas do banco de dados: {e}")
            cursor.close()
            raise e

    def delete_empresa(self, empresa_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute("DELETE FROM empresa WHERE ID = %s", (empresa_id,))
            self.db.conn.commit()  # Confirmar a operação
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao deletar empresa do banco de dados: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'


    def update_empresa(self, empresa_id, novo_nome, novo_cnpj):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "UPDATE empresa SET Nome = %s, Cnpj = %s WHERE ID = %s", 
                (novo_nome, novo_cnpj, empresa_id)
            )
            self.db.conn.commit()  # Confirmar a operação
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao atualizar empresa no banco de dados: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'
        
    def empresa_avaliacao_insert(self, avaliacao_id, empresa_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "UPDATE avaliacao SET ID_Empresa = %s WHERE ID = %s", 
                (empresa_id, avaliacao_id)
            )
            self.db.conn.commit()  # Confirmar a operação
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao vincular empresa à avaliação: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'
    
    def update_empresa_ajuste_avaliacao_inicial(self, id_empresa, nome):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "UPDATE empresa SET Nome = %s WHERE ID = %s", 
                (nome, id_empresa)
            )
            self.db.conn.commit()  # Confirmar a operação
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao atualizar nome da empresa no banco de dados: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'