from werkzeug.security import generate_password_hash
from Database import Database

class Cadastro:
    def __init__(self, db: Database):
        self.db = db

    def cadastrar_usuario(self, nome, email, senha, cargo):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            # Buscar o ID_Tipo baseado na descrição do cargo
            query_tipo = "SELECT ID FROM tipo_usuario WHERE Descricao = %s"
            cursor.execute(query_tipo, (cargo,))
            tipo_result = cursor.fetchone()
            
            if not tipo_result:
                print(f"Cargo '{cargo}' não encontrado no banco de dados.")
                return {"message": f"Cargo '{cargo}' não encontrado."}, 400
            
            id_tipo = tipo_result['ID']  # Ajustado para acessar o valor pelo nome da coluna
            senha_hash = generate_password_hash(senha)

            # Executar a query de inserção
            query = "INSERT INTO usuario (Nome, Email, Senha, ID_Tipo) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nome, email, senha_hash, id_tipo))
            self.db.conn.commit()

            # Recuperar o último ID inserido
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()['LAST_INSERT_ID()']  # Acessando o ID pelo nome da coluna

            return {"message": "Usuário cadastrado com sucesso!", "user_id": user_id}, 201
            
        except Exception as e:
            self.db.conn.rollback()  # Desfaz as mudanças em caso de erro
            print(f"Erro ao cadastrar usuário: {str(e)}")
            return {"message": f"Erro ao cadastrar usuário: {str(e)}"}, 500
        finally:
            cursor.close()  # Fechar o cursor no bloco 'finally' para garantir o fechamento

