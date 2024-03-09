import redis
import psycopg2

# Conexão com o Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Função para buscar dados do PostgreSQL com cache
def get_data_with_cache(key):
    # Verifique se os dados estão presentes no cache
    data = r.get(key)
    if data is not None:
        # Se os dados estiverem no cache, retorne-os
        return data.decode('utf-8')
    else:
        # Se os dados não estiverem no cache, busque do PostgreSQL
        conn = psycopg2.connect("dbname=nome_do_banco_de_dados user=seu_usuario password=sua_senha")
        cur = conn.cursor()
        cur.execute("SELECT * FROM tabela WHERE chave = %s", (key,))
        data = cur.fetchone()
        # Armazene os dados no cache do Redis
        r.set(key, data)
        # Retorne os dados
        return data

# Exemplo de uso da função
data = get_data_with_cache('chave')
