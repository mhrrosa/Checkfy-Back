class Projeto:
    def __init__(self, db):
        self.db = db

    def add_projeto(self, id_avaliacao, nome_projeto, projeto_habilitado, numero_projeto):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            INSERT INTO projeto 
            (ID_Avaliacao, Nome_Projeto, Projeto_Habilitado, Numero_Projeto) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (id_avaliacao, nome_projeto, projeto_habilitado, numero_projeto))
            self.db.conn.commit()  # Confirma a transação
            value = cursor.lastrowid  # Obtém o ID do último projeto inserido
            return value
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao adicionar projeto: {e}")
            raise e
        finally:
            cursor.close()
    def get_projetos_by_id_avaliacao(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        query_projetos = "SELECT * FROM projeto WHERE ID_Avaliacao = %s"
        
        cursor.execute(query_projetos, (id_avaliacao,))
        projetos = cursor.fetchall()

        projetos_com_documentos = []
        for projeto in projetos:
            query_documentos = """
            SELECT d.ID, d.Caminho_Arquivo, d.Nome_Arquivo, d.ID_Projeto 
            FROM documento d 
            WHERE d.ID_Projeto = %s
            """
            cursor.execute(query_documentos, (projeto['ID'],))
            documentos = cursor.fetchall()
            projetos_com_documentos.append({
                'ID': projeto['ID'],
                'ID_Avaliacao': projeto['ID_Avaliacao'],
                'Projeto_Habilitado': projeto['Projeto_Habilitado'],
                'Numero_Projeto': projeto['Numero_Projeto'],
                'Nome_Projeto': projeto['Nome_Projeto'],
                'Documentos': [
                    {
                        'ID': doc['ID'],
                        'Caminho_Arquivo': doc['Caminho_Arquivo'],
                        'Nome_Arquivo': doc['Nome_Arquivo'],
                        'ID_Projeto': doc['ID_Projeto']
                    } for doc in documentos
                ]
            })
        cursor.close()
        return projetos_com_documentos

    def update_projeto(self, projeto_id, nome_projeto, projeto_habilitado):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            UPDATE projeto 
            SET Nome_Projeto = %s, Projeto_Habilitado = %s 
            WHERE ID = %s
        """
        try:
            cursor.execute(query, (nome_projeto, projeto_habilitado, projeto_id))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar projeto: {e}")
            raise e
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def get_next_numero_projeto(self, id_avaliacao):
        try:
            cursor = self.db.conn.cursor(dictionary=True)
            query = "SELECT MAX(Numero_Projeto) as Numero_Projeto FROM projeto WHERE ID_Avaliacao = %s"
            cursor.execute(query, (id_avaliacao,))
            row = cursor.fetchone()
            
            # Consumir resultados pendentes
            cursor.fetchall()
            cursor.close()

            # Tratamento para valores None
            next_numero_projeto = (row['Numero_Projeto'] or 0) + 1 if row and row['Numero_Projeto'] is not None else 1
           
            
            return next_numero_projeto

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None