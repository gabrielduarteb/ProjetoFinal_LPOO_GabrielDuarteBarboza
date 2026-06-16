import psycopg


class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg.connect(
                "host=localhost port=5432 dbname=lpoo_projeto_gabrielduarte user=postgres password=postgres"
            )
            return conexao
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
