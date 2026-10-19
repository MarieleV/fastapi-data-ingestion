<div align="center">
  <!-- Ícone representativo de API/Dados -->
  <img src="https://img.icons8.com/fluency/96/000000/api-settings.png" alt="Ícone de API" width="80"/>
  
  <h1>FastAPI: Ingestão de Dados & Data Quality</h1>

  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-API_REST-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/Pandas-Data_Cleaning-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
    <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  </p>

  <p><em>Pipeline de Mini-ETL local e leve construído para validação estrita e ingestão automatizada de dados.</em></p>
</div>

<br>

<h2>Sobre o Projeto</h2>
<p>
  Este projeto consiste em uma <b>API RESTful</b> desenvolvida em Python para automatizar a ingestão, validação e higienização de dados cadastrais em lote. O objetivo principal é substituir processos manuais e falhos de importação de planilhas por um fluxo programático seguro.
</p>
<p>
  A API recebe arquivos brutos (CSV ou Excel), processa tudo em memória com <b>Pandas</b> para tratar anomalias estruturais, aplica rigorosas regras de negócio com <b>Pydantic</b> (como adequação matemática e de tamanho de CPFs/CNPJs) e salva os registros válidos em um banco de dados relacional (SQLite via <b>SQLAlchemy</b>). Tudo isso garantindo o conceito de <i>Data Quality</i> antes que os dados sujem o ecossistema da empresa.
</p>

<br>

<h2> Principais Funcionalidades</h2>

<table>
  <tr>
    <td width="200"><b>Upload Flexível</b></td>
    <td>Suporte nativo para ingestão via endpoints <code>POST</code> de arquivos estruturados nos formatos <code>.csv</code> e <code>.xlsx</code>.</td>
  </tr>
  <tr>
    <td><b>Data Cleansing</b></td>
    <td>Tratamento inteligente em memória com Pandas: remove artefatos gerados pelo Excel, lida com dados ausentes (NaN) e preserva zeros à esquerda.</td>
  </tr>
  <tr>
    <td><b>Validação Inteligente</b></td>
    <td>Verificação granular linha a linha com Pydantic, garantindo que documentos e nomes cumpram as exigências do banco de dados antes da inserção.</td>
  </tr>
  <tr>
    <td><b>Controle de Duplicidade</b></td>
    <td>Mecanismo preventivo no ORM SQLAlchemy contra a inserção de cadastros com CPFs ou CNPJs já existentes na base.</td>
  </tr>
  <tr>
    <td><b>Feedback Estruturado</b></td>
    <td>Retorno rápido em JSON contendo métricas do processamento (sucessos vs. falhas) e mapeamento exato da linha e motivo de cada erro.</td>
  </tr>
</table>

<br>

<h2>📂 Arquitetura do Sistema</h2>

<details>
  <summary><b>Clique para visualizar a estrutura do projeto</b></summary>
  <br>
  
  ```text
  ├── main.py               # Script centralizado: Rotas FastAPI, Data Cleaning (Pandas) e ORM
  ├── mini_etl.db           # Banco de dados SQLite autogerado na primeira execução
  ├── requirements.txt      # Mapeamento de dependências (FastAPI, Pandas, Pydantic, SQLAlchemy)
  └── README.md             # Documentação e manual de uso do projeto
  ```
</details>

<br>

<h2>⚙️ Como Executar Localmente</h2>

<p>Siga os passos abaixo para rodar a API em sua máquina local:</p>

```bash
# 1. Clone este repositório
git clone https://github.com/MarieleV/fastapi-data-ingestion.git
cd fastapi-data-ingestion

# 2. Crie e ative um ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1   # No Windows
# source venv/bin/activate    # No Linux/Mac

# 3. Instale as dependências listadas
pip install fastapi uvicorn pandas pydantic sqlalchemy python-multipart openpyxl

# 4. Inicie o servidor de desenvolvimento
uvicorn main:app --reload --port 8080
```

<br>

<h2>📖 Documentação da API (Swagger)</h2>
<p>
  Com a aplicação rodando, acesse a documentação interativa autogerada no seu navegador para testar o upload de planilhas na prática: <br>
  👉 <a href="http://127.0.0.1:8080/docs">http://127.0.0.1:8080/docs</a>
</p>

<br>

<h2>👩‍💻 Autora</h2>
<p>
  <b>Mariele Vieira da Silva</b><br>
  <i>Estudante de Engenharia de Software | Engenharia de Dados, Cloud e IA</i><br><br>
  <a href="https://www.linkedin.com/in//mariele-vieira-8698091b7">LinkedIn</a> | 
  <a href="https://github.com/MarieleV">GitHub</a> | 
  ✉️ silvamariele797@gmail.com
</p>