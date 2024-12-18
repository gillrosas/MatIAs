import os

import google.generativeai as genai
import streamlit as st
from streamlit import chat_input

#Configurando o o modelo gemini 1.5 flash
genai.configure(api_key= os.getenv('GEMINI_API_KEY'))
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="Você é um especialista em ensinar matemática para adolescentes e jovens . Sua tarefa é envolver-se em conversas sobre matemática e responder a perguntas."
                    " Explique conceitos matemáticos de forma clara e fácil de entender. Utilize analogias e exemplos do cotidiano. Use humor para tornar a "
                    "conversa educativa e interessante. Faça perguntas para entender melhor o usuário e melhorar a experiência de aprendizado. "
                    "Sugira maneiras de relacionar esses conceitos com o mundo real por meio de observações e atividades práticas.",
)

#Histórico de mensagens(mostrarão na tela o que está sendo conversado)

if "history" not in st.session_state:
    st.session_state ["history"]= []
#fazer a interface

st.title(" **Mat.IA.s**")
st.write("Seja bem -vindo. Sou seu chatbot que tira as suas dúvidas em matemática. O que posso te ajudar hoje? ")
#fazer a interação com o usuario
user_input = st.chat_input("Escreva aqui sua dúvida")
if user_input:
  st.write(f"Você: {user_input}")
  if not user_input.strip():
    print("Preciso que escreva a sua dúvida ")
  else:
    try:
      chat_session = model.start_chat(history =st.session_state.history)
      response = chat_session.send_message(user_input)
      resposta_ia = response.text
      # Atualiza o histórico
      st.session_state.history.append({"role": "user", "parts": [user_input]})
      st.session_state.history.append({"role": "model", "parts": [resposta_ia]})

    except Exception as e:
      st.error(f"ocorreu um erro : {e}")

































