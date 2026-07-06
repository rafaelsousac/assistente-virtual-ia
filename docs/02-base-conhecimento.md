# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
>
> Organize a base de conhecimento do agente "InfoNutri" usando os arquivos da pasta `data/` (em anexo). Explique pra que serve cada arquivo e monte um exemplo de contexto formatado que será enviado pro LLM. Preencha o template abaixo.
>

## Dados Utilizados

| Arquivo                        | Formato | Para que serve no InfoNutri?                                                                    |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| `historico_duvidas.csv`         | CSV     | Contextualizar dúvidas anteriores, dando continuidade ao atendimento de forma mais eficiente.    |
| `perfil_usuario.json`           | JSON    | Personalizar as explicações de acordo com restrições alimentares e nível de conhecimento da pessoa. |
| `alimentos_nutrientes.json`     | JSON    | Conhecer o catálogo de alimentos disponível para usar como exemplo prático nas explicações.      |
| `registro_consumo.csv`          | CSV     | Analisar o padrão de consumo alimentar recente da pessoa e usar isso de forma didática.           |
| `glossario_nutrientes.json`     | JSON    | Definir termos técnicos (nutrientes, rótulos) de forma correta e consistente.                    |
| `faq_mitos_verdades.json`       | JSON    | Responder crenças populares sobre alimentação com base em consenso nutricional, evitando mitos.  |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Optei por separar o conhecimento nutricional "estático" (glossário e FAQ) dos dados "da pessoa usuária" (perfil, consumo e histórico). Isso porque, diferente do Edu — cujos produtos financeiros mudam pouco — o InfoNutri precisa distinguir claramente entre "o que é verdade sobre nutrição" (não muda por pessoa) e "o que essa pessoa específica come e pergunta" (muda por pessoa). Assim, é mais fácil garantir que o agente nunca misture uma opinião pessoal com um fato nutricional.

---

## Estratégia de Integração

### Como os dados são carregados?

> Descreva como seu agente acessa a base de conhecimento.

Assim como no exemplo do Edu, os dados são carregados via código no início da aplicação:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_usuario.json'))
registro_consumo = pd.read_csv('./data/registro_consumo.csv')
historico = pd.read_csv('./data/historico_duvidas.csv')
alimentos = json.load(open('./data/alimentos_nutrientes.json'))
glossario = json.load(open('./data/glossario_nutrientes.json'))
faq = json.load(open('./data/faq_mitos_verdades.json'))
```

### Como os dados são usados no prompt?

> Os dados vão no system prompt? São consultados dinamicamente?

Para o protótipo, os dados são injetados diretamente no prompt a cada pergunta, junto do system prompt, garantindo que o InfoNutri tenha sempre o contexto completo disponível:

```
DADOS DA PESSOA USUÁRIA (data/perfil_usuario.json):
{
  "nome": "Camila Souza",
  "idade": 29,
  "nivel_conhecimento_nutricao": "iniciante",
  "restricoes_alimentares": ["intolerância à lactose"],
  "topicos_de_interesse": ["leitura de rótulos", "mitos sobre alimentação", "grupos alimentares"]
}

REGISTRO DE CONSUMO (data/registro_consumo.csv):
data,refeicao,alimento,quantidade_estimativa
2026-06-01,café da manhã,Aveia em flocos,1 porção
2026-06-01,almoço,Lentilha cozida,1 porção
2026-06-02,lanche da tarde,Iogurte natural,1 unidade
2026-06-03,jantar,Abacate,1/2 unidade
2026-06-04,lanche,Refrigerante comum,1 lata

HISTORICO DE DUVIDAS (data/historico_duvidas.csv):
data,pergunta,categoria,resposta_encontrada_na_base
2026-06-01,O que significa 'light' no rótulo?,glossario,sim
2026-06-02,Carboidrato à noite engorda mais?,faq_mito,sim
2026-06-03,Qual o melhor suplemento para emagrecer?,fora_de_escopo,nao

CATALOGO DE ALIMENTOS (data/alimentos_nutrientes.json):
[
  {
    "alimento": "Aveia em flocos",
    "grupo": "Cereal integral",
    "principais_nutrientes": ["fibra alimentar", "ferro", "magnésio"],
    "beneficio_informativo": "Fonte de fibras que ajudam na saciedade e no funcionamento do intestino."
  },
  {
    "alimento": "Iogurte natural",
    "grupo": "Laticínio",
    "principais_nutrientes": ["cálcio", "proteína", "probióticos"],
    "beneficio_informativo": "Contribui para a saúde óssea e intestinal."
  }
]

GLOSSARIO DE NUTRIENTES (data/glossario_nutrientes.json):
[
  {
    "termo": "Fibra alimentar",
    "definicao": "Parte dos alimentos vegetais que o corpo não digere. Ajuda no funcionamento do intestino e dá mais sensação de saciedade."
  },
  {
    "termo": "Sódio",
    "definicao": "Mineral presente no sal de cozinha. Em excesso, está associado a pressão alta."
  }
]

FAQ DE MITOS E VERDADES (data/faq_mitos_verdades.json):
[
  {
    "pergunta": "Comer carboidrato à noite engorda mais?",
    "resposta": "Não existe evidência de que o horário, isoladamente, determine ganho de peso.",
    "categoria": "mito"
  }
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

Assim como no Edu, o contexto pode ser sintetizado para economizar tokens, mantendo apenas as informações mais relevantes para a pergunta feita:

```
DADOS DA PESSOA USUÁRIA:
- Nome: Camila Souza
- Nível: Iniciante em nutrição
- Restrição alimentar: intolerância à lactose
- Interesse: leitura de rótulos, mitos sobre alimentação

CONSUMO RECENTE:
- Aveia em flocos, Lentilha cozida, Iogurte natural (sem lactose), Abacate, Refrigerante (ocasional)

TERMOS RELEVANTES DO GLOSSÁRIO:
- Fibra alimentar: ajuda no funcionamento do intestino
- Light: redução de pelo menos 25% em algum componente vs. versão original

MITOS RELACIONADOS:
- "Carboidrato à noite engorda mais" → mito, o que importa é o total calórico do dia
```