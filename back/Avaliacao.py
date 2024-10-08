class Avaliacao:
    def __init__(self, db):
        self.db = db

    def adicionar_avaliacao(self, nome, descricao, id_nivel_solicitado, adjunto_emails, colaborador_emails, id_usuario, id_versao_modelo):
        try:

            cursor = self.db.conn.cursor(dictionary=True)
            query = """
                INSERT INTO avaliacao (Nome, Descricao, ID_Nivel_Solicitado, ID_Avaliador_Lider, ID_Atividade, ID_Versao_Modelo, ID_Status_Avaliacao) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (nome, descricao, id_nivel_solicitado, id_usuario, 1, id_versao_modelo, 1)
            cursor.execute(query, values)
            id_avaliacao = cursor.lastrowid

            query = """
                INSERT INTO usuarios_avaliacao (ID_Avaliacao, ID_Usuario, ID_Funcao) 
                VALUES (%s, %s, %s)
            """
            values = (id_avaliacao, id_usuario, 1)
            cursor.execute(query, values)
            def inserir_ou_linkar_usuario(email, id_funcao):
                query = "SELECT ID FROM usuario WHERE Email = %s"
                cursor.execute(query, (email,))
                usuario = cursor.fetchone()

                # Consumir quaisquer resultados pendentes
                cursor.fetchall()

                if usuario:
                    query = "INSERT INTO usuarios_avaliacao (ID_Avaliacao, ID_Usuario, ID_Funcao) VALUES (%s, %s, %s)"
                    cursor.execute(query, (id_avaliacao, usuario['ID'], id_funcao))
                    
                else:
                    query = "INSERT INTO usuario (Nome, Email, Senha, ID_Tipo) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, ("Usuário", email, "senha", id_funcao))
                    novo_usuario_id = cursor.lastrowid
                    query = "INSERT INTO usuarios_avaliacao (ID_Avaliacao, ID_Usuario, ID_Funcao) VALUES (%s, %s, %s)"
                    cursor.execute(query, (id_avaliacao, novo_usuario_id, id_funcao))
                    print(f"Simulação de envio de e-mail para {email} solicitando cadastro no sistema.")
                   
            for email in adjunto_emails:
                inserir_ou_linkar_usuario(email, 2)

            for email in colaborador_emails:
                inserir_ou_linkar_usuario(email, 5)

            self.db.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Erro ao adicionar avaliação: {e}")
            self.db.conn.rollback()
            cursor.close()
            raise

    def listar_avaliacoes(self, idAvaliador):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query_ids = "SELECT ID_Avaliacao FROM usuarios_avaliacao WHERE ID_Usuario = %s"
            values = (idAvaliador,)
            cursor.execute(query_ids, values)
            avaliacao_ids = cursor.fetchall()

            if not avaliacao_ids:
                print("Nenhum ID de avaliação encontrada")
                cursor.close()
                return []

            avaliacao_ids = [row['ID_Avaliacao'] for row in avaliacao_ids]

            placeholders = ','.join(['%s'] * len(avaliacao_ids))
            query = f"SELECT * FROM avaliacao WHERE ID IN ({placeholders}) order by ID DESC"
            cursor.execute(query, tuple(avaliacao_ids))
            result = cursor.fetchall()

            avaliacoes = [
                {
                    "id": row['ID'],
                    "nome": row['Nome'],
                    "descricao": row['Descricao'],
                    "id_avaliador_lider": row['ID_Avaliador_Lider'],
                    "id_atividade": row['ID_Atividade'],
                    "id_empresa": row['ID_Empresa'],
                    "id_nivel_solicitado": row['ID_Nivel_Solicitado'],
                    "id_versao_modelo": row['ID_Versao_Modelo'],
                    "id_status_avaliacao": row['ID_Status_Avaliacao']
                }
                for row in result
            ]
            cursor.close()
            return avaliacoes

        except Exception as e:
            print(f"Erro ao executar query: {e}")
            cursor.close()
            raise

    def obter_avaliacao(self, projeto_id):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            SELECT a.ID, a.Nome, a.Descricao, a.ID_Avaliador_Lider, u.Nome AS Nome_Avaliador_Lider, 
            atv.Descricao AS Descricao_Atividade, a.ID_Empresa, e.Nome AS Nome_Empresa, n.Nivel AS Nivel_Solicitado, 
            v.Nome AS Nome_Versao_Modelo, a.ID_Instituicao, a.Atividade_Planejamento, a.Cronograma_Planejamento, 
            a.Avaliacao_Aprovada_Pela_Softex, a.ID_Atividade, a.ID_Nivel_Solicitado, a.ID_Versao_Modelo, 
            r.descricao AS Descricao_Relatorio_Ajuste_Inicial, r.Caminho_Arquivo AS Caminho_Arquivo_Relatorio_Ajuste_Inicial, 
            tr.descricao AS Tipo_Relatorio_Ajuste_Inicial, a.Ata_Reuniao_Abertura, a.ID_Nivel_Atribuido, 
            n2.Nivel AS Nivel_Atribuido, a.Parecer_Final, a.ID_Status_Avaliacao
            FROM avaliacao a
            LEFT JOIN empresa e ON a.ID_Empresa = e.ID
            LEFT JOIN nivel_maturidade_mpsbr n ON a.ID_Nivel_Solicitado = n.ID
            LEFT JOIN nivel_maturidade_mpsbr n2 ON a.ID_Nivel_Atribuido = n2.ID
            LEFT JOIN usuario u ON a.ID_Avaliador_Lider = u.ID
            LEFT JOIN versao_modelo v ON a.ID_Versao_Modelo = v.ID
            LEFT JOIN atividade atv ON a.ID_Atividade = atv.ID
            LEFT JOIN relatorio r ON a.ID = r.ID_Avaliacao
            LEFT JOIN tipo_relatorio tr ON r.ID_Tipo = tr.ID
            WHERE a.ID = %s
        """
        cursor.execute(query, (projeto_id,))
        row = cursor.fetchone()
        # Consumir resultados pendentes
        cursor.fetchall()

        if row:
            avaliacao_data = {
                "id": row['ID'],
                "nome": row['Nome'],
                "descricao": row['Descricao'],
                "id_avaliador_lider": row['ID_Avaliador_Lider'],
                "nome_avaliador_lider": row['Nome_Avaliador_Lider'],
                "descricao_atividade": row['Descricao_Atividade'],
                "id_empresa": row['ID_Empresa'],
                "nome_empresa": row['Nome_Empresa'],
                "nivel_solicitado": row['Nivel_Solicitado'],
                "nome_versao_modelo": row['Nome_Versao_Modelo'],
                "id_instituicao": row['ID_Instituicao'],
                "atividade_planejamento": row['Atividade_Planejamento'],
                "cronograma_planejamento": row['Cronograma_Planejamento'],
                "aprovacao_softex": row['Avaliacao_Aprovada_Pela_Softex'],
                "id_atividade": row['ID_Atividade'],
                "id_nivel_solicitado": row['ID_Nivel_Solicitado'],
                "id_versao_modelo": row['ID_Versao_Modelo'],
                "descricao_relatorio_ajuste_inicial": row['Descricao_Relatorio_Ajuste_Inicial'],
                "caminho_arquivo_relatorio_ajuste_inicial": row['Caminho_Arquivo_Relatorio_Ajuste_Inicial'],
                "tipo_relatorio_ajuste_inicial": row['Tipo_Relatorio_Ajuste_Inicial'],
                "ata_reuniao_abertura": row['Ata_Reuniao_Abertura'],
                "id_nivel_atribuido": row['ID_Nivel_Atribuido'],
                "nivel_atribuido": row['Nivel_Atribuido'],
                "parecer_final": row['Parecer_Final'],                
                "id_status_avaliacao": row['ID_Status_Avaliacao']
            }
            cursor.close()
            return avaliacao_data
        else:
            print(f"Erro: A consulta não retornou os campos esperados. Resultado da consulta: {row}")
            cursor.close()
            return None

    def deletar_avaliacao(self, projeto_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "DELETE FROM avaliacao WHERE ID = %s"
            cursor.execute(query, (projeto_id,))
            
            # Confirmar a exclusão
            self.db.conn.commit()
        except Exception as e:
            # Desfazer mudanças se houver erro
            self.db.conn.rollback()
            print(f"Erro ao deletar avaliação: {e}")
        finally:
            cursor.close()

    def atualizar_avaliacao(self, projeto_id, novo_nome, nova_descricao, novo_id_avaliador_lider, novo_id_status_avaliacao, novo_modelo, novo_id_atividade, novo_id_empresa, novo_id_nivel_solicitado, novo_id_nivel_atribuido, novo_parece_nivel_final):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE avaliacao SET Nome = %s, Descricao = %s, ID_Avaliador_Lider = %s, ID_Status_Avaliacao = %s, 
                Modelo = %s, ID_Atividade = %s, ID_Empresa = %s, ID_Nivel_Solicitado = %s, 
                ID_Nivel_Atribuido = %s, Parece_Nivel_Final = %s WHERE ID = %s
            """
            values = (novo_nome, nova_descricao, novo_id_avaliador_lider, novo_id_status_avaliacao, novo_modelo, novo_id_atividade, novo_id_empresa, novo_id_nivel_solicitado, novo_id_nivel_atribuido, novo_parece_nivel_final, projeto_id)
            cursor.execute(query, values)
            
            # Confirmar a atualização
            self.db.conn.commit()
        except Exception as e:
            # Desfazer mudanças em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar avaliação: {e}")
        finally:
            cursor.close()
    def atualizar_id_atividade(self, projeto_id, nova_id_atividade):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "UPDATE avaliacao SET ID_Atividade = %s WHERE ID = %s"
            cursor.execute(query, (nova_id_atividade, projeto_id))
            
            # Confirmar a atualização
            self.db.conn.commit()
        except Exception as e:
            # Desfazer mudanças se houver erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar ID da atividade: {e}")
        finally:
            cursor.close()


    def inserir_planejamento(self, projeto_id, aprovacaoSoftex, atividade_planejamento, cronograma_planejamento):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE avaliacao SET Avaliacao_Aprovada_Pela_Softex = %s, 
                Atividade_Planejamento = %s, Cronograma_Planejamento = %s WHERE ID = %s
            """
            values = (aprovacaoSoftex, atividade_planejamento, cronograma_planejamento, projeto_id)
            cursor.execute(query, values)
            
            # Confirmar a inserção
            self.db.conn.commit()
        except Exception as e:
            # Desfazer mudanças se houver erro
            self.db.conn.rollback()
            print(f"Erro ao inserir planejamento: {e}")
        finally:
            cursor.close()

    def inserir_ata_reuniao(self, projeto_id, ata_reuniao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "UPDATE avaliacao SET Ata_Reuniao_Abertura = %s WHERE ID = %s"
            values = (ata_reuniao, projeto_id)
            cursor.execute(query, values)
            
            # Confirmar as mudanças no banco de dados
            self.db.conn.commit()
        except Exception as e:
            # Se ocorrer um erro, desfaz as alterações
            self.db.conn.rollback()
            print(f"Erro ao inserir ata de reunião: {e}")
        finally:
            cursor.close()

    def salvar_apresentacao_equipe(self, id_avaliacao, apresentacao_inicial, equipe_treinada):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE avaliacao 
                SET Apresentacao_Inicial = %s, Equipe_Treinada = %s
                WHERE ID = %s
            """
            values = (apresentacao_inicial, equipe_treinada, id_avaliacao)
            cursor.execute(query, values)
            
            # Confirmar a operação
            self.db.conn.commit()
        except Exception as e:
            # Desfazer alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao salvar apresentação inicial e equipe treinada: {e}")
            raise e
        finally:
            cursor.close()

    def get_apresentacao_equipe(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT Apresentacao_Inicial, Equipe_Treinada
                FROM avaliacao
                WHERE ID = %s
            """
            cursor.execute(query, (id_avaliacao,))
            result = cursor.fetchone()
            cursor.fetchall()  # Consumir quaisquer resultados pendentes
            print(result)
            if result:
                cursor.close()
                return {
                    "apresentacao_inicial": bool(result['Apresentacao_Inicial']),
                    "equipe_treinada": bool(result['Equipe_Treinada'])
                }
            else:
                cursor.close()
                return None
        except Exception as e:
            print(f"Erro ao buscar apresentação inicial e equipe treinada: {e}")
            cursor.close()
            raise

    def atualizar_avaliacao_ajuste_inicial(self, avaliacao_id, descricao, cronograma_planejamento, atividade_planejamento):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE avaliacao 
                SET Descricao = %s, Cronograma_Planejamento = %s, Atividade_Planejamento = %s 
                WHERE ID = %s
            """
            values = (descricao, cronograma_planejamento, atividade_planejamento, avaliacao_id)
            cursor.execute(query, values)
            
            # Confirmar a operação
            self.db.conn.commit()
        except Exception as e:
            # Desfazer alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar avaliação: {e}")
            raise e
        finally:
            cursor.close()

    def adicionar_data_avaliacao_final(self, id_avaliacao, data_avaliacao_final):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "UPDATE avaliacao SET data_avaliacao_final = %s WHERE ID = %s"
            cursor.execute(query, (data_avaliacao_final, id_avaliacao))
            
            # Confirmar a operação
            self.db.conn.commit()
        except Exception as e:
            # Desfazer alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao adicionar data da avaliação final: {e}")
            raise e
        finally:
            cursor.close()

    def obter_data_avaliacao_final(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "SELECT data_avaliacao_final FROM avaliacao WHERE ID = %s"
            cursor.execute(query, (id_avaliacao,))
            data_avaliacao_final = cursor.fetchone()
            cursor.fetchall()  # Consumir quaisquer resultados pendentes
            cursor.close()
            return data_avaliacao_final['data_avaliacao_final'] if data_avaliacao_final else None
        except Exception as e:
            print(f"Erro ao obter data da avaliação final: {e}")
            cursor.close()
            raise

    def atualizar_data_avaliacao_final(self, id_avaliacao, nova_data_avaliacao_final):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "UPDATE avaliacao SET data_avaliacao_final = %s WHERE ID = %s"
            cursor.execute(query, (nova_data_avaliacao_final, id_avaliacao))
            
            # Confirmar a operação
            self.db.conn.commit()
        except Exception as e:
            # Desfazer alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar data da avaliação final: {e}")
            raise e
        finally:
            cursor.close()

    def update_resultado_final(self, id_avaliacao, parecer_final, id_nivel_atribuido):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "UPDATE avaliacao SET Parecer_Final = %s, ID_Nivel_Atribuido = %s WHERE ID = %s"
            values = (parecer_final, id_nivel_atribuido, id_avaliacao)
            cursor.execute(query, values)
            
            # Confirmar a operação
            self.db.conn.commit()
        except Exception as e:
            # Desfazer alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar resultado final: {e}")
            raise e
        finally:
            cursor.close()


    def atualizar_status_avaliacao(self, id_avaliacao, id_status):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                UPDATE avaliacao SET ID_Status_Avaliacao = %s WHERE ID = %s
            """
            values = (id_status, id_avaliacao)
            cursor.execute(query, values)
            
            # Confirmar a atualização
            self.db.conn.commit()
        except Exception as e:
            # Desfazer mudanças em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar avaliação: {e}")
        finally:
            cursor.close()