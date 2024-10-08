class Documento:
    def __init__(self, db):
        self.db = db

    def add_documento(self, caminho_arquivo, nome_arquivo, id_projeto):
        cursor = self.db.conn.cursor(dictionary=True)
        query = "INSERT INTO documento (Caminho_Arquivo, Nome_Arquivo, ID_Projeto) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (caminho_arquivo, nome_arquivo, id_projeto))
            documento_id = cursor.lastrowid  # Recuperar o ID do documento inserido
            self.db.conn.commit()  # Confirmar a operação
            return documento_id
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao adicionar documento: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'

    def update_documento(self, documento_id, nome_arquivo, caminho_arquivo):
        cursor = self.db.conn.cursor(dictionary=True)
        query = "UPDATE documento SET Nome_Arquivo = %s, Caminho_Arquivo = %s WHERE ID = %s"
        try:
            cursor.execute(query, (nome_arquivo, caminho_arquivo, documento_id))
            self.db.conn.commit()  # Confirmar a operação
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao atualizar documento: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'

    def delete_documento(self, documento_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Deletar as referências na tabela evidencia primeiro
            delete_evidencia_query = "DELETE FROM evidencia WHERE ID_Documento = %s"
            cursor.execute(delete_evidencia_query, (documento_id,))

            # Deletar o documento na tabela documento
            delete_documento_query = "DELETE FROM documento WHERE ID = %s"
            cursor.execute(delete_documento_query, (documento_id,))
            self.db.conn.commit()  # Confirmar a operação
        except Exception as e:
            self.db.conn.rollback()  # Desfazer alterações em caso de erro
            print(f"Erro ao deletar documento: {e}")
            raise
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally'

    def get_documentos_by_projeto(self, id_projeto):
        cursor = self.db.conn.cursor(dictionary=True)
        query = "SELECT * FROM documento WHERE ID_Projeto = %s"
        cursor.execute(query, (id_projeto,))
        value = cursor.fetchall()
        cursor.close()
        return value
