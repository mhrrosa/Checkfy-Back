class Relatorio:
    def __init__(self, db):
        self.db = db

    def inserir_relatorio_inicial(self, descricao, id_avaliacao, caminho_arquivo):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                INSERT INTO relatorio (Descricao, ID_Tipo, ID_Avaliacao, Caminho_Arquivo)
                VALUES (%s, %s, %s, %s)
            """
            values = (descricao, 1, id_avaliacao, caminho_arquivo)
            cursor.execute(query, values)
            value = cursor.lastrowid
            self.db.conn.commit()  # Confirma a transação
            return value
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao inserir relatório: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def atualizar_relatorio_inicial(self, descricao, id_avaliacao, caminho_arquivo):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE relatorio
                SET Descricao = %s, Caminho_Arquivo = %s
                WHERE ID_Avaliacao = %s AND ID_Tipo = 1
            """
            values = (descricao, caminho_arquivo, id_avaliacao)
            cursor.execute(query, values)
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar relatório: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def obter_relatorio_inicial(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT Descricao, Caminho_Arquivo
                FROM relatorio
                WHERE ID_Avaliacao = %s AND ID_Tipo = 1
            """
            cursor.execute(query, (id_avaliacao,))
            result = cursor.fetchone()
            # Consumir quaisquer resultados pendentes
            cursor.fetchall()
            cursor.close()
            if result:
                return {"descricao": result['Descricao'], "caminhoArquivo": result['Caminho_Arquivo']}
            return None
        except Exception as e:
            cursor.close()
            print(f"Erro ao obter relatório: {e}")
            raise
    
    # Métodos para a ata de reunião de abertura
    def inserir_ata_abertura(self, descricao, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                INSERT INTO relatorio (Descricao, ID_Tipo, ID_Avaliacao, Caminho_Arquivo)
                VALUES (%s, %s, %s, %s)
            """
            values = (descricao, 2, id_avaliacao, 'não existe')
            cursor.execute(query, values)
            value = cursor.lastrowid
            self.db.conn.commit()  # Confirma a transação
            return value
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao inserir ata de abertura: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def atualizar_ata_abertura(self, descricao, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE relatorio
                SET Descricao = %s, Caminho_Arquivo = %s
                WHERE ID_Avaliacao = %s AND ID_Tipo = 2
            """
            values = (descricao, 'não existe', id_avaliacao)
            cursor.execute(query, values)
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar ata de abertura: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def obter_ata_abertura(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT Descricao, Caminho_Arquivo
                FROM relatorio
                WHERE ID_Avaliacao = %s AND ID_Tipo = 2
            """
            cursor.execute(query, (id_avaliacao,))
            result = cursor.fetchone()
            # Consumir quaisquer resultados pendentes
            cursor.fetchall()
            cursor.close()
            if result:
                return {"descricao": result['Descricao'], "caminhoArquivo": result['Caminho_Arquivo']}
            return None
        except Exception as e:
            cursor.close()
            print(f"Erro ao obter ata de abertura: {e}")
            raise

    def inserir_relatorio_auditoria_final(self, descricao, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                INSERT INTO relatorio (Descricao, ID_Tipo, ID_Avaliacao, Caminho_Arquivo)
                VALUES (%s, %s, %s, %s)
            """
            values = (descricao, 2, id_avaliacao, 'Não existe')
            cursor.execute(query, values)
            relatorio_id = cursor.lastrowid
            self.db.conn.commit()  # Confirma a transação
            return relatorio_id
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao inserir relatório: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def atualizar_relatorio_auditoria_final(self, descricao, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE relatorio
                SET Descricao = %s
                WHERE ID_Avaliacao = %s AND ID_Tipo = 2
            """
            values = (descricao, id_avaliacao)
            cursor.execute(query, values)
            self.db.conn.commit()  # Confirma a transação
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a operação em caso de erro
            print(f"Erro ao atualizar relatório: {e}")
            raise e
        finally:
            cursor.close()  # Garante o fechamento do cursor

    def get_relatorio_auditoria_final(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT Descricao
                FROM relatorio
                WHERE ID_Avaliacao = %s AND ID_Tipo = 2
            """
            cursor.execute(query, (id_avaliacao,))
            result = cursor.fetchone()
            # Consumir quaisquer resultados pendentes
            cursor.fetchall()
            cursor.close()
            if result:
                return {"descricao": result['Descricao']}
            return None
        except Exception as e:
            print(f"Erro ao obter relatório: {e}")
            cursor.close()
            raise
