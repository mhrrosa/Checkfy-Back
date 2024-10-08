class GrauImplementacao:
    def __init__(self, db):
        self.db = db

    def add_graus_implementacao_empresa(self, valores):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
        INSERT INTO grau_implementacao_processo_unidade_organizacional 
        (ID_Avaliacao, ID_Resultado_Esperado, Nota) 
        VALUES (%s, %s, %s)
        """
        try:
            # Executa a inserção de múltiplos valores ao mesmo tempo
            cursor.executemany(query, valores)
            self.db.conn.commit()  # Confirma a operação no banco de dados
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao adicionar os graus de implementação: {e}")
            raise
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def get_grau_implementacao_empresa(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query_graus = "SELECT * FROM grau_implementacao_processo_unidade_organizacional WHERE ID_Avaliacao = %s"
            cursor.execute(query_graus, (id_avaliacao,))
            graus = cursor.fetchall()

            # Verificar se a consulta retornou algo
            if not graus:
                return None  # Retorna uma mensagem informando que não encontrou nada
            
            graus_implementacao = []
            for grau in graus:
                grau_dict = {
                    'ID': grau['ID'],
                    'ID_Resultado_Esperado': grau['ID_Resultado_Esperado'],
                    'Nota': grau['Nota'],
                    'ID_Avaliacao': grau['ID_Avaliacao'],
                }
                graus_implementacao.append(grau_dict)
            cursor.close()
            return graus_implementacao

        except Exception as e:
            print(f"Erro ao buscar graus de implementação: {e}")
            raise

    def update_graus_implementacao_empresa_batch(self, update_data):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            UPDATE grau_implementacao_processo_unidade_organizacional
            SET Nota = %s
            WHERE ID_Avaliacao = %s AND ID_Resultado_Esperado = %s
        """
        try:
            # Executa a atualização para cada item no batch de dados
            cursor.executemany(query, update_data)
            self.db.conn.commit()  # Confirma a operação no banco de dados
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao atualizar grau de implementação: {e}")
            raise
        finally:
            cursor.close()  # Garante que o cursor será fechado