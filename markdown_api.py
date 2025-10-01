from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import base64
import PyPDF2
import io

# 1. Crie uma instância do FastAPI
app = FastAPI(
    title="API Completa - Processamento de Arquivos",
    description="Processa arquivos binários e gera markdown",
    version="5.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Modelo para receber arquivo em base64
class FileData(BaseModel):
    filename: str
    file_content: str  # base64 encoded
    document_hash: str

# 3. Modelo para dados extraídos (mantém compatibilidade)
class LicitacaoData(BaseModel):
    numero_edital: Optional[str] = None
    modalidade: Optional[str] = None
    objeto_licitacao: Optional[str] = None
    data_abertura: Optional[str] = None
    prazo_proposta: Optional[str] = None
    valor_estimado: Optional[float] = None
    document_hash: str

def extract_text_from_pdf(file_content_base64: str) -> str:
    """Extrai texto de PDF a partir de conteúdo base64"""
    try:
        # Decodifica base64
        pdf_bytes = base64.b64decode(file_content_base64)
        
        # Cria um objeto de arquivo em memória
        pdf_file = io.BytesIO(pdf_bytes)
        
        # Lê o PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extrai texto de todas as páginas
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"

@app.get("/")
def ler_raiz():
    return {"message": "API de Processamento de Arquivos - v5.0"}

# 4. Novo endpoint para processar arquivo binário
@app.post("/process-file-to-markdown")
def process_file_to_markdown(data: FileData):
    """
    Recebe arquivo binário (base64) e retorna markdown com texto extraído
    """
    
    # Extrai texto do arquivo
    extracted_text = extract_text_from_pdf(data.file_content)
    
    # Gera markdown básico com o texto extraído
    markdown_text = f"""
# 📄 Documento Processado: {data.filename}

**Hash do Documento:** `{data.document_hash}`

---

## 📝 Conteúdo Extraído

{extracted_text}

---
*Processado automaticamente pela API de Licitações*
"""
    
    return {
        "filename": data.filename,
        "document_hash": data.document_hash,
        "extracted_text": extracted_text,
        "markdown_content": markdown_text,
        "success": True
    }

# 5. Mantém o endpoint original para compatibilidade
@app.post("/generate-markdown")
def create_markdown_summary(data: LicitacaoData):
    """
    Recebe dados de uma licitação em formato JSON e retorna um resumo em Markdown.
    """
    
    markdown_text = f"""
## 📄 Resumo da Licitação: {data.numero_edital or "Não identificado"}

**Modalidade:** {data.modalidade or "Não informada"}
**Status:** 새로운 (Novo)

---

### **Objeto da Licitação**
> {data.objeto_licitacao or "Não extraído."}

---

### **Datas e Valores**
* **🗓️ Abertura das Propostas:** `{data.data_abertura or "Não informada"}`
* **🏁 Prazo Final para Proposta:** `{data.prazo_proposta or "Não informado"}`
* **💰 Valor Estimado:** R$ `{data.valor_estimado or "Não informado"}`

---
**Hash de Identificação:**
`{data.document_hash}`
"""
    
    return {"resumo_markdown": markdown_text}

@app.get("/test")
def test():
    return {"test": "ok", "version": "5.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)