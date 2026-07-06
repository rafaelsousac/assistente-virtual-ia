import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_usuario.json'))
registro_consumo = pd.read_csv('./data/registro_consumo.csv')
historico = pd.read_csv('./data/historico_duvidas.csv')
alimentos = json.load(open('./data/alimentos_nutrientes.json'))
glossario = json.load(open('./data/glossario_nutrientes.json'))
faq = json.load(open('./data/faq_mitos_verdades.json'))

# ============ MONTAR CONTEXTO ============
contexto = f"""
PESSOA USUÁRIA: {perfil['nome']}, {perfil['idade']} anos, nível {perfil['nivel_conhecimento_nutricao']}
OBJETIVO: {perfil['objetivo_principal']}
RESTRIÇÕES ALIMENTARES: {', '.join(perfil['restricoes_alimentares'])}
TÓPICOS DE INTERESSE: {', '.join(perfil['topicos_de_interesse'])}

REGISTRO DE CONSUMO RECENTE:
{registro_consumo.to_string(index=False)}

DÚVIDAS ANTERIORES:
{historico.to_string(index=False)}

CATÁLOGO DE ALIMENTOS:
{json.dumps(alimentos, indent=2, ensure_ascii=False)}

GLOSSÁRIO DE NUTRIENTES:
{json.dumps(glossario, indent=2, ensure_ascii=False)}

FAQ DE MITOS E VERDADES:
{json.dumps(faq, indent=2, ensure_ascii=False)}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o InfoNutri, um assistente de nutrição informativa amigável e didático.

OBJETIVO:
Explicar conceitos de nutrição de forma simples, ajudando a pessoa usuária a entender melhor o que come, usando os dados fornecidos como exemplos práticos.

REGRAS:
- NUNCA prescreva dietas, planos alimentares, metas de calorias ou macronutrientes — apenas explique como os nutrientes e alimentos funcionam;
- JAMAIS diagnostique condições de saúde (intolerâncias, deficiências, doenças); se a pergunta exigir isso, recomende buscar um nutricionista ou médico;
- JAMAIS responda a perguntas fora do tema nutrição informativa. Quando ocorrer, responda lembrando o seu papel de assistente de nutrição informativa;
- Use os dados fornecidos (perfil, registro de consumo, catálogo de alimentos, glossário e FAQ) para dar exemplos personalizados;
- Linguagem simples e acolhedora, como se explicasse para um amigo, sem julgamento sobre as escolhas alimentares da pessoa;
- Se não souber algo ou a informação não estiver na base, admita: "Não tenho essa informação na minha base, mas recomendo consultar um nutricionista para isso";
- Sempre pergunte se a pessoa entendeu ou se quer que você explique de outro jeito;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DA PESSOA USUÁRIA:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ============ INTERFACE ============
st.title("🥗 InfoNutri, seu Assistente de Nutrição Informativa")

if pergunta := st.chat_input("Sua dúvida sobre nutrição..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
