#################################################################################################################################################################
###############################   1.  IMPORTING MODULES AND INITIALIZING VARIABLES   ############################################################################
#################################################################################################################################################################

from dotenv import load_dotenv
import os
import json
import pandas as pd
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
import shutil
import time

# NEW imports for file reading
from PyPDF2 import PdfReader
from docx import Document

load_dotenv()

###############################   INITIALIZE EMBEDDINGS MODEL  #################################################################################################

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

###############################   DELETE CHROMA DB IF EXISTS AND INITIALIZE   ##################################################################################

if os.path.exists(os.getenv("DATABASE_LOCATION")):
    shutil.rmtree(os.getenv("DATABASE_LOCATION"))

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"), 
)

###############################   INITIALIZE TEXT SPLITTER   ###################################################################################################

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

#################################################################################################################################################################
###############################   2.  FILE READER FUNCTIONS   ###################################################################################################
#################################################################################################################################################################

def process_json_lines(file_path):
    """Process each JSON line and extract relevant information."""
    extracted = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            extracted.append(obj)
    return extracted


def read_pdf(file_path):
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def read_docx(file_path):
    """Extract text from a DOCX file."""
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text.strip()


def read_txt(file_path):
    """Read a plain text file."""
    with open(file_path, encoding="utf-8") as f:
        return f.read().strip()


def read_csv(file_path):
    """Read all text content from a CSV file (concatenate columns)."""
    df = pd.read_csv(file_path)
    text = "\n".join(df.astype(str).apply(lambda x: " | ".join(x), axis=1))
    return text.strip()


#################################################################################################################################################################
###############################   3.  LOAD DATA FROM MULTIPLE SOURCES   #########################################################################################
#################################################################################################################################################################

file_content = []
data_folder = os.getenv("DATASET_STORAGE_FOLDER")

# ✅ Load JSON lines file if exists
json_path = os.path.join(data_folder, "data.txt")
if os.path.exists(json_path):
    file_content.extend(process_json_lines(json_path))

# ✅ Auto-scan folder for all supported files
for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    ext = filename.lower().split(".")[-1]

    text = None

    if ext == "pdf":
        text = read_pdf(file_path)
    elif ext == "docx":
        text = read_docx(file_path)
    elif ext == "txt" and filename != "data.txt":
        text = read_txt(file_path)
    elif ext == "csv":
        text = read_csv(file_path)
    elif ext == "json":
        # Handle JSON file (non-line-delimited)
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if "raw_text" in item:
                        file_content.append(item)
            continue

    if text:
        file_content.append({
            "url": file_path,
            "title": os.path.splitext(filename)[0],
            "raw_text": text
        })


#################################################################################################################################################################
###############################   4.  CHUNKING, EMBEDDING AND INGESTION   #######################################################################################
#################################################################################################################################################################

for line in file_content:
    if "raw_text" not in line or not line["raw_text"].strip():
        continue

    print(f"Ingesting: {line['title']}")

    texts = text_splitter.create_documents(
        [line["raw_text"]],
        metadatas=[{"source": line["url"], "title": line["title"]}]
    )

    uuids = [str(uuid4()) for _ in range(len(texts))]

    vector_store.add_documents(documents=texts, ids=uuids)

print("✅ Ingestion completed successfully.")
