# 📄 PDF AI Chatbot with Local LLM

A powerful, cost-effective RAG (Retrieval-Augmented Generation) system that allows you to chat with your PDF documents locally. This project uses a LlamaCpp model, eliminating the need for paid API services and ensuring complete data privacy.

-----

## **Key Features**

  - **Zero API Costs**: Utilizes a local Large Language Model (LLM) (`Llama-3.2-3B-Instruct-Q4_K_M.gguf`), meaning there are no recurring costs for API usage.
  - **RAG Architecture**: Efficiently retrieves information from your PDF and uses it to generate accurate, context-aware responses.
  - **User-Friendly Interface**: A clean and modern web interface built with Flask and Tailwind CSS.
  - **Streaming Responses**: Delivers chatbot responses in real-time, providing a smooth and interactive user experience.

-----

## **Tech Stack**

  - **Backend**: Python, Flask
  - **Core AI**: `Llama-3.2-3B-Instruct-Q4_K_M.gguf` (a local LlamaCpp model)
  - **Frameworks**:
      - **LangChain**: For building the RAG pipeline.
      - **Chroma**: A lightweight vector store for document embeddings.
  - **Document Processing**: `pypdf` for handling PDF documents.
  - **Frontend**: HTML, JavaScript, and Tailwind CSS (via CDN)

-----

## **How to Run the Project**

### **Step 1: Setup the Environment**

First, set up a Python virtual environment and install the required libraries. This is a crucial step to manage project dependencies.

```bash
# Purge pip cache to avoid conflicts
pip cache purge

# Create and activate the virtual environment
conda create --name rag_chatbot python=3.10 -y
conda activate rag_chatbot

# Install core dependencies
pip install Flask langchain langchain-community pypdf

# Install the LlamaCpp Python binding (this may take some time)
pip install "llama-cpp-python>=0.2.78"
```

### **Step 2: Place the LLM Model**

Download the `Llama-3.2-3B-Instruct-Q4_K_M.gguf` model file and place it in the designated `models` folder at the root of your project directory. This is the model that will power your chatbot.

```
project_root/
├── app.py
├── templates/
├── uploads/
└── models/
    └── Llama-3.2-3B-Instruct-Q4_K_M.gguf
```

### **Step 3: Run the Application**

Start the Flask server by running the `app.py` file.

```bash
python app.py
```

After a moment, you will see a message indicating the server is running on `http://127.0.0.1:5000`. Open this URL in your web browser.

### **Step 4: Upload a PDF**

On the web interface, click the "Select a PDF file" button and choose a PDF document. Then, click "Process PDF". The system will process the document and prepare the chatbot. This step may take some time depending on the size of the PDF and your system's performance.

### **Step 5: Start the Chat**

Once the processing is complete, the chat interface will appear. You can now ask questions related to the content of your uploaded PDF. The chatbot will retrieve relevant information and provide a concise, accurate answer based on the document.


### How It Works (The RAG Process)

This application uses a special technique called **Retrieval-Augmented Generation (RAG)**. RAG makes sure the AI's answers are accurate because it forces the AI to look at a specific document for the answer, instead of using its general knowledge.

Here is a simple flowchart explaining the process:

**1. Preparation** 📖
First, the app prepares the document for the AI.

* **Load PDF:** When you upload a PDF, the app reads all the text inside it.
* **Split into Chunks:** The long document is broken down into small pieces of text, called **chunks**. This makes the data easier to work with.
* **Create Embeddings:** Each text chunk is turned into a special numerical code called an **embedding**. This code captures the meaning of the text.
* **Save to Vector Store:** All these embeddings are saved in a special database called a **vector store**. This database is like a super-fast search engine for similar meanings.

**2. Question and Answer** 🧠
Next, the app answers your question using the prepared data.

* **User Question:** You type your question.
* **Retrieve Relevant Chunks:** The app takes your question, turns it into an embedding, and searches the vector store to find the chunks that are most similar or relevant to your question. This is the **Retrieval** step.
* **Generate Answer:** The relevant chunks from the PDF and your original question are given to an AI model (**LlamaCpp** in this case). The AI then generates a complete answer using *only* the provided information. This is the **Generation** step.

This whole process ensures that the AI's answer is based entirely on the PDF you provided.

***

### Technologies Used

* **Flask:** The web framework for building the application.
* **LangChain:** A powerful framework used to connect all the components of the RAG system.
* **LlamaCpp:** A library that runs the powerful Llama-3 AI model on your computer.
* **ChromaDB:** The **vector store** that efficiently saves and searches through the document chunks.
* **PyPDFLoader:** A tool to load and read text from PDF files.

***