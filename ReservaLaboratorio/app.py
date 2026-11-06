import streamlit as st
import mysql.connector
import pandas as pd



def conectar():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="reservas_laboratorio"
    )



def listar_laboratorios():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome FROM Laboratorios"
    )

    dados = cursor.fetchall()

    conn.close()

    return dados



def verificar_conflito(lab_id, data, turno):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Reservas
        WHERE lab_id = %s
        AND data_reserva = %s
        AND turno = %s
    """, (lab_id, data, turno))

    resultado = cursor.fetchone()

    conn.close()

    return resultado



def salvar_reserva(lab_id, professor, data, turno):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Reservas
        (
            lab_id,
            nome_professor,
            data_reserva,
            turno
        )
        VALUES (%s, %s, %s, %s)
    """, (lab_id, professor, data, turno))

    conn.commit()

    conn.close()



def listar_reservas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            l.nome,
            r.nome_professor,
            r.data_reserva,
            r.turno
        FROM Reservas r
        INNER JOIN Laboratorios l
        ON r.lab_id = l.id
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados



st.title("Sistema de Reserva de Laboratórios")



professor = st.text_input(
    "Nome do Professor"
)



labs = listar_laboratorios()

opcoes = {}

for id_lab, nome in labs:
    opcoes[nome] = id_lab

laboratorio = st.selectbox(
    "Laboratório",
    list(opcoes.keys())
)



data = st.date_input(
    "Data da Reserva"
)



turno = st.selectbox(
    "Turno",
    ["Manhã", "Tarde", "Noite"]
)



if st.button("Reservar"):

    lab_id = opcoes[laboratorio]

    conflito = verificar_conflito(
        lab_id,
        data,
        turno
    )

    if conflito:

        st.error(
            "Este laboratório já está reservado nesse horário."
        )

    else:

        salvar_reserva(
            lab_id,
            professor,
            data,
            turno
        )

        st.success(
            "Reserva cadastrada com sucesso!"
        )


st.subheader("Reservas Realizadas")

reservas = listar_reservas()

df = pd.DataFrame(
    reservas,
    columns=[
        "ID",
        "Laboratório",
        "Professor",
        "Data",
        "Turno"
    ]
)

st.dataframe(df)