class ResultadoEsperado:
    def __init__(self, db):
        self.db = db

    def add_resultado_esperado(self, descricao, id_nivel_intervalo_inicio, id_nivel_intervalo_fim, id_processo):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            INSERT INTO resultado_esperado_mpsbr 
            (Descricao, ID_Nivel_Intervalo_Inicio, ID_Nivel_Intervalo_Fim, ID_Processo) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (descricao, id_nivel_intervalo_inicio, id_nivel_intervalo_fim, id_processo))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Reverte a operação em caso de erro
            print(f"Erro ao adicionar resultado esperado: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def update_resultado_esperado(self, resultado_id, nova_descricao, novo_id_nivel_intervalo_inicio, novo_id_nivel_intervalo_fim, novo_id_processo):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            UPDATE resultado_esperado_mpsbr 
            SET Descricao = %s, ID_Nivel_Intervalo_Inicio = %s, ID_Nivel_Intervalo_Fim = %s, ID_Processo = %s 
            WHERE ID = %s
        """
        try:
            cursor.execute(query, (nova_descricao, novo_id_nivel_intervalo_inicio, novo_id_nivel_intervalo_fim, novo_id_processo, resultado_id))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Reverte a operação em caso de erro
            print(f"Erro ao atualizar resultado esperado: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor
    def delete_resultado_esperado(self, resultado_id):
        cursor = self.db.conn.cursor(dictionary=True)
        query = "DELETE FROM resultado_esperado_mpsbr WHERE ID = %s"
        try:
            cursor.execute(query, (resultado_id,))
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Reverte a operação em caso de erro
            print(f"Erro ao deletar resultado esperado: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def get_resultados_esperados(self, id_processos):
        placeholders = ', '.join(['%s'] * len(id_processos))
        resultados = self.db.fetch_all(f"SELECT * FROM resultado_esperado_mpsbr WHERE ID_Processo IN ({placeholders})", tuple(id_processos))
        return resultados