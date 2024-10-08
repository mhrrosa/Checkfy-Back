class Auditor:
    def __init__(self, db):
        self.db = db

    def adicionar_auditor(self, id_avaliacao, auditor_emails):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            def inserir_ou_linkar_usuario(email, id_funcao):
                # Verificar se o usuário já existe
                query = "SELECT ID FROM usuario WHERE Email = %s"
                cursor.execute(query, (email,))
                usuario = cursor.fetchone()  # Apenas use fetchone() aqui
                
                if usuario:
                    # Se o usuário já existir, vinculá-lo à avaliação
                    query = "INSERT INTO usuarios_avaliacao (ID_Avaliacao, ID_Usuario, ID_Funcao) VALUES (%s, %s, %s)"
                    cursor.execute(query, (id_avaliacao, usuario['ID'], id_funcao))
                else:
                    # Se o usuário não existir, criar um novo usuário e vinculá-lo
                    query = "INSERT INTO usuario (Nome, Email, Senha, ID_Tipo) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, ("Usuário", email, "senha", id_funcao))
                    novo_usuario_id = cursor.lastrowid
                    query = "INSERT INTO usuarios_avaliacao (ID_Avaliacao, ID_Usuario, ID_Funcao) VALUES (%s, %s, %s)"
                    cursor.execute(query, (id_avaliacao, novo_usuario_id, id_funcao))
                    print(f"Simulação de envio de e-mail para {email} solicitando cadastro no sistema.")

            # Iterar sobre os e-mails e aplicar a função para cada auditor
            for email in auditor_emails:
                inserir_ou_linkar_usuario(email, 3)

            # Confirmar a operação
            self.db.conn.commit()
        except Exception as e:
            # Desfazer as alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao adicionar auditores: {e}")
            raise e
        finally:
            cursor.close()

    def get_email_auditor(self, avaliacao_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Obter o ID_Usuario da tabela usuarios_avaliacao com ID_Funcao = 3
            query = """
                SELECT ID_Usuario 
                FROM usuarios_avaliacao 
                WHERE ID_Avaliacao = %s AND ID_Funcao = 3
            """
            cursor.execute(query, (avaliacao_id,))
            id_usuario = cursor.fetchone()
            # Garantir que todos os resultados anteriores sejam lidos ou descartados
            cursor.fetchall()  # Descarta qualquer resultado não processado

            if id_usuario:
                # Agora, buscar o e-mail do usuário na tabela usuario
                query_email = """
                    SELECT Email 
                    FROM usuario 
                    WHERE ID = %s
                """
                cursor.execute(query_email, (id_usuario['ID_Usuario'],))
                email = cursor.fetchone()
                cursor.close()
                if email:
                    return email['Email']
                else:
                    return None
            else:
                cursor.close()
                return None
        except Exception as e:
            print(f"Erro ao buscar e-mail do auditor: {e}")
            cursor.close()
            raise e

    def update_email_auditor(self, avaliacao_id, novo_email):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Atualizar o e-mail do auditor usando apenas uma query
            query = """
                UPDATE usuario u
                JOIN usuarios_avaliacao ua ON u.ID = ua.ID_Usuario
                SET u.Email = %s
                WHERE ua.ID_Avaliacao = %s AND ua.ID_Funcao = 3
            """
            rows_affected = cursor.execute(query, (novo_email, avaliacao_id))
            
            # Confirmar a operação
            self.db.conn.commit()
            
            # Verificar se alguma linha foi afetada (se o auditor foi encontrado)
            if rows_affected == 0:
                raise Exception("Auditor não encontrado para essa avaliação")
        except Exception as e:
            # Desfazer as alterações em caso de erro
            self.db.conn.rollback()
            print(f"Erro ao atualizar e-mail do auditor: {e}")
            raise e
        finally:
            cursor.close()