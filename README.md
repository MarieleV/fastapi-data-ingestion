# fastapi-data-ingestion

Pipeline de Mini-ETL local e leve construído com FastAPI, Pandas e Pydantic para validação estrita e ingestão de dados em SQLite.

## 📌 Sobre o Projeto

Este projeto consiste em uma API desenvolvida para automatizar a **ingestão, validação e higienização de dados cadastrais em lote**.

O objetivo principal é substituir processos manuais de importação de planilhas, garantindo a integridade e a qualidade dos dados (*Data Quality*) antes que eles entrem no banco de dados da empresa. A API recebe arquivos brutos, processa em memória, aplica rigorosas regras de negócio e consolida as informações.

## 🛠️ Tecnologias Utilizadas

* **FastAPI:** Framework web moderno e de alta performance para construção da API.
* **Pandas:** Utilizado para a manipulação e limpeza estrutural das planilhas em memória.
* **Pydantic:** Responsável pela validação de dados e garantia de tipagem (ex: verificação de integridade de CPFs/CNPJs).
* **SQLAlchemy:** ORM (Object Relational Mapper) utilizado para a modelagem e persistência dos dados.
* **SQLite:** Banco de dados relacional leve e autossuficiente para armazenamento local.

## ✨ Principais Funcionalidades

1. **Upload Flexível:** Suporte nativo para ingestão de arquivos `.csv` e `.xlsx`.
2. **Data Cleansing:** Tratamento inteligente de dados ausentes (NaN) e padronização de formatação proveniente de artefatos do Excel.
3. **Validação Inteligente:** Checagem de regras de negócio, como a consistência matemática e tamanho de documentos de identificação.
4. **Controle de Duplicidade:** Mecanismo preventivo contra a inserção de cadastros duplicados no banco de dados.
5. **Feedback Detalhado:** Retorno estruturado em JSON contendo o status do processamento, número de sucessos e o mapeamento de erros por linha.

## ⚙️ Como Executar Localmente

### 1. Pré-requisitos

* Python 3.9+ instalado na máquina.
* Gerenciador de pacotes `pip`.

### 2. Passo a Passo

Clone este repositório:

```bash
git clone https://github.com/MarieleV/fastapi-data-ingestion.git
cd fastapi-data-ingestion
```

Crie e ative um ambiente virtual (recomendado):

```bash
# No Windows:
python -m venv venv
.\venv\Scripts\Activate.ps1

# No Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências do projeto:

```bash
pip install fastapi uvicorn pandas pydantic sqlalchemy python-multipart openpyxl
```

Inicie o servidor de desenvolvimento:

```bash
uvicorn main:app --reload --port 8080
```

## 📖 Documentação da API

Com a aplicação rodando, você pode acessar a documentação interativa autogerada pelo FastAPI:

* **Swagger UI:** [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs) (Ideal para testar o upload de arquivos na prática).
* **ReDoc:** [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc) (Ideal para leitura fluida das regras e esquemas da API).

## 👩‍💻 Autora

**Mariele Vieira da Silva**

*Estudante de Engenharia de Software | Engenharia de Dados, Cloud e IA*

* [LinkedIn](https://www.linkedin.com/in//mariele-vieira-8698091b7)
* [GitHub](https://github.com/MarieleV)
* Contato: silvamariele797@gmail.com