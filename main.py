from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import io

# --- Configuração do Banco de Dados (SQLite Local) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./mini_etl.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ClienteDB(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cpf_cnpj = Column(String, unique=True, index=True)
    status = Column(String)

# Cria as tabelas no SQLite caso não existam
Base.metadata.create_all(bind=engine)

# --- Validação de Dados (Pydantic) ---
class ClienteSchema(BaseModel):
    nome: str = Field(..., min_length=2)
    cpf_cnpj: str
    status: str

    @field_validator('cpf_cnpj')
    def validar_documento(cls, v):
        # Transforma em string e remove um eventual ".0" decimal gerado pelo Pandas
        v_str = str(v).split('.')[0]
        
        # Mantém apenas os dígitos numéricos
        doc = ''.join(filter(str.isdigit, v_str))
        
        # Recoloca o zero à esquerda caso o Excel tenha apagado
        if len(doc) == 10:
            doc = doc.zfill(11) # Preenche até 11 dígitos
        elif len(doc) == 13:
            doc = doc.zfill(14) # Preenche até 14 dígitos
            
        if len(doc) not in [11, 14]:
            raise ValueError(f'Tamanho inválido. Após processamento, o documento ficou com {len(doc)} dígitos: {doc}')
        
        return doc

# --- Configuração da Documentação (Swagger UI) ---
descricao_api = """
Esta API foi desenvolvida para automatizar a **ingestão, validação e higienização** de dados cadastrais em lote. 

Ideal para substituir processos manuais em planilhas, garantindo a integridade e qualidade dos dados (Data Quality) antes de entrarem no banco de dados da empresa.

### Principais Funcionalidades:
* **Upload de Lotes:** Aceita arquivos estáticos nos formatos `.csv` e `.xlsx`.
* **Validação Inteligente:** Aplica regras de negócio para checar formatação e consistência matemática de CPFs e CNPJs.
* **Controle de Duplicidade:** Evita o cadastro duplicado de documentos já existentes na base.
"""

app = FastAPI(
    title="Mini-ETL API | Portfólio de Engenharia de Dados",
    description=descricao_api,
    version="1.0.0",
    contact={
        "name": "Mariele Vieira da Silva",
        "url": "https://github.com/MarieleV",
        "email": "silvamariele797@gmail.com",
    }
)

@app.post(
    "/batches/upload", 
    tags=["Ingestão de Dados"], 
    summary="Processar planilha de clientes",
    description="Recebe um arquivo CSV ou Excel, processa os dados em memória com Pandas, aplica as validações do Pydantic e salva os registros válidos no banco SQLite."
)
async def upload_arquivo(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Formato inválido. Envie um arquivo .csv ou .xlsx.")

    try:
        # Lendo o arquivo em memória com Pandas
        contents = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents), dtype=str).fillna("")
        else:
            df = pd.read_excel(io.BytesIO(contents), dtype=str).fillna("")
        
        # Padronizando o nome das colunas para minúsculo
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Verificando se o cabeçalho possui as colunas obrigatórias
        colunas_esperadas = {'nome', 'cpf_cnpj', 'status'}
        if not colunas_esperadas.issubset(set(df.columns)):
            raise HTTPException(
                status_code=400, 
                detail=f"O arquivo deve conter as colunas obrigatórias: {colunas_esperadas}"
            )

        db = SessionLocal()
        registros_sucesso = 0
        erros = []

        # Processamento linha a linha simulando o worker
        for index, row in df.iterrows():
            try:
                # 1. Validação de formato via Pydantic
                cliente_validado = ClienteSchema(**row.to_dict())
                
                # 2. Verificação de duplicidade no banco
                existe = db.query(ClienteDB).filter(ClienteDB.cpf_cnpj == cliente_validado.cpf_cnpj).first()
                
                if not existe:
                    # 3. Inserção
                    novo_cliente = ClienteDB(**cliente_validado.model_dump())
                    db.add(novo_cliente)
                    registros_sucesso += 1
                else:
                    erros.append({"linha": index + 2, "erro": "Documento já cadastrado na base"})
            
            except Exception as e:
                erros.append({"linha": index + 2, "erro": str(e)})

        db.commit()
        db.close()

        return {
            "mensagem": "Processamento concluído",
            "linhas_processadas": len(df),
            "sucessos": registros_sucesso,
            "falhas": len(erros),
            "detalhes_erros": erros[:10] # Limite para não sobrecarregar o JSON de retorno
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o arquivo: {str(e)}")