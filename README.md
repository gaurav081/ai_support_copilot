# AI Customer Support & Knowledge Copilot

An AI-powered customer support application that combines **Retrieval-Augmented Generation (RAG), hybrid search, LLM-based classification, database-backed tools, human-support escalation, and analytics**.

The application allows customers to ask questions about support policies, retrieve order information, and request human assistance. An administrative dashboard provides visibility into request volume, response times, priorities, and escalations.

**Project status:** Deployed portfolio prototype

## 🔗 Live Demo

| Component | Link |
|---|---|
| Customer Support UI | [Open AI Support Copilot](https://ai-support-copilot-frontend-xehg.onrender.com/) |
| FastAPI Backend | [Open API](https://ai-support-copilot-3ef6.onrender.com/) |
| Interactive API Documentation | [Explore Swagger UI](https://ai-support-copilot-3ef6.onrender.com/docs) |
| GitHub Repository | [View Source Code](https://github.com/gaurav081/ai_support_copilot) |

*Note: The application is a portfolio prototype. The sample customer/order data and support policies are intended for demonstration, not real customer-service operations.*

---

## 🚀 Features

### 1. Retrieval-Augmented Generation (RAG)

- HTML knowledge-base ingestion
- Text cleaning and paragraph-aware chunking
- Sentence-transformer embeddings for semantic retrieval
- FAISS vector search
- BM25 keyword-based retrieval
- Hybrid retrieval and ranking
- Source information accompanying generated answers
- Retrieval evaluation using Hit@3 and Mean Reciprocal Rank (MRR)

### 2. Customer Support Intelligence

- Intent classification
- Sentiment analysis
- Priority classification
- Structured outputs validated with Pydantic
- Context-aware follow-up questions
- Conversation history maintained in application memory

Supported intent categories include:

- `return_request`
- `refund_request`
- `shipping_question`
- `order_status`
- `exchange_request`
- `cancellation_request`
- `general_question`
- `other`

Sentiment categories:

- `positive`
- `neutral`
- `negative`

Priority categories:

- `low`
- `medium`
- `high`

### 3. Database-Backed Tools

The application provides tools for:

- Customer lookup
- Order-status lookup
- Support-ticket creation
- Database-backed information retrieval
- LLM tool calling

The LLM can use these tools to retrieve information instead of relying on generated answers for database-specific questions.

### 4. Human-Support Escalation

The escalation workflow identifies requests requiring human assistance.

- High-priority requests can trigger escalation.
- Explicit human-support requests can trigger escalation even when the classifier returns medium or low priority.
- Support tickets are stored in the database.
- The assistant returns the created ticket ID when escalation succeeds.

### 5. Analytics Dashboard

The Streamlit admin dashboard displays metrics such as:

- Total requests
- Average response time
- Escalated requests
- Escalation rate
- Intent distribution
- Priority distribution

The dashboard obtains its metrics from the FastAPI backend.

### 6. Backend and Deployment

- FastAPI REST API
- SQLite database
- SQLAlchemy ORM
- Streamlit frontend
- Environment-based configuration
- Docker support for the backend
- Render deployment with separate frontend and backend services

---

## 🏗️ Architecture

```text
                     Customer / Admin
                            |
                            v
                +------------------------+
                |     Streamlit UI       |
                |                        |
                | Customer Support Chat  |
                | Admin Analytics        |
                +-----------+------------+
                            |
                    HTTP Requests
                            |
                            v
                +------------------------+
                |      FastAPI API       |
                |                        |
                | POST /chat             |
                | GET  /analytics        |
                | GET  /analytics/metrics|
                +-----------+------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
       +------------+ +------------+ +------------+
       | Classifier | | RAG System | | Tool System |
       |            | |            | |            |
       | Intent     | | FAISS      | | Customers  |
       | Sentiment  | | BM25       | | Orders     |
       | Priority   | | Hybrid     | | Tickets    |
       +------------+ +------+-----+ +------+-----+
                             |                |
                             v                v
                    +----------------+ +-------------+
                    | HTML Knowledge | |   SQLite    |
                    | Base           | |  Database   |
                    +----------------+ +-------------+
                             |
                             v
                    +----------------+
                    | LLM Provider   |
                    | Gemini/Ollama* |
                    +----------------+
```

\*The available LLM provider depends on the application configuration and the environment in which it is running.

### Request Flow

1. The customer submits a message through the Streamlit interface.
2. The frontend sends the request to FastAPI.
3. The backend analyzes the message for intent, sentiment, and priority.
4. The application determines whether to retrieve knowledge, invoke a database-backed tool, or escalate the request.
5. The RAG pipeline retrieves relevant knowledge when needed.
6. The LLM generates a response using the available context.
7. If escalation is required, the application creates a support ticket.
8. The backend returns the response and relevant metadata to the frontend.
9. Request analytics are recorded for the dashboard.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Frontend | Streamlit |
| LLM | Ollama / Google Gemini, depending on configuration |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| Keyword Search | BM25 |
| RAG | Custom retrieval pipeline |
| Data Validation | Pydantic |
| Database | SQLite |
| ORM | SQLAlchemy |
| HTTP Client | Requests |
| Testing | Pytest |
| Containerization | Docker |
| Deployment | Render |
| Version Control | Git and GitHub |

---

## 📁 Project Structure

```text
ai_support_copilot/
│
├── app/
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
│   └── vector_store/
│
├── streamlit_app.py
├── build_index.py
├── create_database.py
├── seed_database.py
├── evaluation_dataset.py
├── evaluate_rag.py
│
├── test_*.py
├── requirements.txt
├── requirements-render.txt
├── requirements-frontend.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

*The tree summarizes the main components; individual test files and other project files are abbreviated.*

---

## ⚙️ Local Setup

### Prerequisites

Install the following:

- Python 3.13
- Git
- Ollama, if using a local Ollama model
- A Google Gemini API key, if using the Gemini provider

### 1. Clone the repository

```bash
git clone https://github.com/gaurav081/ai_support_copilot.git
cd ai_support_copilot
```

### 2. Create and activate a virtual environment

On Linux or WSL:

```bash
python3.13 -m venv myenv
source myenv/bin/activate
```

On Windows PowerShell:

```powershell
py -3.13 -m venv myenv
.\myenv\Scripts\Activate.ps1
```

### 3. Install dependencies

For local development:

```bash
pip install -r requirements.txt
```

The project also contains separate dependency files for the deployed backend and frontend.

- `requirements-render.txt` — backend deployment dependencies
- `requirements-frontend.txt` — Streamlit frontend dependencies

### 4. Configure the LLM

Configure the provider and model through the application's settings and environment variables.

For Ollama, install and start Ollama, then pull a model:

```bash
ollama pull llama3.2
ollama list
```

Ensure the model name matches the application configuration.

For Gemini, configure a valid `GEMINI_API_KEY` and select the Gemini provider through the application's configuration.

**Security:** Keep API keys in environment variables or a local `.env` file that is excluded from Git. Never commit credentials.

### 5. Prepare the database

Create the database:

```bash
python create_database.py
```

Seed demonstration data:

```bash
python seed_database.py
```

The application may also create missing tables during startup, depending on its database initialization logic.

### 6. Build the knowledge-base index

```bash
python build_index.py
```

The source documents are stored in:

```text
data/documents/
```

The ingestion process cleans the HTML content, splits it into chunks, generates embeddings, and builds the retrieval index.

### 7. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

The local backend is available at:

- API: `http://127.0.0.1:8000`
- Interactive documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

### 8. Start the Streamlit frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run streamlit_app.py
```

By default, the frontend connects to the local API. The backend URL can be configured with the `BACKEND_URL` environment variable.

For example, in Linux or WSL:

```bash
export BACKEND_URL=http://127.0.0.1:8000
streamlit run streamlit_app.py
```

---

## 🌐 API Reference

### `GET /health`

Checks the backend health endpoint.

### `POST /chat`

Processes a customer message.

Example request:

```json
{
  "conversation_id": "demo-conversation",
  "prompt": "How can I request a refund?"
}
```

Example response structure:

```json
{
  "prompt": "How can I request a refund?",
  "response": "Refund instructions based on the available policy...",
  "analysis": {
    "intent": "refund_request",
    "sentiment": "neutral",
    "priority": "medium"
  },
  "sources": []
}
```

The response's source list depends on the retrieved documents. The response above illustrates the structure; it is not a guaranteed live API response.

### `GET /analytics`

Returns analytics information from the backend.

### `GET /analytics/metrics`

Returns aggregate metrics for the admin dashboard.

For the authoritative request and response schemas, use the live [FastAPI Swagger documentation](https://ai-support-copilot-3ef6.onrender.com/docs).

---

## 🔎 Hybrid Retrieval

The project combines semantic search and keyword search to improve knowledge retrieval.

### Semantic Search

FAISS searches vector representations of document chunks generated using sentence-transformer embeddings.

It helps retrieve passages that are semantically related to the customer's question, even when the wording differs.

### Keyword Search

BM25 ranks passages using keyword relevance.

It can be particularly useful for exact terms, policy names, and specific phrases.

### Hybrid Ranking

```text
             Customer Query
                   |
          +--------+--------+
          |                 |
          v                 v
     Semantic Search    BM25 Search
          |                 |
          v                 v
         FAISS          Keyword Ranker
          |                 |
          +--------+--------+
                   |
                   v
             Hybrid Ranking
                   |
                   v
          Relevant Documents
                   |
                   v
             LLM Response
```

Combining these retrieval methods helps balance semantic relevance with exact keyword matching.

### Deployment Consideration

The deployed backend is configured to use keyword retrieval through `RETRIEVAL_MODE=keyword` to reduce resource requirements in the hosting environment. The local development setup supports the broader hybrid retrieval workflow when its dependencies and configuration are available.

---

## 🧠 Conversation Memory

The application maintains conversation history to support follow-up questions.

Example:

```text
Customer: Where is my order ORD1001?

Assistant: Your order is currently shipped.

Customer: What happens if it is delayed?

Assistant: Uses the conversation context to interpret
the follow-up and retrieve relevant shipping information.
```

The current memory implementation is in-process memory. Conversation history may be lost when the backend restarts and is not a persistent cross-session memory store.

---

## 🔧 Database Tools and Escalation

### Order Lookup

The order tool retrieves order information from the database rather than asking the LLM to invent order details.

Example:

```text
Customer: Where is my order ORD1001?
```

### Customer Lookup

The customer tool retrieves customer information using the supported lookup fields.

### Support Ticket Creation

When escalation is required, the application creates a support ticket and returns its identifier to the customer.

Direct requests for human support can trigger escalation even when the classifier assigns a priority below `high`.

Example:

```text
Customer: I require human assistance.

System:
1. Analyzes the message.
2. Checks whether escalation is required.
3. Creates a support ticket.
4. Returns the ticket ID when ticket creation succeeds.
```

Escalation decision logic and successful ticket creation are separate concerns: the ticket tool and its database operation must also succeed.

---

## 📊 Analytics

The backend records information about customer requests so that aggregate metrics can be displayed in the admin interface.

Metrics include:

- Total requests
- Average response time
- Intent distribution
- Priority distribution
- Escalated requests
- Escalation rate

These metrics are intended for demonstration and development. They should not be interpreted as production-grade observability or business reporting.

---

## 🧪 Testing

Run the test suite from the project root:

```bash
pytest -q
```

The tests cover project components such as retrieval, classification, database tools, and escalation.

The latest full local test run during development completed with:

```text
8 passed, 1 warning
```

The warning concerned deprecated use of `datetime.datetime.utcnow()` in a SQLAlchemy-related code path. It did not cause the test run to fail.

Test results may change as the project evolves. Run the tests against the current checkout before relying on the result.

### RAG Evaluation

Run:

```bash
python evaluate_rag.py
```

The evaluation dataset includes questions related to refunds, shipping, returns, and delayed orders.

The project measures:

- **Hit@3:** Whether a relevant document appears among the top three retrieved results.
- **MRR (Mean Reciprocal Rank):** How highly the first relevant result is ranked.

Earlier development runs achieved Hit@3 of `1.00` and MRR of `1.00` on the small included dataset. These results are specific to that dataset and do not demonstrate general production accuracy.

---

## 🐳 Docker

Build the backend image:

```bash
docker build -t ai-support-copilot .
```

Run it:

```bash
docker run --rm -p 8000:8000 \
  -e MODEL_NAME=llama3.2 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  ai-support-copilot
```

This example assumes the image's dependencies and application configuration support the specified Ollama settings. Ollama runs outside the container and must be reachable at the configured address.

The container's ability to reach the host differs by operating system and Docker configuration. Verify connectivity in your environment.

---

## ☁️ Deployment on Render

The application uses separate services for the Streamlit frontend and FastAPI backend.

### Backend Service

The backend uses the repository's backend deployment requirements.

Typical configuration:

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build command | `pip install -r requirements-render.txt` |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Required environment variables depend on the configured LLM provider. The deployed backend also uses:

```text
RETRIEVAL_MODE=keyword
```

Keep all required provider credentials and configuration in the backend service's own environment settings.

### Frontend Service

The frontend uses its separate requirements file.

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build command | `pip install -r requirements-frontend.txt` |
| Start command | `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0` |

Configure the frontend's environment variable:

```text
BACKEND_URL=https://ai-support-copilot-3ef6.onrender.com
```

This allows the Streamlit application to communicate with the deployed FastAPI service.

The two services are independently deployed. Updating backend code requires a backend deployment, while frontend-only changes can be deployed through the frontend service.

---

## 🧩 Key Design Decisions

### Hybrid Retrieval

Semantic and keyword search have different strengths. Combining them provides a practical retrieval strategy for policy questions.

### Structured Classification

Pydantic restricts the classifier's output to predefined intent, sentiment, and priority categories.

### Database-Backed Tools

Customer and order information is retrieved through application tools rather than relying on the LLM's generated knowledge.

### Local LLM Development

Ollama supports local experimentation without requiring every development request to use a hosted LLM.

### Separate Frontend and Backend

The Streamlit UI and FastAPI backend are deployed independently, making their responsibilities and configuration easier to manage.

### Resource-Aware Deployment

The deployed backend uses keyword retrieval to reduce dependency and memory requirements compared with loading the complete local embedding pipeline.

---

## ⚠️ Limitations

This is a production-style portfolio prototype, not a production-ready customer-support platform.

Current limitations include:

- Demonstration customer and order data
- In-process conversation memory
- No production authentication or role-based authorization
- No integration with a real customer-service platform
- Limited RAG evaluation data
- No demonstrated large-scale load testing
- Response quality depends on the LLM and available knowledge base
- Analytics are intended for demonstration rather than production monitoring
- The deployed keyword retrieval configuration differs from the local hybrid retrieval configuration
- Persistent production-grade storage, observability, and operational controls remain future improvements

Do not use the prototype to process real customer data without implementing appropriate security, privacy, access control, reliability, and operational safeguards.

---

## 🔮 Future Improvements

Potential enhancements include:

- Persistent conversation memory
- Authentication and role-based access control
- More extensive RAG evaluation datasets
- Advanced reranking
- Automated evaluation pipelines
- Human-agent workflow integration
- Persistent production database
- Real order and customer-system integrations
- Improved monitoring and observability
- Feedback-driven response evaluation
- Load and reliability testing
- More robust production deployment architecture

---

## 🎓 What This Project Demonstrates

This project brings together several practical AI engineering and backend development concepts:

- Retrieval-Augmented Generation
- Embeddings and vector search
- BM25 and hybrid retrieval
- Prompt engineering
- Structured LLM outputs
- Function and tool calling
- Conversation memory
- FastAPI REST API development
- SQLAlchemy and database integration
- Streamlit UI development
- Analytics pipelines
- RAG evaluation
- Automated testing
- Docker
- Git and GitHub
- Cloud deployment and environment configuration


---

**Built as a learning and portfolio project to explore practical LLM application development, RAG systems, backend integration, testing, and deployment.**
