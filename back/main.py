from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
import mysql.connector
from back.Nivel import Nivel
from back.Processo import Processo
from back.ResultadoEsperado import ResultadoEsperado
from back.Avaliacao import Avaliacao
from back.Projeto import Projeto
from back.Documento import Documento
from back.Versao_Modelo import Versao_Modelo
from back.Empresa import Empresa
from back.Instituicao import Instituicao
from back.Login import Login
from back.Cadastro import Cadastro
from back.Atividade import Atividade
from back.Email import Email
from back.Auditor import Auditor
from back.Relatorio import Relatorio
from back.GrauImplementacao import GrauImplementacao
from back.ImplementacaoOrganizacional import ImplementacaoOrganizacional
from back.ImplementacaoProjeto import ImplementacaoProjeto
from back.Database import Database
import os
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://checkfy-front.vercel.app"}})

UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Conexão com o banco de dados MySQL
db_config = {
    "host": "database-checkfy.cz4g8uek4dbw.us-east-2.rds.amazonaws.com",
    "user": "admin",  
    "password": "checkfyAJM", 
    "database": "checkfy", 
}

def get_db():
    if 'db' not in g:
        g.db = Database(**db_config)
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Criando objetos
# db = Database(**db_config)
# db2 = Database(**db_config)
# nivel = Nivel(db)
# processo = Processo(db)
# resultado_esperado = ResultadoEsperado(db)
# avaliacao = Avaliacao(db)
# projeto = Projeto(db)
# documento = Documento(db)
# versao_modelo = Versao_Modelo(db)
# empresa = Empresa(db)
# instituicao = Instituicao(db)
# login = Login(db)
# cadastro = Cadastro(db)
# atividade = Atividade(db)
# email = Email(db)
# auditor = Auditor(db2)
# relatorio = Relatorio(db)
# grau_implementacao = GrauImplementacao(db)

@app.route('/add_nivel', methods=['POST'])
def add_nivel():
    db = get_db()
    nivel = Nivel(db)
    nivel_data = request.json
    try:
        nivel.add_nivel(nivel_data['nivel'], nivel_data['nome_nivel'], nivel_data['id_versao_modelo'])
        return jsonify({"message": "Nível adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar nível: {e}")
        return jsonify({"message": "Erro ao adicionar nível", "error": str(e)}), 500

@app.route('/get_niveis/<int:id_versao_modelo>', methods=['GET'])
def get_niveis(id_versao_modelo):
    db = get_db()
    nivel = Nivel(db)
    try:
        niveis = nivel.get_niveis(id_versao_modelo)
        return jsonify(niveis), 200
    except Exception as e:
        print(f"Erro ao buscar níveis: {e}")
        return jsonify({"message": "Erro ao buscar níveis", "error": str(e)}), 500
    
@app.route('/get_niveis_limitado/<int:id_versao_modelo>/<int:id_nivel_solicitado>', methods=['GET'])
def get_niveis_limitado(id_versao_modelo, id_nivel_solicitado):
    db = get_db()
    nivel = Nivel(db)
    try:
        niveis = nivel.get_niveis_limitado(id_versao_modelo, id_nivel_solicitado)
        return jsonify(niveis), 200
    except Exception as e:
        print(f"Erro ao buscar níveis: {e}")
        return jsonify({"message": "Erro ao buscar níveis", "error": str(e)}), 500

@app.route('/delete_nivel/<int:nivel_id>', methods=['DELETE'])
def delete_nivel(nivel_id):
    db = get_db()
    nivel = Nivel(db)
    try:
        nivel.delete_nivel(nivel_id)
        return jsonify({"message": "Nível deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": "Erro ao deletar nível", "error": str(e)}), 500

@app.route('/update_nivel/<int:nivel_id>', methods=['PUT'])
def update_nivel(nivel_id):
    db = get_db()
    nivel = Nivel(db)
    nivel_data = request.json
    try:
        nivel.update_nivel(nivel_id, nivel_data['nivel'], nivel_data['nome_nivel'])
        return jsonify({"message": "Nível atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar nível: {e}")
        return jsonify({"message": "Erro ao atualizar nível", "error": str(e)}), 500

@app.route('/add_processo', methods=['POST'])
def add_processo():
    db = get_db()
    processo = Processo(db)
    try:
        descricao = request.json['descricao']
        tipo = request.json['tipo']
        id_versao_modelo = request.json['id_versao_modelo']
        processo.add_processo(descricao, tipo, id_versao_modelo)
        return jsonify({"message": "Processo adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar processo: {e}")
        return jsonify({"message": "Erro ao adicionar processo", "error": str(e)}), 500

@app.route('/get_processos/<int:id_versao_modelo>', methods=['GET'])
def get_processos(id_versao_modelo):
    db = get_db()
    processo = Processo(db)
    try:
        processos = processo.get_processos(id_versao_modelo)
        return jsonify(processos), 200  
    except Exception as e:
        print(f"Erro ao buscar processos: {e}")
        return jsonify({"message": "Erro ao buscar processos", "error": str(e)}), 500

@app.route('/delete_processo/<int:processo_id>', methods=['DELETE'])
def delete_processo(processo_id):
    db = get_db()
    processo = Processo(db)
    try:
        processo.delete_processo(processo_id)
        return jsonify({"message": "Processo deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": "Erro ao deletar processo", "error": str(e)}), 500

@app.route('/update_processo/<int:processo_id>', methods=['PUT'])
def update_processo(processo_id):
    db = get_db()
    processo = Processo(db)
    try:
        data = request.json
        nova_descricao = data['nova_descricao']
        novo_tipo = data['novo_tipo']
        processo.update_processo(processo_id, nova_descricao, novo_tipo)
        return jsonify({"message": "Processo atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar processo: {e}")
        return jsonify({"message": "Erro ao atualizar processo", "error": str(e)}), 500

@app.route('/add_resultado_esperado', methods=['POST'])
def add_resultado_esperado():
    db = get_db()
    resultado_esperado = ResultadoEsperado(db)
    try:
        data = request.json
        descricao = data['descricao']
        id_nivel_intervalo_inicio = data['id_nivel_intervalo_inicio']
        id_nivel_intervalo_fim = data['id_nivel_intervalo_fim']
        id_processo = data['id_processo']
        resultado_esperado.add_resultado_esperado(descricao, id_nivel_intervalo_inicio, id_nivel_intervalo_fim, id_processo)
        return jsonify({"message": "Resultado esperado adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar resultado esperado: {e}")
        return jsonify({"message": "Erro ao adicionar resultado esperado", "error": str(e)}), 500

@app.route('/get_resultados_esperados', methods=['GET'])
def get_resultados_esperados_route():
    db = get_db()
    resultado_esperado = ResultadoEsperado(db)
    try:
        processos_ids = request.args.get('processosId')
        if not processos_ids:
            return jsonify({"message": "No process IDs provided"}), 400
        processos_ids_list = [int(id) for id in processos_ids.split(',')]
        resultado_esperado = ResultadoEsperado(db)
        resultados_esperados = resultado_esperado.get_resultados_esperados(processos_ids_list)
        return jsonify(resultados_esperados), 200
    except Exception as e:
        print(f"Erro ao buscar resultados esperados: {e}")
        return jsonify({"message": "Erro ao buscar resultados esperados", "error": str(e)}), 500

@app.route('/delete_resultado_esperado/<int:resultado_id>', methods=['DELETE'])
def delete_resultado_esperado(resultado_id):
    db = get_db()
    resultado_esperado = ResultadoEsperado(db)
    try:
        resultado_esperado.delete_resultado_esperado(resultado_id)
        return jsonify({"message": "Resultado esperado deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": "Erro ao deletar resultado esperado", "error": str(e)}), 500

@app.route('/update_resultado_esperado/<int:resultado_id>', methods=['PUT'])
def update_resultado_esperado(resultado_id):
    db = get_db()
    resultado_esperado = ResultadoEsperado(db)
    try:
        data = request.json
        nova_descricao = data['nova_descricao']
        novo_id_nivel_intervalo_inicio = data['novo_id_nivel_intervalo_inicio']
        novo_id_nivel_intervalo_fim = data['novo_id_nivel_intervalo_fim']
        novo_id_processo = data['novo_id_processo']
        resultado_esperado.update_resultado_esperado(resultado_id, nova_descricao, novo_id_nivel_intervalo_inicio, novo_id_nivel_intervalo_fim, novo_id_processo)
        return jsonify({"message": "Resultado esperado atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar resultado esperado: {e}")
        return jsonify({"message": "Erro ao atualizar resultado esperado", "error": str(e)}), 500

@app.route('/add_avaliacao', methods=['POST'])
def add_avaliacao():
    db = get_db()
    avaliacao = Avaliacao(db)
    avaliacao_data = request.json
    try:
        nome = avaliacao_data['evaluationName']
        descricao = avaliacao_data['descricao']
        nivel_solicitado = avaliacao_data['nivelSolicitado']
        adjunto_emails = avaliacao_data['adjuntoEmails']
        colaborador_emails = avaliacao_data['colaboradorEmails']
        id_versao_modelo = avaliacao_data['idVersaoModelo']
        id_usuario = avaliacao_data['idUsuario']
        avaliacao.adicionar_avaliacao(nome, descricao, nivel_solicitado, adjunto_emails, colaborador_emails, id_usuario, id_versao_modelo)
        return jsonify({"message": "Avaliação adicionada com sucesso"}), 200
    except KeyError as e:
        print(f"Erro: Campo necessário não fornecido - {str(e)}")
        return jsonify({"message": "Campo necessário não fornecido", "error": str(e)}), 400
    except Exception as e:
        print(f"Erro ao adicionar avaliação: {e}")
        return jsonify({"message": "Erro ao adicionar avaliação", "error": str(e)}), 500

@app.route('/listar_avaliacoes/<int:id_usuario>', methods=['GET'])
def listar_avaliacoes(id_usuario):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        projetos = avaliacao.listar_avaliacoes(id_usuario)
        return jsonify(projetos), 200
    except Exception as e:
        print(f"Erro ao listar projetos: {e}")
        return jsonify({"message": "Erro ao listar projetos", "error": str(e)}), 500

@app.route('/deletar_avaliacao/<int:projeto_id>', methods=['DELETE'])
def deletar_avaliacao(projeto_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        avaliacao.deletar_avaliacao(projeto_id)
        return jsonify({"message": "Avaliação deletada com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": "Erro ao deletar avaliacão", "error": str(e)}), 500

@app.route('/atualizar_avaliacao/<int:projeto_id>', methods=['PUT'])
def atualizar_avaliacao(projeto_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    projeto_data = request.json
    try:
        avaliacao.atualizar_avaliacao(projeto_id, **projeto_data)
        return jsonify({"message": "Avaliação atualizada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar avaliação: {e}")
        return jsonify({"message": "Erro ao atualizar avaliação", "error": str(e)}), 500

@app.route('/atualizar_atividade/<int:projeto_id>', methods=['PUT'])
def atualizar_atividade(projeto_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    projeto_data = request.json
    try:
        nova_id_atividade = projeto_data.get('id_atividade')
        if nova_id_atividade is None:
            return jsonify({"message": "Campo 'id_atividade' ausente no JSON"}), 400
        
        avaliacao.atualizar_id_atividade(projeto_id, nova_id_atividade)
        return jsonify({"message": "ID_Atividade atualizada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar ID_Atividade: {e}")
        return jsonify({"message": "Erro ao atualizar ID_Atividade", "error": str(e)}), 500
    
@app.route('/inserir_planejamento/<int:projeto_id>', methods=['PUT'])
def inserir_planejamento(projeto_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        data = request.json
        avaliacao.inserir_planejamento(projeto_id, data['aprovacaoSoftex'], data['atividadePlanejamento'], data['cronogramaPlanejamento'])
        return jsonify({"message": "Planejamento adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar ID_Atividade: {e}")
        return jsonify({"message": "Erro ao adicionar planejamento", "error": str(e)}), 500
    
@app.route('/inserir_ata_reuniao/<int:projeto_id>', methods=['PUT'])
def inserir_ata_reuniao(projeto_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        data = request.json
        avaliacao.inserir_ata_reuniao(projeto_id, data['ataReuniao'])
        return jsonify({"message": "Planejamento adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar ID_Atividade: {e}")
        return jsonify({"message": "Erro ao adicionar planejamento", "error": str(e)}), 500

@app.route('/avaliacao/<int:projeto_id>', methods=['GET'])
def obter_avaliacao(projeto_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        avaliacao_data = avaliacao.obter_avaliacao(projeto_id)
        if avaliacao_data:
            return jsonify(avaliacao_data), 200
        else:
            return jsonify({"message": "Avaliação não encontrada"}), 404
    except Exception as e:
        print(f"Erro ao obter avaliação: {e}")
        return jsonify({"message": "Erro ao obter avaliação", "error": str(e)}), 500

@app.route('/add_projeto', methods=['POST'])
def add_projeto():
    db = get_db()
    projeto = Projeto(db)
    projeto_data = request.json
    try:
        avaliacao_id = projeto_data['avaliacaoId']
        nome_projeto = projeto_data['nome']
        habilitado = projeto_data['habilitado']
        numero_projeto = projeto.get_next_numero_projeto(avaliacao_id)
        projeto_id = projeto.add_projeto(avaliacao_id, nome_projeto, habilitado, numero_projeto)
        return jsonify({"message": "Projeto adicionado com sucesso", "projetoId": projeto_id}), 200
    except KeyError as e:
        print(f"Erro: Campo necessário não fornecido - {e}")
        return jsonify({"message": "Campo necessário não fornecido", "error": str(e)}), 400
    except Exception as e:
        print(f"Erro ao adicionar projeto: {e}")
        return jsonify({"message": "Erro ao adicionar projeto", "error": str(e)}), 500

@app.route('/update_projeto/<int:projeto_id>', methods=['PUT'])
def update_projeto(projeto_id):
    db = get_db()
    projeto = Projeto(db)
    projeto_data = request.json
    try:
        nome_projeto = projeto_data['nome']
        habilitado = projeto_data['habilitado']
        projeto.update_projeto(projeto_id, nome_projeto, habilitado)
        return jsonify({"message": "Projeto atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar projeto: {e}")
        return jsonify({"message": "Erro ao atualizar projeto", "error": str(e)}), 500

@app.route('/get_projetos_by_avaliacao/<int:avaliacao_id>', methods=['GET'])
def get_projetos_by_avaliacao(avaliacao_id):
    db = get_db()
    projeto = Projeto(db)
    try:
        projetos = projeto.get_projetos_by_id_avaliacao(avaliacao_id)
        return jsonify(projetos), 200
    except Exception as e:
        print(f"Erro ao buscar projetos por ID de avaliação: {e}")
        return jsonify({"message": "Erro ao buscar projetos", "error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({"filepath": filename}), 200 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/add_documento', methods=['POST'])
def add_documento():
    db = get_db()
    documento = Documento(db)
    documento_data = request.json
    try:
        id_projeto = documento_data['id_projeto']
        caminho_arquivo = documento_data['caminho_arquivo']
        nome_arquivo = documento_data['nome_arquivo']
        documento_id = documento.add_documento(caminho_arquivo, nome_arquivo, id_projeto)
        return jsonify({"message": "Documento adicionado com sucesso", "documentoId": documento_id}), 200
    except Exception as e:
        print(f"Erro ao adicionar documento: {e}")
        return jsonify({"message": "Erro ao adicionar documento", "error": str(e)}), 500

@app.route('/update_documento/<int:documento_id>', methods=['PUT'])
def update_documento(documento_id):
    db = get_db()
    documento = Documento(db)
    documento_data = request.json
    try:
        nome_arquivo = documento_data.get('nome_arquivo')
        caminho_arquivo = documento_data.get('caminho_arquivo')
        documento.update_documento(documento_id, nome_arquivo, caminho_arquivo)
        return jsonify({"message": "Documento atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar documento: {e}")
        return jsonify({"message": "Erro ao atualizar documento", "error": str(e)}), 500

@app.route('/documentos_por_projeto/<int:id_projeto>', methods=['GET'])
def documentos_por_projeto(id_projeto):
    db = get_db()
    documento = Documento(db)
    try:
        documentos = documento.get_documentos_by_projeto(id_projeto)
        return jsonify(documentos), 200
    except Exception as e:
        print(f"Erro ao buscar documentos: {e}")
        return jsonify({"message": "Erro ao buscar documentos", "error": str(e)}), 500

@app.route('/delete_documento/<int:documento_id>', methods=['DELETE'])
def delete_documento(documento_id):
    db = get_db()
    documento = Documento(db)
    try:
        documento.delete_documento(documento_id)
        return jsonify({"message": "Documento removido com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao remover documento: {e}")
        return jsonify({"message": "Erro ao remover documento", "error": str(e)}), 500

@app.route('/get_processos_por_avaliacao/<int:avaliacao_id>/<int:id_versao_modelo>', methods=['GET'])
def get_processos_por_avaliacao(avaliacao_id, id_versao_modelo):
    db = get_db()
    try:
        nivel_solicitado_query = "SELECT ID_Nivel_Solicitado FROM avaliacao WHERE ID = %s"
        db.cursor.execute(nivel_solicitado_query, (avaliacao_id,))
        nivel_solicitado = db.cursor.fetchone()[0]

        processos_query = """
            SELECT DISTINCT p.ID, p.Descricao
            FROM processo p
            JOIN resultado_esperado_mpsbr re ON p.ID = re.ID_Processo
            WHERE %s <= re.ID_Nivel_Intervalo_Inicio AND %s >= re.ID_Nivel_Intervalo_Fim and p.ID_Versao_Modelo = %s
        """
        db.cursor.execute(processos_query, (nivel_solicitado, nivel_solicitado, id_versao_modelo))
        processos = db.cursor.fetchall()

        return jsonify({
            'nivel_solicitado': nivel_solicitado,
            'processos': [{'ID': p[0], 'Descricao': p[1]} for p in processos]
        }), 200
    except Exception as e:
        print(f"Erro ao buscar processos por avaliação: {e}")
        return jsonify({"message": "Erro ao buscar processos", "error": str(e)}), 500

@app.route('/get_resultados_esperados_por_processo/<int:processo_id>/<int:avaliacao_id>', methods=['GET'])
def get_resultados_esperados_por_processo(processo_id, avaliacao_id):
    db = get_db()
    try:
        # Obtemos o nível solicitado da avaliação
        nivel_solicitado_query = "SELECT ID_Nivel_Solicitado FROM avaliacao WHERE ID = %s"
        db.cursor.execute(nivel_solicitado_query, (avaliacao_id,))
        nivel_solicitado = db.cursor.fetchone()[0]

        # Agora obtemos os resultados esperados que satisfazem a condição do nível solicitado
        query = """
            SELECT re.ID, re.Descricao, re.ID_Processo
            FROM resultado_esperado_mpsbr re
            WHERE re.ID_Processo = %s AND %s <= re.ID_Nivel_Intervalo_Inicio AND %s >= re.ID_Nivel_Intervalo_Fim
        """
        db.cursor.execute(query, (processo_id, nivel_solicitado, nivel_solicitado))
        resultados = db.cursor.fetchall()

        return jsonify([{
            'ID': r[0],
            'Descricao': r[1],
            'ID_Processo': r[2]
        } for r in resultados]), 200
    except Exception as e:
        print(f"Erro ao buscar resultados esperados por processo: {e}")
        return jsonify({"message": "Erro ao buscar resultados esperados", "error": str(e)}), 500

@app.route('/add_evidencia', methods=['POST'])
def add_evidencia():
    db = get_db()
    evidencia_data = request.json
    try:
        id_resultado_esperado = evidencia_data['id_resultado_esperado']
        id_documento = evidencia_data['id_documento']
        query = "INSERT INTO evidencia (ID_Resultado_Esperado, ID_Documento) VALUES (%s, %s)"
        db.cursor.execute(query, (id_resultado_esperado, id_documento))
        db.conn.commit()
        return jsonify({"message": "Evidencia adicionada com sucesso"}), 200
    except KeyError as e:
        print(f"Erro: Campo necessário não fornecido - {str(e)}")
        return jsonify({"message": f"Erro: Campo necessário não fornecido - {str(e)}"}), 400
    except Exception as e:
        print(f"Erro ao adicionar evidencia: {e}")
        db.conn.rollback()
        return jsonify({"message": "Erro ao adicionar evidencia", "error": str(e)}), 500

@app.route('/get_evidencias_por_resultado/<int:resultado_id>/<int:projeto_id>', methods=['GET'])
def get_evidencias_por_resultado(resultado_id, projeto_id):
    db = get_db()
    try:
        query = """
            SELECT d.ID, d.Caminho_Arquivo, d.Nome_Arquivo, d.ID_Projeto
            FROM documento d
            JOIN evidencia e ON d.ID = e.ID_Documento
            WHERE e.ID_Resultado_Esperado = %s AND d.ID_Projeto = %s
        """
        db.cursor.execute(query, (resultado_id, projeto_id))
        documentos = db.cursor.fetchall()
        return jsonify(documentos), 200
    except Exception as e:
        print(f"Erro ao buscar evidencias: {e}")
        return jsonify({"message": "Erro ao buscar evidencias", "error": str(e)}), 500

@app.route('/update_evidencia/<int:evidencia_id>', methods=['PUT'])
def update_evidencia(evidencia_id):
    db = get_db()
    projeto = Projeto(db)
    evidencia_data = request.json
    try:
        id_resultado_esperado = evidencia_data['id_resultado_esperado']
        id_documento = evidencia_data['id_documento']
        projeto.update_evidencia(evidencia_id, id_resultado_esperado, id_documento)
        return jsonify({"message": "Evidencia atualizado com sucesso"}), 200
    except KeyError as e:
        print(f"Erro: Campo necessário não fornecido - {e}")
        return jsonify({"message": "Campo necessário não fornecido", "error": str(e)}), 400
    except Exception as e:
        print(f"Erro ao atualizar evidencia: {e}")
        return jsonify({"message": "Erro ao atualizar evidencia", "error": str(e)}), 500
    
@app.route('/delete_evidencia/<int:id_resultado_esperado>/<int:id_documento>', methods=['DELETE'])
def delete_evidencia(id_resultado_esperado, id_documento):
    db = get_db()
    try:
        query = "DELETE FROM evidencia WHERE ID_Resultado_Esperado = %s AND ID_Documento = %s"
        db.cursor.execute(query, (id_resultado_esperado, id_documento))
        db.conn.commit()
        return jsonify({"message": "Evidência deletada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar evidência: {e}")
        return jsonify({"message": "Erro ao deletar evidência", "error": str(e)}), 500

@app.route('/add_or_update_grau_implementacao', methods=['POST'])
def add_or_update_grau_implementacao():
    db = get_db()
    try:
        data = request.json
        nota = data.get('nota')
        id_resultado_esperado = data.get('resultadoId')
        id_projeto = data.get('projetoId')

        # Verificar se já existe uma entrada para o resultado e projeto especificados
        query = """
            SELECT ID FROM grau_implementacao_processo_projeto 
            WHERE ID_Resultado_Esperado = %s AND ID_Projeto = %s
        """
        db.cursor.execute(query, (id_resultado_esperado, id_projeto))
        result = db.cursor.fetchone()

        if result:
            # Atualizar a entrada existente
            update_query = """
                UPDATE grau_implementacao_processo_projeto
                SET Nota = %s
                WHERE ID_Resultado_Esperado = %s AND ID_Projeto = %s
            """
            db.cursor.execute(update_query, (nota, id_resultado_esperado, id_projeto))
        else:
            # Inserir nova entrada
            insert_query = """
                INSERT INTO grau_implementacao_processo_projeto (Nota, ID_Resultado_Esperado, ID_Projeto)
                VALUES (%s, %s, %s)
            """
            db.cursor.execute(insert_query, (nota, id_resultado_esperado, id_projeto))

        db.conn.commit()
        return jsonify({"message": "Grau de implementação adicionado/atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar/atualizar grau de implementação: {e}")
        db.conn.rollback()
        return jsonify({"message": "Erro ao adicionar/atualizar grau de implementação", "error": str(e)}), 500

@app.route('/get_graus_implementacao/<int:avaliacao_id>', methods=['GET'])
def get_graus_implementacao(avaliacao_id):
    db = get_db()
    try:
        query = """
            SELECT gip.ID, gip.Nota, gip.ID_Resultado_Esperado, gip.ID_Projeto
            FROM grau_implementacao_processo_projeto gip
            JOIN projeto p ON gip.ID_Projeto = p.ID
            WHERE p.ID_Avaliacao = %s
        """
        db.cursor.execute(query, (avaliacao_id,))
        graus = db.cursor.fetchall()
        graus_implementacao = [
            {'ID': g[0], 'Nota': g[1], 'ID_Resultado_Esperado': g[2], 'ID_Projeto': g[3]}
        for g in graus]

        return jsonify(graus_implementacao), 200
    except Exception as e:
        print(f"Erro ao buscar graus de implementação: {e}")
        return jsonify({"message": "Erro ao buscar graus de implementação", "error": str(e)}), 500

@app.route('/get_versao_modelo', methods=['GET'])
def get_versao_modelo():
    db = get_db()
    versao_modelo = Versao_Modelo(db)
    try:
        return jsonify(versao_modelo.get_versao_modelo()), 200  
    except Exception as e:
        print(f"Erro ao buscar versao_modelo: {e}")
        return jsonify({"message": "Erro ao buscar versao_modelo", "error": str(e)}), 500
    
@app.route('/add_versao_modelo', methods=['POST'])
def add_versao_modelo():
    db = get_db()
    versao_modelo = Versao_Modelo(db)
    try:
        data = request.json
        versao_modelo.add_versao_modelo(nome=data['nome'], status=data['status'])
        return jsonify({"message": "Processo adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar processo: {e}")
        return jsonify({"message": "Erro ao adicionar processo", "error": str(e)}), 500

@app.route('/delete_versao_modelo/<int:versao_modelo_id>', methods=['DELETE'])
def delete_versao_modelo(versao_modelo_id):
    db = get_db()
    versao_modelo = Versao_Modelo(db)
    try:
        versao_modelo.delete_versao_modelo(versao_modelo_id)
        return jsonify({"message": "versao_modelo deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": "Erro ao deletar versao_modelo", "error": str(e)}), 500

@app.route('/update_versao_modelo/<int:versao_modelo_id>', methods=['PUT'])
def update_versao_modelo(versao_modelo_id):
    db = get_db()
    versao_modelo = Versao_Modelo(db)
    try:
        data = request.json
        versao_modelo.update_versao_modelo(nome=data['nome'], status=data['status'], id=versao_modelo_id)
        return jsonify({"message": "Processo atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar processo: {e}")
        return jsonify({"message": "Erro ao atualizar processo", "error": str(e)}), 500

@app.route('/get_empresas', methods=['GET'])
def get_empresas():
    db = get_db()
    empresa = Empresa(db)
    try:
        empresas = empresa.get_empresas()
        return jsonify(empresas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_empresa', methods=['POST'])
def add_empresa():
    db = get_db()
    empresa = Empresa(db)
    data = request.json
    try:
        empresa_id = empresa.add_empresa(data['nome'], data['cnpj'])
        return jsonify({'id': empresa_id, 'message': 'Empresa adicionada com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_empresa/<int:id>', methods=['PUT'])
def update_empresa(id):
    db = get_db()
    empresa = Empresa(db)
    data = request.json
    try:
        empresa.update_empresa(id, data['nome'], data['cnpj'])
        return jsonify({'message': 'Empresa atualizada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_empresa/<int:id>', methods=['DELETE'])
def delete_empresa(id):
    db = get_db()
    empresa = Empresa(db)
    try:
        empresa.delete_empresa(id)
        return jsonify({'message': 'Empresa deletada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/empresa_avaliacao_insert/<int:avaliacao_id>', methods=['PUT'])
def empresa_avaliacao_insert(avaliacao_id):
    db = get_db()
    empresa = Empresa(db)
    data = request.json
    try:
        empresa.empresa_avaliacao_insert(avaliacao_id, data['idEmpresa'])
        return jsonify({'message': 'Empresa atualizada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_instituicoes', methods=['GET'])
def get_instituicoes():
    db = get_db()
    instituicao = Instituicao(db)
    try:
        instituicoes = instituicao.get_instituicoes()
        return jsonify(instituicoes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_instituicao', methods=['POST'])
def add_instituicao():
    db = get_db()
    instituicao = Instituicao(db)
    data = request.json
    try:
        instituicao_id = instituicao.add_instituicao(data['nome'], data['cnpj'])
        return jsonify({'id': instituicao_id, 'message': 'Instituição adicionada com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instituicao_avaliacao_insert/<int:avaliacao_id>', methods=['PUT'])
def instituicao_avaliacao_insert(avaliacao_id):
    db = get_db()
    instituicao = Instituicao(db)
    data = request.json
    try:
        instituicao.instituicao_avaliacao_insert(avaliacao_id, data['idInstituicao'])
        return jsonify({'message': 'Instituição atualizada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def user_login():
    db = get_db()
    login = Login(db)
    try:
        data = request.json
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({"message": "Email e senha são obrigatórios."}), 400

        response = login.login(email, senha)
        return jsonify(response), response["status"]

    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({"message": f"Erro no login: {str(e)}"}), 500

@app.route('/cadastro', methods=['POST'])
def cadastro_route():
    db = get_db()
    cadastro = Cadastro(db)
    data = request.json
    print(f"Dados recebidos: {data}")
    
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    cargo = data.get('cargo')

    response, status = cadastro.cadastrar_usuario(nome, email, senha, cargo)
    return jsonify(response), status

@app.route('/upload_acordo_confidencialidade/<int:avaliacao_id>', methods=['POST'])
def upload_acordo_confidencialidade(avaliacao_id):
    db = get_db()
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Atualizar o campo Caminho_Acordo_Confidencialidade na tabela avaliacao
        try:
            query = "UPDATE avaliacao SET Caminho_Acordo_Confidencialidade = %s WHERE ID = %s"
            values = (filename, avaliacao_id)
            db.cursor.execute(query, values)
            db.conn.commit()
            return jsonify({"message": "Acordo de confidencialidade salvo com sucesso!", "filepath": filename}), 200
        except Exception as e:
            print(f"Erro ao atualizar Caminho_Acordo_Confidencialidade: {e}")
            return jsonify({"message": "Erro ao atualizar Caminho_Acordo_Confidencialidade", "error": str(e)}), 500

@app.route('/get_acordo_confidencialidade/<int:avaliacao_id>', methods=['GET'])
def get_acordo_confidencialidade(avaliacao_id):
    db = get_db()
    try:
        query = "SELECT Caminho_Acordo_Confidencialidade FROM avaliacao WHERE ID = %s"
        db.cursor.execute(query, (avaliacao_id,))
        result = db.cursor.fetchone()

        if result and result[0]:
            return jsonify({"filepath": result[0]}), 200
        else:
            # Retorna uma resposta com status 200, mas sem um caminho de arquivo
            return jsonify({"message": "Nenhum acordo de confidencialidade encontrado.", "filepath": None}), 200
    except Exception as e:
        print(f"Erro ao obter Caminho_Acordo_Confidencialidade: {e}")
        return jsonify({"message": "Erro ao obter Caminho_Acordo_Confidencialidade", "error": str(e)}), 500
    
@app.route('/get_atividade', methods=['GET'])
def get_atividades():
    db = get_db()
    atividade = Atividade(db)
    try:
        atividades = atividade.get_atividades()
        return jsonify(atividades), 200
    except Exception as e:
        print(f"Erro ao buscar atividades: {e}")
        return jsonify({"message": "Erro ao buscar atividades", "error": str(e)}), 500

@app.route('/enviar_email/<int:avaliacao_id>', methods=['POST'])
def enviar_email(avaliacao_id):
    db = get_db()
    email = Email(db)
    try:
        email.email_aprovar_softex(avaliacao_id)
        return jsonify({"message": "E-mail enviado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/enviar_email_solicitar_feedback/<int:avaliacao_id>', methods=['POST'])
def enviar_email_solicitar_feedback(avaliacao_id):
    db = get_db()
    email = Email(db)
    try:
        email.solicitar_link_formulario_feedback(avaliacao_id)
        return jsonify({"message": "E-mail Feedback enviado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/enviar_email_auditor_avaliacao_final/<int:avaliacao_id>', methods=['POST'])
def enviar_email_auditor_avaliacao_final(avaliacao_id):
    db = get_db()
    email = Email(db)
    try:
        email.enviar_email_auditor_avaliacao_final(avaliacao_id)
        return jsonify({"message": "E-mail de avaliação final enviado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@app.route('/add_auditor', methods=['POST'])
def add_auditor():
    db = get_db()
    auditor = Auditor(db)
    auditor_data = request.json
    try:
        id_avaliacao = auditor_data['idAvaliacao']
        auditor_emails = auditor_data['auditorEmails']
        
        auditor.adicionar_auditor(id_avaliacao, auditor_emails)
        
        return jsonify({"message": "Auditores adicionados com sucesso"}), 200  # Retorne uma resposta JSON com código 200
    except KeyError as e:
        print(f"Erro: Campo necessário não fornecido - {str(e)}")
        return jsonify({"message": "Campo necessário não fornecido", "error": str(e)}), 400
    except Exception as e:
        print(f"Erro ao adicionar auditores: {e}")
        return jsonify({"message": "Erro ao adicionar auditores", "error": str(e)}), 500

@app.route('/get_email_auditor/<int:avaliacao_id>', methods=['GET'])
def get_email_auditor(avaliacao_id):
    db = get_db()
    auditor = Auditor(db)
    try:
        email = auditor.get_email_auditor(avaliacao_id)
        
        if email:
            return jsonify({"email": email}), 200
        else:
            # Retorna 200 com uma mensagem indicando que o auditor ainda não foi cadastrado
            return jsonify({"message": "Nenhum auditor cadastrado para esta avaliação"}), 200

    except Exception as e:
        print(f"Erro ao buscar e-mail do auditor: {e}")
        return jsonify({"message": "Erro ao buscar e-mail do auditor", "error": str(e)}), 500

@app.route('/update_email_auditor/<int:avaliacao_id>', methods=['PUT'])
def update_email_auditor(avaliacao_id):
    db = get_db()
    auditor = Auditor(db)
    data = request.get_json()
    novo_email = data.get('novo_email')
    if not novo_email:
        return jsonify({"message": "O novo e-mail é obrigatório."}), 400

    try:
        # Chama o método de atualização na classe Auditor
        auditor.update_email_auditor(avaliacao_id, novo_email)
        return jsonify({"message": "E-mail do auditor atualizado com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao atualizar e-mail do auditor: {e}")
        return jsonify({"message": "Erro ao atualizar e-mail do auditor", "error": str(e)}), 500

@app.route('/salvar_apresentacao_equipe', methods=['POST'])
def salvar_apresentacao_equipe():
    db = get_db()
    avaliacao = Avaliacao(db)
    data = request.json
    id_avaliacao = data.get('idAvaliacao')
    apresentacao_inicial = data.get('apresentacaoInicial')
    equipe_treinada = data.get('equipeTreinada')

    if id_avaliacao is None or apresentacao_inicial is None or equipe_treinada is None:
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        avaliacao.salvar_apresentacao_equipe(id_avaliacao, apresentacao_inicial, equipe_treinada)
        return jsonify({"message": "Dados salvos com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return jsonify({"message": "Erro ao salvar dados"}), 500

@app.route('/get_apresentacao_equipe/<int:avaliacao_id>', methods=['GET'])
def get_apresentacao_equipe(avaliacao_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    id_avaliacao = avaliacao_id

    if not id_avaliacao:
        return jsonify({"message": "ID da avaliação não fornecido"}), 400

    try:
        result = avaliacao.get_apresentacao_equipe(id_avaliacao)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"message": "Dados não encontrados"}), 404
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return jsonify({"message": "Erro ao buscar dados"}), 500

@app.route('/inserir_relatorio_inicial', methods=['POST'])
def inserir_relatorio_inicial():
    db = get_db()
    relatorio = Relatorio(db)
    data = request.json
    descricao = data.get('descricao')
    id_avaliacao = data.get('idAvaliacao')
    caminho_arquivo = data.get('caminhoArquivo')

    if not descricao or not id_avaliacao:
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        relatorio_id = relatorio.inserir_relatorio_inicial(descricao, id_avaliacao, caminho_arquivo)
        return jsonify({"message": "Relatório inserido com sucesso", "id": relatorio_id}), 201
    except Exception as e:
        print(f"Erro ao inserir relatório: {e}")
        return jsonify({"message": "Erro ao inserir relatório"}), 500

@app.route('/atualizar_relatorio_inicial', methods=['PUT'])
def atualizar_relatorio_inicial():
    db = get_db()
    relatorio = Relatorio(db)
    data = request.json
    descricao = data.get('descricao')
    id_avaliacao = data.get('idAvaliacao')
    caminho_arquivo = data.get('caminhoArquivo')
    print(data)
    if not descricao or not id_avaliacao:
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        relatorio.atualizar_relatorio_inicial(descricao, id_avaliacao, caminho_arquivo)
        return jsonify({"message": "Relatório atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar relatório: {e}")
        return jsonify({"message": "Erro ao atualizar relatório"}), 500

@app.route('/get_relatorio_inicial/<int:avaliacao_id>', methods=['GET'])
def get_relatorio_inicial(avaliacao_id):
    db = get_db()
    relatorio = Relatorio(db)
    id_avaliacao = avaliacao_id
    if not id_avaliacao:
        return jsonify({"message": "ID da avaliação não fornecido"}), 400
    try:
        result = relatorio.obter_relatorio_inicial(id_avaliacao)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"message": "Relatório não encontrado, ainda não foi criado"}), 200
    except Exception as e:
        print(f"Erro ao buscar relatório: {e}")
        return jsonify({"message": "Erro ao buscar relatório"}), 500
    
@app.route('/inserir_relatorio_auditoria_final', methods=['POST'])
def inserir_relatorio_auditoria_final():
    db = get_db()
    relatorio = Relatorio(db)
    data = request.json
    descricao = data.get('descricao')
    id_avaliacao = data.get('idAvaliacao')

    if not descricao or not id_avaliacao:
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        relatorio_id = relatorio.inserir_relatorio_auditoria_final(descricao, id_avaliacao)
        return jsonify({"message": "Relatório inserido com sucesso", "id": relatorio_id}), 201
    except Exception as e:
        print(f"Erro ao inserir relatório: {e}")
        return jsonify({"message": "Erro ao inserir relatório"}), 500

@app.route('/atualizar_relatorio_auditoria_final', methods=['PUT'])
def atualizar_relatorio_auditoria_final():
    db = get_db()
    relatorio = Relatorio(db)
    data = request.json
    descricao = data.get('descricao')
    id_avaliacao = data.get('idAvaliacao')
    print(data)
    if not descricao or not id_avaliacao:
        return jsonify({"message": "Dados incompletos"}), 400
    try:
        relatorio.atualizar_relatorio_auditoria_final(descricao, id_avaliacao)
        return jsonify({"message": "Relatório atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao atualizar relatório: {e}")
        return jsonify({"message": "Erro ao atualizar relatório"}), 500

@app.route('/get_relatorio_auditoria_final/<int:avaliacao_id>', methods=['GET'])
def get_relatorio_auditoria_final(avaliacao_id):
    db = get_db()
    relatorio = Relatorio(db)
    id_avaliacao = avaliacao_id
    if not id_avaliacao:
        return jsonify({"message": "ID da avaliação não fornecido"}), 400
    try:
        result = relatorio.get_relatorio_auditoria_final(id_avaliacao)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"message": "Relatório não encontrado, ainda não foi criado"}), 200
    except Exception as e:
        print(f"Erro ao buscar relatório: {e}")
        return jsonify({"message": "Erro ao buscar relatório"}), 500

@app.route('/enviar_email_auditor/<int:avaliacao_id>', methods=['POST'])
def enviar_email_auditor(avaliacao_id):
    db = get_db()
    db_email = get_db()
    auditor = Auditor(db)
    email = Email(db_email)
    try:
        # Chama o método da classe Auditor para obter o e-mail
        email_auditor = auditor.get_email_auditor(avaliacao_id)
        if email_auditor:
            # Chama a função para enviar o e-mail
            email.enviar_email_auditor_avaliacao_inicial(avaliacao_id, email_auditor)
            return jsonify({"message": "E-mail enviado com sucesso!"}), 200
        else:
            return jsonify({"message": "Auditor não encontrado"}), 404

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/enviar_email_auditor_data_avaliacao_final/<int:avaliacao_id>', methods=['POST'])
def enviar_email_auditor_data_avaliacao_final(avaliacao_id):
    db = get_db()
    auditor = Auditor(db)
    email = Email(db)
    try:
        # Chama o método da classe Auditor para obter o e-mail
        email_auditor = auditor.get_email_auditor(avaliacao_id)
        if email_auditor:
            # Chama a função para enviar o e-mail
            email.enviar_email_auditor_data_avaliacao_final(avaliacao_id, email_auditor)
            return jsonify({"message": "E-mail enviado com sucesso!"}), 200
        else:
            return jsonify({"message": "Auditor não encontrado"}), 404

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/notificar_participantes_resultado_avaliacao_inicial/<int:avaliacao_id>', methods=['POST'])
def notificar_participantes_resultado_avaliacao_inicial(avaliacao_id):
    db = get_db()
    email = Email(db)
    try:
        email.notificar_participantes_resultado_avaliacao_inicial(avaliacao_id)
        return jsonify({"message": "E-mail enviado com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/update_empresa_ajuste_avaliacao_inicial/<int:id_empresa>', methods=['PUT'])
def update_empresa_ajuste_avaliacao_inicial(id_empresa):
    db = get_db()
    empresa = Empresa(db)
    data = request.json
    try:
        empresa.update_empresa_ajuste_avaliacao_inicial(id_empresa, data['nome'])
        return jsonify({"message": "Empresa atualizada com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao atualizar empresa: {e}")
        return jsonify({"message": "Erro ao atualizar empresa", "error": str(e)}), 500

@app.route('/update_avaliacao_ajuste_inicial/<int:avaliacao_id>', methods=['PUT'])
def update_avaliacao_ajuste_inicial(avaliacao_id):
    db = get_db()
    avaliacao = Avaliacao(db)
    data = request.json
    try:
        avaliacao.atualizar_avaliacao_ajuste_inicial(
            avaliacao_id,
            descricao=data.get('descricao'),
            cronograma_planejamento=data.get('cronograma_planejamento'),
            atividade_planejamento=data.get('atividade_planejamento')
        )
        return jsonify({"message": "Avaliação atualizada com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao atualizar avaliação: {e}")
        return jsonify({"message": "Erro ao atualizar avaliação", "error": str(e)}), 500

@app.route('/update_relatorio_ajuste_avaliacao_inicial/<int:avaliacao_id>', methods=['PUT'])
def update_relatorio_ajuste_avaliacao_inicial(avaliacao_id):
    db = get_db()
    relatorio = Relatorio(db)
    data = request.json
    print(data)
    try:
        relatorio.atualizar_relatorio_inicial(descricao=data.get('descricao'), id_avaliacao=avaliacao_id, caminho_arquivo=data.get('caminho_arquivo') )
        return jsonify({"message": "Relatório atualizado com sucesso!"}), 200
    except Exception as e:
        print(f"Erro ao atualizar relatório: {e}")
        return jsonify({"message": "Erro ao atualizar relatório", "error": str(e)}), 500

@app.route('/add_data_avaliacao', methods=['POST'])
def add_data_avaliacao():
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        data = request.json
        id_avaliacao = data['idAvaliacao']
        data_avaliacao_final = data['dataAvaliacaoFinal']
        avaliacao.adicionar_data_avaliacao_final(id_avaliacao, data_avaliacao_final)
        return jsonify({"message": "Data de avaliação final adicionada com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_data_avaliacao/<int:id_avaliacao>', methods=['GET'])
def get_data_avaliacao(id_avaliacao):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        data_avaliacao_final = avaliacao.obter_data_avaliacao_final(id_avaliacao)
        if data_avaliacao_final:
            return jsonify({"dataAvaliacaoFinal": data_avaliacao_final}), 200
        else:
            return jsonify({"message": "Data de avaliação final não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_data_avaliacao/<int:id_avaliacao>', methods=['PUT'])
def update_data_avaliacao(id_avaliacao):
    db = get_db()
    avaliacao = Avaliacao(db)
    try:
        data = request.json
        nova_data_avaliacao_final = data['dataAvaliacaoFinal']
        avaliacao.atualizar_data_avaliacao_final(id_avaliacao, nova_data_avaliacao_final)
        return jsonify({"message": "Data de avaliação final atualizada com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_graus_implementacao_empresa/<int:id_avaliacao>', methods=['GET'])
def get_graus_implementacao_empresa(id_avaliacao):
    db = get_db()
    grau_implementacao = GrauImplementacao(db)
    graus = grau_implementacao.get_grau_implementacao_empresa(id_avaliacao)
    return jsonify(graus), 200

@app.route('/insert_graus_implementacao_empresa', methods=['POST'])
def insert_graus_implementacao_empresa():
    db = get_db()
    grau_implementacao = GrauImplementacao(db)
    try:
        # O 'data' agora é um array de objetos, onde cada objeto tem 'id_avaliacao', 'id_resultado_esperado' e 'nota'
        data = request.json

        # Montar os valores para o insert múltiplo
        valores = [(item['id_avaliacao'], item['id_resultado_esperado'], item['nota']) for item in data]

        # Realizar o insert múltiplo
        grau_implementacao.add_graus_implementacao_empresa(valores)

        return jsonify({'message': 'Graus de implementação inseridos com sucesso!'}), 201
    except Exception as e:
        print(f"Erro ao inserir graus de implementação: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_graus_implementacao_empresa', methods=['PUT'])
def update_graus_implementacao_empresa():
    db = get_db()
    grau_implementacao = GrauImplementacao(db)
    try:
        data = request.json
        update_data = [(item['nota'], item['id_avaliacao'], item['id_resultado_esperado']) for item in data]

        grau_implementacao.update_graus_implementacao_empresa_batch(update_data)
        return jsonify({'message': 'Graus de implementação atualizados com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_resultado_final/<int:id_avaliacao>', methods=['PUT'])
def update_resultado_final(id_avaliacao):
    db = get_db()
    avaliacao = Avaliacao(db)
    data = request.json
    try:
        parecer_final = data['parecerFinal']
        id_nivel_atribuido = data['idNivelAtribuido']
        
        avaliacao.update_resultado_final(id_avaliacao, parecer_final, id_nivel_atribuido)

        return jsonify({"message": "Resultado final atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_perguntas_capacidade_processo_organizacional/<int:id_nivel>', methods=['GET'])
def get_perguntas_capacidade_processo_organizacional(id_nivel):
    print(id_nivel)
    db = get_db()
    organizacional = ImplementacaoOrganizacional(db)
    try:        
        perguntas = organizacional.get_perguntas(id_nivel)
        if perguntas is not None:
            return jsonify(perguntas), 200
        else:
            return jsonify({'message': 'Nenhuma pergunta encontrada para o nível especificado.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_capacidade_processo_organizacional/<int:id_avaliacao>', methods=['GET'])
def get_capacidade_processo_organizacional(id_avaliacao):
    db = get_db()
    organizacional = ImplementacaoOrganizacional(db)
    capacidade_processo = organizacional.get_capacidade_processo_organizacional(id_avaliacao)
    return jsonify(capacidade_processo), 200

@app.route('/insert_capacidade_processo_organizacional', methods=['POST']) 
def insert_capacidade_processo_organizacional():
    db = get_db()
    organizacional = ImplementacaoOrganizacional(db)
    try:
        # O 'data' agora é um array de objetos, onde cada objeto tem 'id_avaliacao', 'id_resultado_esperado' e 'nota'
        data = request.json

        # Montar os valores para o insert múltiplo
        valores = [(item['id_avaliacao'], item['id_processo'], item['nota']) for item in data]

        # Realizar o insert múltiplo
        organizacional.add_capacidade_processo_organizacional(valores)

        return jsonify({'message': 'Capacidade do processo inserido com sucesso!'}), 201
    except Exception as e:
        print(f"Erro ao inserir graus de implementação: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_capacidade_processo_organizacional', methods=['PUT'])
def update_capacidade_processo_organizacional():
    db = get_db()
    organizacional = ImplementacaoOrganizacional(db)
    try:
        data = request.json
        update_data = [(item['nota'], item['id_avaliacao'], item['id_processo']) for item in data]

        organizacional.update_capacidade_processo_organizacional_batch(update_data)
        return jsonify({'message': 'Capacidade do processo atualizados com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_perguntas_capacidade_processo_projeto/<int:id_nivel>', methods=['GET'])
def get_perguntas_capacidade_processo_projeto(id_nivel):
    print(id_nivel)
    db = get_db()
    projeto = ImplementacaoProjeto(db)
    try:        
        perguntas = projeto.get_perguntas(id_nivel)
        if perguntas is not None:
            return jsonify(perguntas), 200
        else:
            return jsonify({'message': 'Nenhuma pergunta encontrada para o nível especificado.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_capacidade_processo_projeto/<int:id_avaliacao>', methods=['GET'])
def get_capacidade_processo_projeto(id_avaliacao):
    db = get_db()
    projeto = ImplementacaoProjeto(db)
    capacidade_processo = projeto.get_capacidade_processo_projeto(id_avaliacao)
    return jsonify(capacidade_processo), 200

@app.route('/insert_capacidade_processo_projeto', methods=['POST']) 
def insert_capacidade_processo_projeto():
    db = get_db()
    projeto = ImplementacaoProjeto(db)
    try:
        # O 'data' agora é um array de objetos, onde cada objeto tem 'id_avaliacao', 'id_resultado_esperado' e 'nota'
        data = request.json
        # Montar os valores para o insert múltiplo
        valores = [(item['id_avaliacao'], item['id_projeto'], item['nota']) for item in data]

        # Realizar o insert múltiplo
        projeto.add_capacidade_processo_projeto(valores)

        return jsonify({'message': 'Capacidade do processo inserido com sucesso!'}), 201
    except Exception as e:
        print(f"Erro ao inserir graus de implementação: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_capacidade_processo_projeto', methods=['PUT'])
def update_capacidade_processo_projeto():
    db = get_db()
    projeto = ImplementacaoProjeto(db)
    try:
        data = request.json
        update_data = [(item['nota'], item['id_avaliacao'], item['id_projeto']) for item in data]
        print(update_data)
        projeto.update_capacidade_processo_projeto_batch(update_data)
        return jsonify({'message': 'Capacidade do processo atualizados com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/notificar_participantes_resultado_avaliacao_final/<int:avaliacao_id>', methods=['POST'])
def notificar_participantes_resultado_avaliacao_final(avaliacao_id):
    db = get_db()
    email = Email(db)
    try:
        email.notificar_participantes_resultado_avaliacao_final(avaliacao_id)
        return jsonify({"message": "E-mail de avaliação final enviado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_evidencias_por_pergunta_projeto/<int:pergunta_id>/<int:projeto_id>', methods=['GET'])
def get_evidencias_por_pergunta_projeto(pergunta_id, projeto_id):
    db = get_db()
    implementacao_projeto = ImplementacaoProjeto(db)
    try:
        evidencias = implementacao_projeto.get_evidencias_por_pergunta(pergunta_id, projeto_id)
        return jsonify(evidencias), 200
    except Exception as e:
        print(f"Erro ao buscar evidências: {e}")
        return jsonify({"message": "Erro ao buscar evidências", "error": str(e)}), 500

@app.route('/add_evidencia_projeto', methods=['POST'])
def add_evidencia_projeto():
    db = get_db()
    implementacao_projeto = ImplementacaoProjeto(db)
    data = request.json
    try:
        id_pergunta = data['id_pergunta']
        id_projeto = data['id_projeto']
        caminho_arquivo = data['caminho_arquivo']
        nome_arquivo = data['nome_arquivo']

        evidencia_id = implementacao_projeto.add_evidencia_projeto(id_pergunta, id_projeto, caminho_arquivo, nome_arquivo)
        return jsonify({"message": "Evidência adicionada com sucesso", "evidencia_id": evidencia_id}), 200
    except Exception as e:
        print(f"Erro ao adicionar evidência: {e}")
        return jsonify({"message": "Erro ao adicionar evidência", "error": str(e)}), 500

@app.route('/delete_evidencia_projeto/<int:evidencia_id>', methods=['DELETE'])
def delete_evidencia_projeto(evidencia_id):
    db = get_db()
    implementacao_projeto = ImplementacaoProjeto(db)
    try:
        implementacao_projeto.delete_evidencia_projeto(evidencia_id)
        return jsonify({"message": "Evidência deletada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar evidência: {e}")
        return jsonify({"message": "Erro ao deletar evidência", "error": str(e)}), 500

# Similar routes for Organizacional
@app.route('/get_evidencias_por_pergunta_organizacional/<int:pergunta_id>/<int:processo_id>', methods=['GET'])
def get_evidencias_por_pergunta_organizacional(pergunta_id, processo_id):
    db = get_db()
    implementacao_organizacional = ImplementacaoOrganizacional(db)
    try:
        evidencias = implementacao_organizacional.get_evidencias_por_pergunta(pergunta_id, processo_id)
        return jsonify(evidencias), 200
    except Exception as e:
        print(f"Erro ao buscar evidências: {e}")
        return jsonify({"message": "Erro ao buscar evidências", "error": str(e)}), 500

@app.route('/add_evidencia_organizacional', methods=['POST'])
def add_evidencia_organizacional():
    db = get_db()
    implementacao_organizacional = ImplementacaoOrganizacional(db)
    data = request.json
    try:
        id_pergunta = data['id_pergunta']
        id_processo = data['id_processo']
        caminho_arquivo = data['caminho_arquivo']
        nome_arquivo = data['nome_arquivo']
        id_avaliacao = data['id_avaliacao']

        evidencia_id = implementacao_organizacional.add_evidencia_organizacional(id_pergunta, id_processo, caminho_arquivo, nome_arquivo, id_avaliacao)
        return jsonify({"message": "Evidência adicionada com sucesso", "evidencia_id": evidencia_id}), 200
    except Exception as e:
        print(f"Erro ao adicionar evidência: {e}")
        return jsonify({"message": "Erro ao adicionar evidência", "error": str(e)}), 500

@app.route('/delete_evidencia_organizacional/<int:evidencia_id>', methods=['DELETE'])
def delete_evidencia_organizacional(evidencia_id):
    db = get_db()
    implementacao_organizacional = ImplementacaoOrganizacional(db)
    try:
        implementacao_organizacional.delete_evidencia_organizacional(evidencia_id)
        return jsonify({"message": "Evidência deletada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar evidência: {e}")
        return jsonify({"message": "Erro ao deletar evidência", "error": str(e)}), 500

@app.route('/atualizar_status_avaliacao/<int:id_avaliacao>', methods=['PUT'])
def atualizar_status_avaliacao(id_avaliacao):
    db = get_db()
    avaliacao = Avaliacao(db)
    data = request.json
    try:
        id_status = data['id_status']
        avaliacao.atualizar_status_avaliacao(id_avaliacao, id_status)
        return jsonify({"message": "Resultado final atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
    app.run()