# AI Customer Support & Knowledge Copilot

An AI-powered customer support system that combines **Retrieval-Augmented Generation (RAG)**, hybrid search, conversation memory, intent/sentiment/priority classification, database-backed support tools, human escalation, and analytics.

The project is designed as a **production-style prototype** demonstrating how modern AI components can be combined into a practical customer-support workflow.

---

## 🚀 Features

### AI & RAG

* Knowledge-base question answering using RAG
* HTML knowledge-base ingestion
* Paragraph-aware document chunking
* Sentence-transformer embeddings
* FAISS vector search
* BM25 keyword retrieval
* Hybrid semantic + keyword retrieval
* Source citations for retrieved knowledge
* Grounded response generation using a local LLM
* RAG evaluation using Hit@3 and MRR

### Conversation Intelligence

* Conversation memory
* Intent classification
* Sentiment analysis
* Priority classification
* Structured outputs using Pydantic
* Context-aware follow-up questions

### Customer Support Tools

* Customer lookup
* Order-status lookup
* Support-ticket creation
* LLM tool calling
* Human-support escalation
* Priority-based escalation handling

### Data & Backend

* FastAPI REST API
* SQLite database
* SQLAlchemy ORM
* Customer management
* Order management
* Support tickets
* Analytics event storage

### Analytics

* Request tracking
* Response-time measurement
* Intent distribution
* Priority distribution
* Escalation tracking
* Escalation rate
* Admin analytics dashboard

### Interface & Deployment

* Streamlit customer-support interface
* Streamlit admin analytics dashboard
* Dockerized FastAPI backend
* Local Ollama LLM integration

---

# ⚡ Quick Start

For a fresh local setup:

```bash
git clone <repository-url>
cd ai_support_copilot

python3.13 -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt

ollama list

python create_database.py
python seed_database.py
python build_index.py
```

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

In a **second terminal**, activate the environment and start Streamlit:

```bash
cd /path/to/ai_support_copilot
source myenv/bin/activate

streamlit run streamlit_app.py
```

Then open:

```text
Streamlit:
http://localhost:8501

FastAPI:
http://localhost:8000

FastAPI docs:
http://localhost:8000/docs
```

### Quick API Test

With the FastAPI server running:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"quick-start","prompt":"How can I request a refund?"}'
```

### Quick Docker Start

If Docker is already installed and Ollama is running on the host:

```bash
docker build -t ai-support-copilot .

docker run --rm -p 8000:8000 \
  -e MODEL_NAME=llama3.2 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  ai-support-copilot
```

---

# 🏗️ Architecture

```text
                         ┌─────────────────────────┐
                         │     Streamlit UI        │
                         │                         │
                         │ Customer Support        │
                         │ Admin Analytics         │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API       │
                         │                         │
                         │      /chat              │
                         │      /analytics         │
                         │      /analytics/metrics │
                         └────────────┬────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
        ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
        │  Classifier    │   │   RAG System   │   │  Tool System   │
        │                │   │                │   │                │
        │ Intent         │   │ FAISS          │   │ Orders         │
        │ Sentiment      │   │ BM25           │   │ Customers      │
        │ Priority       │   │ Hybrid Search  │   │ Tickets        │
        └────────────────┘   └───────┬────────┘   └───────┬────────┘
                                     │                    │
                                     ▼                    ▼
                              ┌──────────────┐     ┌──────────────┐
                              │ Knowledge    │     │   SQLite     │
                              │ Base         │     │  Database    │
                              │              │     │              │
                              │ HTML Docs    │     │ Customers    │
                              │ Chunks       │     │ Orders       │
                              │ Metadata     │     │ Tickets      │
                              └──────────────┘     │ Analytics    │
                                                   └──────────────┘

                              ┌─────────────────┐
                              │   Ollama LLM    │
                              │    llama3.2     │
                              └─────────────────┘
```

---

# 🔄 Request Flow

A typical customer request follows this flow:

```text
Customer Message
       │
       ▼
Conversation Memory
       │
       ▼
Intent / Sentiment / Priority Analysis
       │
       ├───────────────┐
       │               │
       ▼               ▼
Knowledge Query     Tool Request
       │               │
       ▼               ▼
Hybrid Retrieval    Database Tool
       │               │
       └───────┬───────┘
               ▼
          LLM Response
               │
               ▼
       Source Information
               │
               ▼
        Analytics Event
               │
               ▼
          Final Response
```

High-priority requests can additionally trigger a support-ticket escalation.

---

# 🛠️ Tech Stack

| Category         | Technology            |
| ---------------- | --------------------- |
| Language         | Python                |
| API              | FastAPI               |
| LLM              | Ollama / Llama 3.2    |
| Embeddings       | Sentence Transformers |
| Vector Search    | FAISS                 |
| Keyword Search   | BM25                  |
| RAG              | Custom RAG pipeline   |
| Validation       | Pydantic              |
| Database         | SQLite                |
| ORM              | SQLAlchemy            |
| UI               | Streamlit             |
| Testing          | Pytest                |
| Containerization | Docker                |
| Version Control  | Git / GitHub          |

---

# 📁 Project Structure

```text
ai_support_copilot/
│
├── app/
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── ingestion/
│   │   ├── html_loader.py
│   │   ├── chunker.py
│   │   └── ingest.py
│   │
│   ├── memory/
│   │   └── conversation.py
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── hybrid_retriever.py
│   │
│   ├── services/
│   │   ├── llm.py
│   │   ├── embeddings.py
│   │   ├── rag.py
│   │   ├── classifier.py
│   │   ├── tools.py
│   │   ├── escalation.py
│   │   └── analytics.py
│   │
│   ├── tools/
│   │   ├── orders.py
│   │   ├── customers.py
│   │   └── tickets.py
│   │
│   ├── vector_store/
│   │   ├── faiss_store.py
│   │   └── storage.py
│   │
│   ├── config.py
│   ├── main.py
│   └── schemas.py
│
├── data/
│   ├── documents/
│   │   ├── shopify_returns.html
│   │   └── shipping.html
│   │
│   └── vector_store/
│
├── evaluation_dataset.py
├── evaluate_rag.py
├── build_index.py
├── create_database.py
├── seed_database.py
├── streamlit_app.py
│
├── test_llm.py
├── test_loader.py
├── test_embeddings.py
├── test_vector_store.py
├── test_persistent_store.py
├── test_retriever.py
├── test_bm25.py
├── test_memory.py
├── test_classifier.py
├── test_rag.py
├── test_order_tool.py
├── test_customer_tool.py
├── test_ticket_tool.py
├── test_tool_calling.py
├── test_retrieval_scores.py
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd ai_support_copilot
```

---

## 2. Create a virtual environment

Python 3.13 is used for the project.

```bash
python3.13 -m venv myenv
```

Activate it:

```bash
source myenv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

The project uses a local Ollama model for response generation and tool calling.

Check installed models:

```bash
ollama list
```

The current project configuration uses:

```text
llama3.2
```

Make sure Ollama is running before starting the application.

The model can be configured using `.env`:

```env
APP_ENV=development
MODEL_NAME=llama3.2
```

---

# 📚 Knowledge Base

The knowledge base currently contains support documentation such as:

```text
data/documents/
├── shopify_returns.html
└── shipping.html
```

The ingestion pipeline:

```text
HTML Documents
      │
      ▼
HTML Loader
      │
      ▼
Clean Text
      │
      ▼
Paragraph-aware Chunking
      │
      ▼
Sentence Transformer Embeddings
      │
      ▼
FAISS Vector Store
      │
      ▼
Stored Metadata
```

Build the vector index with:

```bash
python build_index.py
```

---

# 🗄️ Database

The application uses SQLite with SQLAlchemy.

The database stores:

* Customers
* Orders
* Support tickets
* Analytics events

Create the database:

```bash
python create_database.py
```

Seed sample customer and order data:

```bash
python seed_database.py
```

The application also creates missing database tables automatically when the FastAPI application starts.

---

# 🔎 Hybrid Retrieval

The retrieval system combines two approaches:

### Semantic Retrieval

Uses sentence-transformer embeddings and FAISS to find semantically similar documents.

### Keyword Retrieval

Uses BM25 to find documents based on keyword relevance.

### Hybrid Ranking

The two retrieval signals are combined using rank-based scoring.

```text
                    Customer Query
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Semantic Search          BM25 Search
              │                     │
              ▼                     ▼
            FAISS                Keywords
              │                     │
              └──────────┬──────────┘
                         ▼
                  Hybrid Ranking
                         │
                         ▼
                  Top-K Documents
```

This allows the system to benefit from both semantic similarity and exact keyword matching.

---

# 🧠 Conversation Memory

Conversation history is maintained using the conversation-memory service.

This allows follow-up questions such as:

```text
User:
Where is my order ORD1001?

Assistant:
Your order is currently shipped.

User:
What happens if it is delayed?
```

The second question can be interpreted using the previous conversation context.

The current memory implementation is **in-process memory**, so it does not survive a server restart.

---

# 🎯 Intent, Sentiment & Priority

Each customer message is analyzed for:

### Intent

Examples include:

* `return_request`
* `refund_request`
* `shipping_question`
* `order_status`
* `exchange_request`
* `cancellation_request`
* `general_question`
* `other`

### Sentiment

```text
positive
neutral
negative
```

### Priority

```text
low
medium
high
```

The classifier uses structured Pydantic output to keep the result predictable.

---

# 🔧 Tool Calling

The system provides database-backed tools to the LLM.

### Order Tool

```text
get_order_status(order_number)
```

Used for questions such as:

```text
Where is my order ORD1001?
```

### Customer Tool

```text
get_customer_by_email(email)
```

Used to retrieve customer information from the database.

### Ticket Tool

```text
create_support_ticket(...)
```

Used to create a support ticket when human assistance is required.

---

# 🚨 Human Escalation

High-priority requests can be escalated to human support.

The escalation workflow:

```text
Customer Request
      │
      ▼
Priority Analysis
      │
      ▼
High Priority?
   ┌──┴──┐
   │     │
  Yes    No
   │     │
   ▼     ▼
Create   Normal
Ticket   Response
```

Support tickets are stored in the SQLite database.

---

# 📊 Analytics

The system records analytics events for customer requests.

Tracked information includes:

* Conversation ID
* Customer prompt
* Intent
* Sentiment
* Priority
* Response time
* Escalation status
* Timestamp

Available backend endpoints include:

```text
GET /analytics
GET /analytics/metrics
```

Metrics include:

* Total requests
* Average response time
* Escalated requests
* Escalation rate
* Intent distribution
* Priority distribution

---

# 🖥️ Streamlit Interface

Run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The interface provides two main areas:

### Customer Support

* Send customer questions
* Maintain conversation context
* View generated responses
* View retrieved sources
* View analysis information

### Admin Analytics

* Total requests
* Average response time
* Escalated requests
* Escalation rate
* Intent distribution
* Priority distribution

---

# 🚀 FastAPI Backend

Start the backend:

```bash
uvicorn app.main:app --reload
```

The API runs at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# 💬 Example API Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id":"demo","prompt":"How can I request a refund?"}'
```

Example response structure:

```json
{
  "prompt": "How can I request a refund?",
  "response": "...",
  "analysis": {
    "intent": "return_request",
    "sentiment": "neutral",
    "priority": "medium"
  },
  "sources": [
    {
      "text": "...",
      "source": "shopify_returns.html",
      "chunk_id": 0,
      "distance": 0.85
    }
  ]
}
```

---

# 📈 RAG Evaluation

The project includes a small manually defined evaluation dataset.

Evaluation queries cover areas such as:

* Refund requests
* Shipping duration
* Delayed orders
* Returns

Run the evaluation:

```bash
python evaluate_rag.py
```

Metrics:

* **Hit@3** — whether the relevant document appears in the top 3 retrieved documents.
* **MRR (Mean Reciprocal Rank)** — measures how highly the relevant document is ranked.

Current evaluation result on the included dataset:

```text
Hit@3: 1.00
MRR:   1.00
```

These results apply only to the included evaluation dataset and **should not be interpreted as general production accuracy**.

---

# 🧪 Testing

The project contains tests for the major components of the system.

Run the complete test suite:

```bash
pytest
```

### Test Files

| Test                       | Purpose                                        |
| -------------------------- | ---------------------------------------------- |
| `test_llm.py`              | LLM service                                    |
| `test_loader.py`           | Knowledge-base document loading                |
| `test_embeddings.py`       | Sentence-transformer embeddings                |
| `test_vector_store.py`     | FAISS vector store                             |
| `test_persistent_store.py` | Persistent vector-store storage                |
| `test_retriever.py`        | Retrieval pipeline                             |
| `test_bm25.py`             | BM25 keyword retrieval                         |
| `test_retrieval_scores.py` | Retrieval-score inspection                     |
| `test_memory.py`           | Conversation memory                            |
| `test_classifier.py`       | Intent, sentiment, and priority classification |
| `test_rag.py`              | RAG pipeline                                   |
| `test_order_tool.py`       | Order lookup tool                              |
| `test_customer_tool.py`    | Customer lookup tool                           |
| `test_ticket_tool.py`      | Support-ticket creation                        |
| `test_tool_calling.py`     | LLM tool-calling workflow                      |

The tests cover individual components as well as important interactions between retrieval, RAG, classification, database tools, memory, and tool calling.

---

# 🐳 Docker

The FastAPI backend can be containerized using Docker.

Build the image:

```bash
docker build -t ai-support-copilot .
```

Run the container:

```bash
docker run --rm -p 8000:8000 \
  -e MODEL_NAME=llama3.2 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  ai-support-copilot
```

The API will then be available at:

```text
http://localhost:8000
```

### Docker Architecture

```text
┌─────────────────────────────────┐
│          Docker Container       │
│                                 │
│       FastAPI Application       │
│       RAG / Tools / Analytics   │
└───────────────┬─────────────────┘
                │
                │ HTTP
                ▼
┌─────────────────────────────────┐
│        Host Machine             │
│                                 │
│            Ollama               │
│           llama3.2              │
└─────────────────────────────────┘
```

Ollama runs outside the container and the Dockerized backend connects to it through:

```text
host.docker.internal:11434
```

---

# 🧩 Key Design Decisions

### Local LLM

Ollama is used instead of a paid hosted LLM during development to keep the project inexpensive and allow local experimentation.

### Hybrid Retrieval

Semantic retrieval alone can miss exact terminology, while keyword retrieval can miss semantic similarity. Combining FAISS and BM25 provides both signals.

### Structured Classification

Pydantic structured output keeps intent, sentiment, and priority within predefined categories.

### Database-backed Tools

Order and customer information is retrieved through tools instead of asking the LLM to invent database information.

### Source Citations

Retrieved knowledge-base documents are returned with the response so the source used for the answer can be inspected.

### Analytics

Analytics events are stored separately from the conversational response so system behavior can be measured and displayed in the admin dashboard.

---

# 📌 Example Capabilities

### Knowledge Base Question

```text
Customer:
How can I request a refund?

System:
Retrieves relevant return/refund information from the knowledge base
and generates a grounded response with the retrieved source.
```

### Order Lookup

```text
Customer:
Where is my order ORD1001?

System:
Uses the order lookup tool to retrieve the order status from SQLite.
```

### Follow-up Question

```text
Customer:
Where is my order ORD1001?

Assistant:
Your order is currently shipped.

Customer:
What happens if it is delayed?

System:
Uses conversation context and retrieves the relevant shipping policy.
```

### Human Escalation

```text
Customer:
This is urgent. I need human support.

System:
Analyzes the request as high priority and creates a support ticket.
```

---

# ⚠️ Limitations

This project is a **production-style prototype**, not a production customer-support platform.

Current limitations include:

* Customer and order data is simulated.
* The LLM runs locally through Ollama.
* Conversation memory is currently stored in-process.
* Conversation memory does not persist across application restarts.
* The RAG evaluation dataset is small.
* The included evaluation metrics do not represent general production accuracy.
* No production authentication or authorization system is implemented.
* No real customer-service platform integration is included.
* Analytics are intended for development and demonstration.
* Response quality depends on the knowledge base and selected LLM.
* The project has not been evaluated against a large-scale production workload.

---

# 🔮 Future Improvements

Possible extensions include:

* Persistent conversation memory
* Authentication and role-based access control
* Larger RAG evaluation datasets
* More advanced reranking
* Automated evaluation pipelines
* Human-agent workflow integration
* Production observability
* Real customer/order-system integrations
* Cloud-hosted LLM support
* Feedback-driven response evaluation
* Persistent production database
* More robust deployment architecture

---

# 🎓 What This Project Demonstrates

This project demonstrates practical implementation of:

* LLM application development
* Retrieval-Augmented Generation
* Vector databases
* Semantic search
* BM25 keyword retrieval
* Hybrid retrieval
* Embeddings
* Prompt engineering
* Structured LLM outputs
* Function/tool calling
* Conversational memory
* FastAPI backend development
* SQLAlchemy database integration
* Streamlit application development
* Analytics pipelines
* RAG evaluation
* Automated testing
* Docker containerization
* Git-based development workflow

---

# 📄 License

This project is intended for **learning, experimentation, and portfolio demonstration**.
