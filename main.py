#
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import psycopg2
import os


DATABASE_URL = os.getenv("DATABASE_URL")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def main():

  def show_database():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT *  FROM trainup")
    results = cur.fetchall()
    cur.close()
    conn.close()

    id=[]
    serie=[]
    date = []
    exercicio=[]
    repeticao=[]

    for result in results:
      id.append(result[0])
      exercicio.append(result[1])
      serie.append(result[2])
      repeticao.append(result[3])
      date.append(result[4])

    df = pd.DataFrame({
      'exercicio': exercicio,
      'serie': serie,
      'repeticao': repeticao,
      'date': date
    })

    return df


  def execute_database(insert_exercicio, insert_serie, insert_repeticao, insert_data):
    sql =  f"""INSERT INTO trainup (exercicio, serie, repeticao, data)
            VALUES (
                      '{str(insert_exercicio)}',
                      {str(insert_serie)},
                      {str(insert_repeticao)},
                      '{str(insert_data)}'
                  )
          """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

  with st.form("my_form"):
    input_exercicio = st.selectbox("Exercício", ['Flexao normal','Flexao inclinada', 'Rosca', 'Triceps', 'Trapezio', 'Elevacao lateral','Elevacao frontal', 'Desenvolvimento'])
    input_serie = st.number_input('Série', 1)
    input_repeticao = st.number_input('Repetição', 0)
    input_data = st.date_input("Data", "today", format="YYYY-MM-DD")
    button = st.form_submit_button('Adicionar', type='primary')

  if button:
    execute_database(input_exercicio, input_serie, input_repeticao, input_data)

  showDF = show_database()
  showDF = showDF.sort_values(by='date')
  showDF

  df2 = showDF.groupby(['exercicio','date'])['repeticao'].sum().reset_index()

  st.line_chart(df2, x='date', y='repeticao', color='exercicio')



# Função para autenticar o usuário
def authenticate(username, password):
    return username in USER and PASSWORD == password

# Verifica se já há um estado de autenticação
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Se o usuário ainda não está autenticado, mostra a tela de login
if not st.session_state['authenticated']:
    st.title("Tela de Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username  # Armazenando o usuário logado
            st.rerun() # Recarrega a página para exibir a tela de conteúdo
        else:
            st.error("Usuário ou senha incorretos.")

# Se estiver autenticado, mostra a página principal
else:
    st.write(f"Olá, **{st.session_state['username']}**, você está logado!")
    main()

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.rerun()  # Recarrega a página para voltar à tela de login



