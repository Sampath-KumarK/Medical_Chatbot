
# Medical RAG Chatbot

A local, document-grounded medical question-answering chatbot built with
Streamlit, Sentence Transformers, ChromaDB, and Ollama.

The application answers questions using the content of a medical PDF. It uses
retrieval-augmented generation (RAG): relevant PDF text is retrieved from a
local vector database and supplied to a local language model as context.

> **Important:** This project is for educational purposes only. It is not a
> substitute for a qualified medical professional, diagnosis, or emergency
> care.

## Features

- Extracts text from PDF documents.
- Splits extracted text into overlapping chunks.
- Converts chunks into vector embeddings with
  `all-MiniLM-L6-v2`.
- Persists embeddings and documents in ChromaDB.
- Retrieves the three most relevant chunks for each question.
- Generates an answer with the local Ollama model `llama3.2:3b`.
- Displays the generated answer and the retrieved context in the Streamlit UI.
- Keeps data local; the current application does not call a hosted LLM API.

## How The RAG Pipeline Works

```text
Medical PDF
	|
	v
PDF text extraction (utils/pdf_loader.py)
	|
	v
Overlapping chunks: 500 characters, 50-character overlap
	|
	v
Sentence Transformer embeddings
	|
	v
Persistent ChromaDB collection: medical_collection
	|
	v
User question -> question embedding -> top 3 similar chunks
	|
	v
Ollama prompt containing question + retrieved context
	|
	v
Answer and retrieved context shown in Streamlit
```

## Project Structure

```text
Medicaladvice_chatbot/
|-- app.py                  # Streamlit user interface and RAG orchestration
|-- config.py               # Reserved for application configuration
|-- requirements.txt        # Python dependencies
|-- README.md
|-- data/                   # Place source medical PDFs here
|-- db/                     # Persistent ChromaDB files
|   |-- chroma.sqlite3
|   `-- <collection-id>/
`-- utils/
	|-- pdf_loader.py       # PDF text extraction
	|-- chunker.py          # Text chunking with overlap
	|-- embedding.py        # Sentence Transformer embedding model
	|-- chroma_db.py        # ChromaDB storage
	|-- retriever.py        # Similarity search
	`-- llm.py              # Ollama answer generation
```

## Requirements

- Python 3.9 or newer
- Ollama installed and running
- The Ollama model `llama3.2:3b`
- A readable, text-based medical PDF

The Python packages used by the project are pinned in `requirements.txt`:

```text
streamlit==1.50.0
ollama==0.6.2
pypdf==6.1.2
sentence-transformers==5.1.1
chromadb==1.0.20
```

## Installation

Open PowerShell in the project directory and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Ollama from [ollama.com](https://ollama.com), then download the model:

```powershell
ollama pull llama3.2:3b
```

Ollama must be available before asking a question. On most installations the
Ollama application starts its local service automatically. Otherwise run:

```powershell
ollama serve
```

## Add And Index A Medical PDF

Place a PDF in the `data/` directory. The repository contains the reusable
loader, chunker, embedding, and ChromaDB functions, but it does not currently
contain a separate indexing command. Run the following one-time script from
the project root to build or replace the collection:

```powershell
python -c "from utils.pdf_loader import load_pdf; from utils.chunker import split_text; from utils.embedding import create_embeddings; from utils.chroma_db import store_embeddings; text=load_pdf('data/medical_document.pdf'); chunks=split_text(text); embeddings=create_embeddings(chunks); print(f'Extracted characters: {len(text)}'); print(f'Created chunks: {len(chunks)}'); print(f'Stored embeddings: {store_embeddings(chunks, embeddings)}')"
```

Replace `data/medical_document.pdf` with the real PDF filename. The command
deletes the existing documents in `medical_collection` before storing the new
ones, because `store_embeddings` is currently designed for development and
re-indexing one source document at a time.

For a more readable Python script, the same process is:

```python
from utils.chroma_db import store_embeddings
from utils.chunker import split_text
from utils.embedding import create_embeddings
from utils.pdf_loader import load_pdf

text = load_pdf("data/medical_document.pdf")
chunks = split_text(text)
embeddings = create_embeddings(chunks)
stored_count = store_embeddings(chunks, embeddings)

print(f"Extracted characters: {len(text)}")
print(f"Created chunks: {len(chunks)}")
print(f"Stored embeddings: {stored_count}")
```

## Run The Chatbot

After indexing the PDF, start Streamlit:

```powershell
streamlit run app.py
```

Open the local URL displayed by Streamlit, usually
`http://localhost:8501`. Enter a question and select **Ask**.

## Output Conditions

The current UI behaves as follows:

| Condition | Application output |
|---|---|
| The question is empty or contains only spaces | Shows `Please enter a question.` and does not query the database. |
| The question is valid and matching chunks exist | Shows the Ollama-generated answer and an expandable `Retrieved Context` section. |
| The answer is not supported by the retrieved context | Ollama is instructed to return `I couldn't find this information in the provided medical document.` |
| The ChromaDB collection has not been indexed | Retrieval can return no usable context, or the application may fail depending on the ChromaDB response. Index the PDF first. |
| Ollama is unavailable or the model is missing | Answer generation fails until Ollama is running and `llama3.2:3b` is available. |
| The PDF has no extractable text, such as a scanned image-only document | No useful chunks are created. Use OCR or a text-based PDF first. |

The final page also displays the permanent notice:

```text
Educational purposes only. Not medical advice.
```

## Code Explanation

### PDF loading: `utils/pdf_loader.py`

`load_pdf(pdf_path)` creates a `PdfReader`, loops through every page, calls
`extract_text()`, and joins the extracted page text into one string. Pages that
return no text are skipped.

### Chunking: `utils/chunker.py`

```python
split_text(text, chunk_size=500, overlap=50)
```

The function slices the text into 500-character chunks. The next chunk starts
450 characters after the previous one, so 50 characters are shared between
adjacent chunks. This overlap helps preserve context across chunk boundaries.

For a text length of $L$, chunk size $C$, and overlap $O$, the approximate
number of chunks is:

$$
\left\lceil\frac{L-C}{C-O}\right\rceil + 1
$$

### Embeddings: `utils/embedding.py`

The module loads the Sentence Transformers model
`all-MiniLM-L6-v2` once when imported. `create_embeddings(chunks)` converts
each chunk into a numeric vector. Similar meanings produce vectors that are
close together in embedding space.

The same model is used for the user question during retrieval. Using the same
embedding model for documents and queries is necessary for meaningful
similarity search.

### ChromaDB storage: `utils/chroma_db.py`

The project uses:

```python
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection(name="medical_collection")
```

`PersistentClient` stores the vector database on disk in `db/`, so the data
survives application restarts. `store_embeddings` assigns string IDs,
associates each embedding with its original text chunk, and adds both to the
collection. Existing records are deleted first in the current development
implementation.

### Retrieval: `utils/retriever.py`

`retrieve_chunks(question, embedding_model, top_k=3)` embeds the question,
queries ChromaDB with that vector, and returns the three nearest document
chunks. The retrieved chunks are joined into a context string in `app.py`.

### Answer generation: `utils/llm.py`

`generate_answer(question, context)` builds a prompt that tells Ollama to use
only the supplied context. It calls:

```python
ollama.chat(model="llama3.2:3b", messages=[...])
```

The answer text is returned from `response["message"]["content"]` and
rendered by Streamlit.

### Streamlit interface: `app.py`

The app collects the question, validates it, retrieves relevant chunks,
generates an answer, and displays both the answer and the source context.
The context expander is useful for checking which document passages informed
the response.

## Troubleshooting

### `No module named ...`

Activate the virtual environment and reinstall the dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### No answer is generated

Check that Ollama is running and that the model exists:

```powershell
ollama list
ollama run llama3.2:3b
```

### Retrieval returns no useful information

Confirm that the PDF was indexed successfully, that the PDF contains
extractable text, and that the `db/` directory is the same project directory
from which Streamlit is running.

### The model gives an unsupported answer

The prompt requests context-only answers, but language models can still make
mistakes. Review the retrieved context, verify the original medical source,
and consult a qualified professional for medical decisions.

## Limitations And Security Notes

- This is a prototype, not a clinically validated system.
- The answer depends on the quality and completeness of the indexed PDF.
- The current database reset behavior is unsuitable for multi-document
  production indexing without modification.
- Do not upload or index sensitive patient information unless the environment,
  storage, access controls, and applicable regulations have been reviewed.
- Scanned PDFs require OCR before `pypdf` can extract useful text.

## License

No license has been specified for this project yet. Add an appropriate license
before distributing the code publicly.
