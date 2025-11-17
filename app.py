# app.py
import os
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize the Flask application
app = Flask(__name__)
# Create a folder for uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Path for the LlamaCpp model and embeddings
# Please update this path with the name of your downloaded model file.
# Note: On Windows, use forward slashes (/) instead of backslashes (\) or a raw string (r"")
MODEL_PATH = "models/Llama-3.2-3B-Instruct-Q4_K_M.gguf" # Changed to forward slashes for cross-platform compatibility

# Global variables for the RAG system
vectorstore = None
qa_chain = None
llm = None
embeddings = None

def initialize_rag_system(file_path):
    """
    Processes the PDF file and sets up the RAG (Retrieval-Augmented Generation) system.

    This function loads the PDF, splits it into smaller chunks,
    converts these chunks into embeddings, and then creates a vector store.
    Finally, it sets up a QA chain with the LlamaCpp model.
    """
    global vectorstore, qa_chain, llm, embeddings

    print("Starting PDF loading...")
    try:
        # Check for the existence of the model file
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found. Please verify the correct path and file name.")

        # Load the PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
        texts = text_splitter.split_documents(documents)

        # Create embeddings using the LlamaCpp model
        print("Preparing embeddings...")
        embeddings = LlamaCppEmbeddings(model_path=MODEL_PATH)
        
        # Create a Chroma vector store
        print("Creating vector store...")
        vectorstore = Chroma.from_documents(texts, embeddings)
        
        # Initialize the LlamaCpp LLM
        print("Initializing LLM...")
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=0.5,  # Reduced temperature to minimize repetition
            max_tokens=2000,
            n_ctx=2048, # Increased context window for better performance
            verbose=False,
            n_gpu_layers=0  # Set to 0 for CPU execution
        )

        # Create a RetrievalQA chain to find answers
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            return_source_documents=True
        )
        print("RAG system successfully initialized.")
        return True
    except FileNotFoundError as e:
        print(f"File error during RAG system initialization: {e}")
        return False
    except Exception as e:
        print(f"Error preparing RAG system: {e}")
        return False

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading PDF
@app.route('/upload', methods=['POST'])
def upload_pdf():
    global vectorstore

    if 'pdf' not in request.files:
        return jsonify({"success": False, "message": "No PDF file provided."})
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"success": False, "message": "File name cannot be empty."})
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        if initialize_rag_system(file_path):
            return jsonify({"success": True, "message": f"'{file.filename}' successfully uploaded and processed. You can now ask questions."})
        else:
            return jsonify({"success": False, "message": "An error occurred while processing the PDF."})

# Route for question-answering (updated for streaming)
@app.route('/chat', methods=['POST'])
def chat():
    if not qa_chain:
        return jsonify({"response": "Please upload a PDF file first."})

    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"response": "Please enter a question."})

    def generate_chunks():
        try:
            retrieved_docs = qa_chain.retriever.get_relevant_documents(user_message)
            
            # --- Modified Prompt Template for English-only and PDF-scope handling ---
            template = """Based on the provided context, answer the user's question concisely and directly in English.
            Do not add any extraneous information, ask further questions, or repeat your answer.
            If the question is not directly answerable by the context, or if it falls outside the scope of the document,
            state professionally that the answer can only be provided from the uploaded document.
            If the answer is not present in the context, explicitly state: "I apologize, but the answer is not available in the provided document."

            Context:
            {context}

            Question: {question}
            """
            
            prompt = PromptTemplate.from_template(template)

            context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
            formatted_prompt = prompt.format(context=context_text, question=user_message)

            for chunk in llm.stream(formatted_prompt):
                yield chunk
        except Exception as e:
            print(f"Error during streaming: {e}")
            yield "I apologize, an issue occurred while retrieving the answer."

    return Response(stream_with_context(generate_chunks()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
