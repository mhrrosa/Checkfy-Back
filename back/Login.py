from werkzeug.security import check_password_hash
from Database import Database
import traceback

class Login:
    def __init__(self, db: Database):
        self.db = db

    def login(self, email, senha):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = "SELECT id, senha, id_tipo, nome FROM usuario WHERE email = %s"
            print(f"Executando query: {query} com email: {email}")  # Log de SQL

            cursor.execute(query, (email,))
            user = cursor.fetchone()

            # Garantir que todos os resultados sejam processados
            cursor.fetchall()  # Limpa qualquer resultado pendente

            if user:
                print(f"Usuário encontrado: {user}")  # Log de usuário encontrado
            else:
                print("Nenhum usuário encontrado com este email.")

            if user and check_password_hash(user['senha'], senha):
                cursor.close()
                return {"message": "Login realizado com sucesso!", "user_id": user['id'], "user_type": user['id_tipo'], "nome": user['nome'], "status": 200}
            else:
                cursor.close()
                return {"message": "Credenciais inválidas.", "status": 401}

        except Exception as e:
            # Registra o erro com rastreamento completo
            print(f"Erro no login: {e}")
            traceback.print_exc()  # Mostra o stack trace completo para debug

            cursor.close()
            return {"message": f"Erro no login: {str(e)}", "status": 500}