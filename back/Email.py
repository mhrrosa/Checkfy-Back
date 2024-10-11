
'''
        S: ajmCheckfy_0
        vhgx tcej ayum ltxq
'''
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def __init__(self, db):
        self.db = db
    
    def email_aprovar_softex(self, id_avaliacao):
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

        try:
            cursor.execute(query, (id_avaliacao,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                # Extraindo dados da avaliação
                id = row['ID']
                nome = row['Nome']
                descricao = row['Descricao']
                nome_avaliador_lider = row['Nome_Avaliador_Lider']
                descricao_atividade =  row['Descricao_Atividade']
                nome_empresa = row['Nome_Empresa']
                nivel_solicitado =row['Nivel_Solicitado']
                nome_versao_modelo = row['Nome_Versao_Modelo']

                # Configurando o e-mail
                remetente = "checkfyadm@gmail.com"
                destinatario = "checkfyadm@gmail.com"
                assunto = "Solicitação de Aprovação da Softex - Avaliação ID {}".format(id)
                
                corpo = f"""
                Prezado(a) Softex,

                Gostaríamos de solicitar a sua aprovação para a seguinte avaliação, conforme os dados abaixo:

                Nome da Avaliação: {nome}
                Descrição: {descricao}
                Avaliador Líder: {nome_avaliador_lider}
                Empresa: {nome_empresa}
                Nível Solicitado: {nivel_solicitado}
                Versão do Modelo: {nome_versao_modelo}

                Por favor, verifique os dados e aprove para que possamos iniciar a avaliação.

                Atenciosamente,
                Equipe de Avaliação
                """

                # Criando a mensagem de e-mail
                mensagem = MIMEMultipart()
                mensagem['From'] = remetente
                mensagem['To'] = destinatario
                mensagem['Subject'] = assunto
                mensagem.attach(MIMEText(corpo, 'plain'))

                # Enviando o e-mail via servidor SMTP do Gmail
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(remetente, "vhgxtcejayumltxq")
                        server.send_message(mensagem)
                    print("E-mail enviado com sucesso!")
                except Exception as e:
                    print(f"Erro ao enviar e-mail: {e}")
            else:
                print('Avaliação não encontrada')
        except Exception as e:
            print(f"Erro ao buscar avaliação no banco de dados: {e}")
            raise e
    

    def enviar_email_auditor_avaliacao_inicial(self, id_avaliacao, email_auditor):
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


        try:
            cursor.execute(query, (id_avaliacao,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                # Extraindo dados da avaliação
                id = row['ID']
                nome = row['Nome']
                descricao = row['Descricao']
                nome_avaliador_lider = row['Nome_Avaliador_Lider']
                descricao_atividade =  row['Descricao_Atividade']
                nome_empresa = row['Nome_Empresa']
                nivel_solicitado =row['Nivel_Solicitado']
                nome_versao_modelo = row['Nome_Versao_Modelo']
                # Configurando o e-mail
                remetente = "checkfyadm@gmail.com"
                destinatario = email_auditor
                assunto = f"Informações da Avaliação Inicial - ID {id}"

                
                corpo = f"""
                Prezado(a) Auditor(a),

                Você foi designado para realizar a auditoria da avaliação inicial. Seguem as informações da avaliação:

                - ID da Avaliação: {id}
                - Nome da Avaliação: {nome}
                - Descrição: {descricao}
                - Nome do Avaliador Líder: {nome_avaliador_lider}
                - Nome da Empresa: {nome_empresa}
                - Nível Solicitado: {nivel_solicitado}

                Solicitamos que acesse o sistema para dar início ao processo de auditoria conforme as informações apresentadas. Caso tenha alguma dúvida ou necessite de informações adicionais, 
                por favor, entre em contato com o avaliador líder.

                Atenciosamente,

                Equipe de Avaliação
                """

                # Criando a mensagem de e-mail
                mensagem = MIMEMultipart()
                mensagem['From'] = remetente
                mensagem['To'] = destinatario
                mensagem['Subject'] = assunto
                mensagem.attach(MIMEText(corpo, 'plain'))

                # Enviando o e-mail via servidor SMTP do Gmail
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(remetente, "vhgxtcejayumltxq")
                        server.send_message(mensagem)
                    print("E-mail enviado com sucesso!")
                except Exception as e:
                    print(f"Erro ao enviar e-mail: {e}")
            else:
                print('Avaliação não encontrada')
        except Exception as e:
            print(f"Erro ao buscar avaliação no banco de dados: {e}")
            raise e
    
    def enviar_email_auditor_data_avaliacao_final(self, id_avaliacao, email_auditor):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            SELECT a.ID, a.Nome, a.data_avaliacao_final, u.Nome
            FROM avaliacao a
            LEFT JOIN usuario u ON a.ID_Avaliador_Lider = u.ID
            WHERE a.ID = %s
        """

        try:
            cursor.execute(query, (id_avaliacao,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                # Extraindo dados da avaliação
                id = row['ID']
                nome = row['Nome']
                data_avaliacao_final = row['data_avaliacao_final']
                nome_avaliador_lider = row['Nome']

                # Convertendo e formatando a data para o formato dia/mês/ano
                try:
                    data_avaliacao_final_formatada = data_avaliacao_final.strftime('%d/%m/%Y')
                except:
                    data_avaliacao_final_formatada = data_avaliacao_final

                # Configurando o e-mail
                remetente = "checkfyadm@gmail.com"
                destinatario = email_auditor
                assunto = f"Data da Avaliação Final - ID {id}"

                corpo = f"""
                Prezado(a) Auditor(a),

                Informamos que a data da avaliação final para a avaliação ID {id} - {nome} foi agendada para {data_avaliacao_final_formatada}.

                Avaliador Líder: {nome_avaliador_lider}

                Caso tenha alguma dúvida, por favor, entre em contato com o avaliador líder.

                Atenciosamente,

                Equipe de Avaliação
                """

                # Criando a mensagem de e-mail
                mensagem = MIMEMultipart()
                mensagem['From'] = remetente
                mensagem['To'] = destinatario
                mensagem['Subject'] = assunto
                mensagem.attach(MIMEText(corpo, 'plain'))

                # Enviando o e-mail via servidor SMTP do Gmail
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(remetente, "vhgxtcejayumltxq")
                        server.send_message(mensagem)
                    print("E-mail enviado com sucesso!")
                except Exception as e:
                    print(f"Erro ao enviar e-mail: {e}")
            else:
                print('Avaliação não encontrada')
        except Exception as e:
            print(f"Erro ao buscar avaliação no banco de dados: {e}")
            raise e

    def solicitar_link_formulario_feedback(self, id_avaliacao):

        remetente = "checkfyadm@gmail.com"
        destinatario = "checkfyadm@gmail.com"
        assunto = "Solicitação de Link do Formulário de Feedback"

        corpo = f"""
        Prezado(a) Softex,

        Estamos entrando em contato para solicitar o link do formulário de feedback referente a avaliação ID: {id_avaliacao}.

        Agradecemos pela atenção e aguardamos o envio do link.

        Atenciosamente,

        Equipe de Avaliação
        """

        # Criando a mensagem de e-mail
        mensagem = MIMEMultipart()
        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto
        mensagem.attach(MIMEText(corpo, 'plain'))

        # Enviando o e-mail via servidor SMTP do Gmail
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(remetente, "vhgxtcejayumltxq")
                server.send_message(mensagem)
            print("E-mail de solicitação de link do formulário de feedback enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
    
    def notificar_participantes_resultado_avaliacao_inicial(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Consultar os participantes da avaliação na tabela usuarios_avaliacao
            query_participantes = """
            SELECT u.Email
            FROM usuarios_avaliacao ua
            JOIN usuario u ON ua.ID_Usuario = u.ID
            WHERE ua.ID_Avaliacao = %s
            """
            
            # Executando a consulta com o parâmetro
            cursor.execute(query_participantes, (id_avaliacao,))
            participantes = cursor.fetchall()
            cursor.close()
            if participantes:
                # Iterar sobre cada participante e enviar um e-mail de notificação
                for participante in participantes:
                    email_participante = participante['Email']

                    remetente = "checkfyadm@gmail.com"
                    destinatario = email_participante
                    assunto = "Resultado da Avaliação Final"

                    corpo = f"""
                    Prezado(a),

                    Informamos que o resultado da avaliação inicial para a avaliação de ID {id_avaliacao} foi concluído.

                    Por favor, acesse o sistema para visualizar o resultado detalhado.

                    Atenciosamente,

                    Equipe de Avaliação
                    """

                    # Criando a mensagem de e-mail
                    mensagem = MIMEMultipart()
                    mensagem['From'] = remetente
                    mensagem['To'] = destinatario
                    mensagem['Subject'] = assunto
                    mensagem.attach(MIMEText(corpo, 'plain'))

                    # Enviando o e-mail via servidor SMTP do Gmail
                    try:
                        with smtplib.SMTP('smtp.gmail.com', 587) as server:
                            server.starttls()
                            server.login(remetente, "vhgxtcejayumltxq")
                            server.send_message(mensagem)
                        print(f"E-mail enviado com sucesso para {email_participante}!")
                    except Exception as e:
                        print(f"Erro ao enviar e-mail para {email_participante}: {e}")
            else:
                print("Nenhum participante encontrado para esta avaliação.")
        except Exception as e:
            print(f"Erro ao buscar participantes da avaliação no banco de dados: {e}")
            raise e

    def enviar_email_auditor_avaliacao_final(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        query_avaliacao = """
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

        
        query_auditor = """
            SELECT u.Email
            FROM usuarios_avaliacao ua
            JOIN usuario u ON ua.ID_Usuario = u.ID
            WHERE ua.ID_Avaliacao = %s AND ua.ID_Funcao = 3
        """
        
        try:
            # Buscar dados da avaliação
            cursor.execute(query_avaliacao, (id_avaliacao,))
            row = cursor.fetchone()
            cursor.fetchall()
          
            if row:
                # Extraindo dados da avaliação
                id = row['ID']
                nome = row['Nome']
                descricao = row['Descricao']
                nome_avaliador_lider = row['Nome_Avaliador_Lider']
                descricao_atividade =  row['Descricao_Atividade']
                nome_empresa = row['Nome_Empresa']
                nivel_solicitado =row['Nivel_Solicitado']
                nome_versao_modelo = row['Nome_Versao_Modelo']

                # Buscar o e-mail do auditor (ID_Funcao = 3)
                cursor.close()
                
                cursor = self.db.conn.cursor(dictionary=True)
                cursor.execute(query_auditor, (id_avaliacao,))
                email_auditor_row = cursor.fetchone()
                cursor.fetchall()
                cursor.close()

                if email_auditor_row:
                    email_auditor = email_auditor_row['Email']
                else:
                    print("E-mail do auditor não encontrado.")
                    return
                
                print(email_auditor)

                # Configurando o e-mail
                remetente = "checkfyadm@gmail.com"
                destinatario = email_auditor
                assunto = f"Informações da Avaliação Final - ID {id}"

                corpo = f"""
                Prezado(a) Auditor(a),

                Você foi designado para realizar a auditoria da avaliação final. Seguem as informações da avaliação:

                - ID da Avaliação: {id}
                - Nome da Avaliação: {nome}
                - Descrição: {descricao}
                - Nome do Avaliador Líder: {nome_avaliador_lider}
                - Nome da Empresa: {nome_empresa}
                - Nível Solicitado: {nivel_solicitado}

                Solicitamos que acesse o sistema para dar início ao processo de auditoria conforme as informações apresentadas. Caso tenha alguma dúvida ou necessite de informações adicionais, 
                por favor, entre em contato com o avaliador líder.

                Atenciosamente,

                Equipe de Avaliação
                """

                # Criando a mensagem de e-mail
                mensagem = MIMEMultipart()
                mensagem['From'] = remetente
                mensagem['To'] = destinatario
                mensagem['Subject'] = assunto
                mensagem.attach(MIMEText(corpo, 'plain'))

                # Enviando o e-mail via servidor SMTP do Gmail
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(remetente, "vhgxtcejayumltxq")
                        server.send_message(mensagem)
                    print("E-mail enviado com sucesso!")
                except Exception as e:
                    print(f"Erro ao enviar e-mail: {e}")
            else:
                print('Avaliação não encontrada')
        except Exception as e:
            print(f"Erro ao buscar avaliação no banco de dados: {e}")
            raise e
        
    def notificar_participantes_resultado_avaliacao_final(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Consultar os participantes da avaliação na tabela usuarios_avaliacao
            query_participantes = """
            SELECT u.Email
            FROM usuarios_avaliacao ua
            JOIN usuario u ON ua.ID_Usuario = u.ID
            WHERE ua.ID_Avaliacao = %s
            """
            
            # Executando a consulta com o parâmetro
            cursor.execute(query_participantes, (id_avaliacao,))
            participantes = cursor.fetchall()

            if participantes:
                # Iterar sobre cada participante e enviar um e-mail de notificação
                for participante in participantes:
                    email_participante = participante['Email']

                    remetente = "checkfyadm@gmail.com"
                    destinatario = email_participante
                    assunto = "Resultado da Avaliação Final"

                    corpo = f"""
                    Prezado(a),

                    Informamos que o resultado da avaliação final para a avaliação de ID {id_avaliacao} foi concluído.

                    Por favor, acesse o sistema para visualizar o resultado detalhado.

                    Atenciosamente,

                    Equipe de Avaliação
                    """

                    # Criando a mensagem de e-mail
                    mensagem = MIMEMultipart()
                    mensagem['From'] = remetente
                    mensagem['To'] = destinatario
                    mensagem['Subject'] = assunto
                    mensagem.attach(MIMEText(corpo, 'plain'))

                    # Enviando o e-mail via servidor SMTP do Gmail
                    try:
                        with smtplib.SMTP('smtp.gmail.com', 587) as server:
                            server.starttls()
                            server.login(remetente, "vhgxtcejayumltxq")
                            server.send_message(mensagem)
                        print(f"E-mail enviado com sucesso para {email_participante}!")
                    except Exception as e:
                        print(f"Erro ao enviar e-mail para {email_participante}: {e}")
            else:
                print("Nenhum participante encontrado para esta avaliação.")
        except Exception as e:
            print(f"Erro ao buscar participantes da avaliação no banco de dados: {e}")
            raise e