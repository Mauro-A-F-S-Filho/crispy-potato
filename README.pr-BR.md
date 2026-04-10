# Markdown API (PDF → Texto/Markdown + Dados Estruturados)

[English](README.md) | Português

Esta API automatiza o processamento de documentos PDF:
- recebe um PDF (comumente em Base64 a partir do n8n),
- extrai o texto,
- gera Markdown formatado,
- e retorna um JSON que pode ser usado por nós seguintes (LLM/extração) e persistência em banco.

## Exemplo de saída
Veja: `examples/output.example.json`

## Uso no n8n (workflow)
Esta API foi pensada para funcionar dentro de um fluxo no n8n:

1. Converter arquivo para Base64 (nó do n8n)
2. HTTP Request → chama esta API
3. Information Extractor (LLM) → extrai os principais campos
4. Inserção no banco

### NÓ da API (HTTP Request)
![HTTP Request node](docs/images/API_workinnode_N8Nworkflow.png)

### Parameteros nó API
![Parameters](docs/images/API_nodeN8Nparam.png)

## Visão geral (Request/Response)
- Entrada: conteúdo do PDF (Base64) + nome do arquivo (opcional)
- Saída: JSON com `filename`, `document_hash`, `extracted_text`, `markdown_content`, `success`, `error`

## Observações
- PDFs grandes podem gerar respostas grandes. Se necessário, guarde o texto completo em storage externo.
