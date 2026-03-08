<h1>Architecture Diagram</h1>

<img width="500" height="700" alt="Blank diagram" src="https://github.com/user-attachments/assets/0d82e641-b6a8-46a6-a425-c13cdadd7d54" />
<br>

<h1>RAG Workflow Explanation</h1><br>
This project implements a Retrieval-Augmented Generation (RAG) architecture to build a nutrition-focused AI assistant. <br>
The workflow follows these steps:<br>
<h2>1. Document Ingestion</h2> <br>
Nutrition-related PDF documents are collected and converted into structured JSON format. Each document is cleaned and split into smaller chunks to improve retrieval accuracy.
<h2>2. Chunking</h2> <br>
Large documents are divided into smaller segments (chunks) of approximately 300–500 words. Chunking ensures that each unit of information is semantically meaningful and compatible with embedding token limits.
<h2>3. Embedding Generation</h2> <br>
Each chunk is converted into a numerical vector representation using the Mistral embedding model. These embeddings capture the semantic meaning of the text.
<h2>4. Vector Storage</h2> <br>
All document embeddings are stored in memory (NumPy array) and cached locally. This allows fast similarity comparisons when user queries are received.
<h2>5. Query Processing</h2> <br>
When a user submits a question: <br>
1.	The query is converted into an embedding.<br>
2.	The query embedding is compared against document embeddings.<br>
3.	The most relevant document chunks are retrieved.<br>
<h2>6. Context Injection</h2><br>
The top relevant chunks are inserted into a prompt together with the user question.<br>
<h2>7. Response Generation</h2>
The prompt is sent to the Mistral LLM, which generates an answer grounded in the retrieved context.<br>
________________________________________<br>
<h1>Embedding Strategy</h1><br>
Embeddings are used to convert text into dense vector representations that capture semantic relationships.<br>
Model Used<br>
mistral-embed<br>
<h2>Strategy</h2><br>
1.	Each document chunk is embedded once during system initialization.<br>
2.	Embeddings are cached locally to avoid recomputation.<br>
3.	Query embeddings are generated dynamically for each user query.<br>
Advantages<br>
•	Captures semantic similarity between questions and documents<br>
•	Allows retrieval even when exact keywords are not present<br>
•	Improves answer accuracy compared to keyword search<br>
________________________________________<br>
<h1>Similarity Search Explanation</h1><br>
To retrieve relevant document chunks, the system uses cosine similarity.<br>
Process<br>
1.	Generate embedding for user query<br>
2.	Compare query vector with all document vectors<br>
3.	Calculate similarity scores<br>
4.	Select Top-K most similar chunks<br><br>
Cosine Similarity Formula<br>
similarity(A,B) = (A · B) / (||A|| * ||B||)<br><br>
Where:<br>
•	A = query embedding<br>
•	B = document embedding<br><br>
<h2>Retrieval Strategy</h2><br>
Top-K Retrieval = 3<br>
Only the three most relevant chunks are passed to the LLM.<br>
A similarity threshold is also used to prevent unrelated responses.<br>
________________________________________<br>
<h1>Prompt Design Reasoning</h1><br>
Prompt design ensures that the language model produces grounded and factual answers based only on retrieved documents.<br>
Prompt Structure<br>
You are a nutrition assistant.<br><br>

Answer the user's question ONLY using the provided context.<br><br>

If the answer is not present in the context, say:<br>
"I do not have enough information."<br><br>

Context:<br>
{retrieved_chunks}<br><br>

Conversation History:<br>
{previous_messages}<br><br>

User Question:<br>
{query}<br><br>
Design Principles<br>
1. Context Grounding<br>
The model is explicitly instructed to use only the retrieved information.<br>
2. Hallucination Prevention<br>
If no relevant information is found, the model returns a fallback response.<br>
3. Concise Responses<br>
Temperature is kept low to ensure factual and deterministic answers.<br>
________________________________________<br>
<h1>Setup Instructions</h1><br>
<h2>1. Clone the Repository</h2><br>
git clone https://github.com/your-username/genai-chat-assistant.git<br>
cd genai-chat-assistant<br>
________________________________________
<h2>2. Create Virtual Environment</h2><br>
python -m venv venv<br>
Activate environment:<br>
Windows<br>
venv\Scripts\activate<br>
Mac/Linux<br>
source venv/bin/activate<br>
________________________________________
<h2>3. Install Dependencies</h2><br>
pip install -r requirements.txt<br>
Example dependencies:<br>
flask<br>
numpy<br>
scikit-learn<br>
mistralai<br>
pdfplumber<br>
________________________________________
<h2>4. Set API Key</h2><br>
Set the Mistral API key in your shell.<br>
Windows PowerShell<br>
$env:MISTRAL_API_KEY="your_api_key"<br>
Mac/Linux<br>
export MISTRAL_API_KEY="your_api_key"<br>
________________________________________
<h2>5. Run the Application</h2><br>
python app.py<br>
Open browser:<br>
http://127.0.0.1:5000<br>
________________________________________
<h2>6. Chat with the Assistant</h2><br>
Ask questions such as:<br>
What foods help control diabetes?<br>
Which foods are rich in iron?<br>
What diet helps control hypertension?<br>
The assistant will retrieve relevant document chunks and generate grounded responses.<br>
________________________________________<br>
<h2>Result</h2><br>
This system demonstrates a production-style RAG pipeline that includes:<br>
•	document ingestion<br>
•	semantic embeddings<br>
•	vector similarity search<br>
•	context-aware prompting<br>
•	LLM response generation<br>
The assistant provides nutrition and health-related answers grounded in the provided document knowledge base.<br>
________________________________________



