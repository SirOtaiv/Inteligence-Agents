from crewai import Agent, Crew, Task
from dotenv import load_dotenv
from litellm import completion

load_dotenv(".env")

response = completion(
    model="groq/llama3-8b-8192",
    messages=[
        {"role": "user", "content": "hello"}
        ],
)
print(response)

consumer_forecast_agent = Agent(
    role="Agente de Previsão de Consumo",
    goal="Garantir que os valores estejam alinhados com a média de outros hospitáis de mesmo nível e tipo, além de estar acima do valor mínimo para operar considerando também as temporadas do ano.",
    backstory="Voce é um analista sênior e um administrador nato, tendo várias anos como chefe do setor de estoque",
    allow_delegation=False,
    verbose=True,
    llm="groq/llama3-8b-8192"
)

consumer_stock_agent = Agent(
    role="Agente de Monitoramento de Estoque",
    goal="Estar sempre atento aos valores de consumo considerando o periodo do ano de atuação, os consumos recentes e fornecer insights de recomendação de uso e compra.",
    backstory="Analista de negócio experiente no mercado com foco em análise ",
    allow_delegation=False,
    verbose=True,
    llm="groq/llama3-8b-8192"
)

task_research_consumer = Task(
    description= "Prever o consumo de cada tipo de suprimento com base nos históricos de uso, turnos de trabalho e sazonalidade (por exemplo, aumento de internações em certas épocas do ano).", #tarefa a ser realizada
    expected_output=("Gerar estatísticas de consumo de um ano de exemplo"),
    agent=consumer_forecast_agent,
)

task_research_necessity = Task(
    description= "Identificar a necessidade de reposição com base nos níveis atuais de estoque, pedidos futuros e prazos de entrega dos fornecedores.", #tarefa a ser realizada
    expected_output=("Fornecimento de avisos e insights de compra ou redução de compra com base nos valores de uso e compra do mês"),
    agent=consumer_stock_agent,
    output_file='output/consumer.md'
)

crew = Crew(
    agents= [consumer_stock_agent, consumer_forecast_agent],
    task=[task_research_consumer, task_research_necessity],
    verbose = True,
    max_rpm = 25
)

result = crew.kickoff(inputs={"":""})