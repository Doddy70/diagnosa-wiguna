import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()



def create_db_from_multiple_pdfs(pdf_directory="./pdfs", collection_name="car"):
    """
    Process multiple PDF files and create a Milvus vector database.
    
    Args:
        pdf_directory: Directory containing PDF files
        collection_name: Name of the Milvus collection
    """
    # Find all PDF files
    pdf_files = glob.glob(f"{pdf_directory}/*.pdf")
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_directory}")
        return
    
    print(f"📚 Found {len(pdf_files)} PDF files")
    print(f"📂 Directory: {pdf_directory}")
    print("-" * 60)
    
    all_documents = []
    failed_files = []
    
    # Process each PDF with progress bar
    for pdf_file in tqdm(pdf_files, desc="Loading PDFs"):
        try:
            print(f"\n📄 Processing: {Path(pdf_file).name}")
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            
            # Add metadata to track source
            for doc in documents:
                doc.metadata['source_file'] = Path(pdf_file).name
            
            all_documents.extend(documents)
            print(f"   ✅ Loaded {len(documents)} pages")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
            failed_files.append(pdf_file)
    
    print("\n" + "=" * 60)
    print(f"📊 Summary:")
    print(f"   • Total documents loaded: {len(all_documents)}")
    print(f"   • Successful files: {len(pdf_files) - len(failed_files)}")
    print(f"   • Failed files: {len(failed_files)}")
    
    if failed_files:
        print(f"\n⚠️  Failed files:")
        for f in failed_files:
            print(f"   - {Path(f).name}")
    
    if not all_documents:
        print("\n❌ No documents to process. Exiting.")
        return
    
    # Split documents into chunks
    print("\n🔪 Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # Larger chunks for better context
        chunk_overlap=50,      # Overlap to maintain continuity
        length_function=len,
    )
    texts = text_splitter.split_documents(all_documents)
    print(f"   ✅ Created {len(texts)} text chunks")
    
    # Create embeddings and store in Milvus
    print("\n🚀 Creating embeddings and storing in Milvus...")
    print("   (This may take several minutes depending on the number of chunks)")
    
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    
    milvus_uri = os.environ.get("MILVUS_URI")
    milvus_token = os.environ.get("MILVUS_TOKEN")
    milvus_host = os.environ.get("MILVUS_HOST", "localhost")
    milvus_port = os.environ.get("MILVUS_PORT", "19530")

    connection_args = {}
    if milvus_uri:
        connection_args["uri"] = milvus_uri
        if milvus_token:
            connection_args["token"] = milvus_token
    else:
        connection_args["host"] = milvus_host
        connection_args["port"] = milvus_port

    try:
        vector_db = Milvus.from_documents(
            texts, 
            embeddings, 
            collection_name=collection_name,
            connection_args=connection_args
        )
        print(f"\n✅ Successfully created vector database!")
        print(f"   • Collection name: {collection_name}")
        print(f"   • Total chunks indexed: {len(texts)}")
        
    except Exception as e:
        print(f"\n❌ Failed to create vector database: {str(e)}")
        print("   Make sure Milvus is running: docker compose up -d")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Knowledge base update complete!")
    print("=" * 60)


if __name__ == '__main__':
    # Process PDFs from SOP BENGKEL WIGUNA directory
    create_db_from_multiple_pdfs(
        pdf_directory="/Users/doddykapisha/Documents/SOP BENGKEL WIGUNA", 
        collection_name="car"
    )
