import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="reservas_laboratorio"
)

print("Conectado ao banco com sucesso!")

conexao.close()