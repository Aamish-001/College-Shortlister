# Employee Salary Chatbot with RAG – Project Framework

## 1. Project Overview

**Goal**  
Build an internal chatbot for company employees to ask **salary-related queries**, grounded in the company’s official policies and employee data. The chatbot should:

- Answer questions about salary calculation, deductions, bonuses, leaves impact, etc.
- Use **RAG** so answers are based on the real company documents, not just generic model knowledge.[web:17][web:32][web:44]
- Support **voice input** (speech-to-text).
- Show **Frequently Asked Questions (FAQ)** as a quick-access box.
- Require **authentication** (likely Firebase: Google / phone login).
- Run as a **Streamlit web app** initially, with **possible future Telegram bot**.

**Tech Summary**

- Language: **Python**
- UI: **Streamlit**
- Auth: **Firebase Authentication**
- LLM: **Ollama** (local LLM, free) or a free/cheap API
- RAG: **Embeddings + Chroma (vector DB)**[web:27][web:39][web:43]
- Storage: **SQLite** for logs / metadata
- Optional: **Telegram bot** later

---

## 2. High-Level Architecture

### 2.1 User Flow

1. Employee opens Streamlit app.
2. Logs in via Firebase Auth (Google or phone).
3. On the main screen:
   - Can pick a **FAQ question** from a dropdown, or
   - Use **speech-to-text** to ask a question, or
   - Type a question manually.
4. The app:
   - Sends the question to the **RAG pipeline**.
5. RAG pipeline:
   - Retrieves **relevant policy chunks** and, if needed, **employee-specific data** from company datasets.[web:17][web:32][web:44]
   - Augments the prompt with this context and sends it to the LLM (Ollama or other).
6. LLM generates a **grounded answer**, which Streamlit displays.
7. The app logs the interaction (user, question, answer, timestamp) in **SQLite** for analytics / debugging.

### 2.2 RAG Flow (Conceptual)

Following standard RAG architecture:[web:17][web:41][web:44]

1. **User query** comes in.
2. The query is converted to an **embedding** and sent to a **vector database** (Chroma) that contains embeddings of company policies, salary rules, terms, etc.[web:27][web:39][web:43]
3. Chroma performs a **similarity search** to find the most relevant document chunks.[web:27][web:39]
4. The application **augments the LLM prompt** with:
   - Retrieved policy text.
   - Optional employee-specific numeric data.
5. The LLM generates an answer using this augmented context.[web:17][web:32][web:44]
6. The app returns the answer to the user.

---

## 3. Tools and Libraries – Detailed

### 3.1 Core Frameworks

- **Python**
  - Main programming language.
  - Used for Streamlit, RAG pipeline, LLM integration, Firebase backend calls, SQLite, and Telegram bot.

- **Streamlit**
  - Python library for building web apps with minimal code.
  - In this project:
    - Renders the login UI.
    - Provides the chat interface (chat history, input box).
    - Shows FAQ dropdown.
    - Offers upload/record interface for speech input.

### 3.2 Authentication & User Management

- **Firebase Authentication**[web:30]
  - Cloud service for user sign-in (Google, phone, etc.).
  - You’ll use:
    - Google sign-in.
    - Phone number with OTP.
  - In Streamlit:
    - Use a component like `streamlit-firebase-auth` to show a login widget and capture user identity.[web:30]
  - After login, you get:
    - `user_id` (UID), email, display name, etc.
  - You can restrict access to company emails (e.g., `@company.com`).

- **Firebase Admin SDK (optional, backend)**
  - Used from Python to verify ID tokens (if you implement a stricter separation between frontend and backend).

### 3.3 LLM Backend

- **Ollama**[web:28][web:34][web:40][web:43]
  - Local tool that runs open-source LLMs (like Llama, Mistral) and exposes them via a simple HTTP API.
  - Why use it:
    - Free and runs entirely on your machine.
    - No API key or internet required.
    - Suitable for a student project and small internal tool.
  - It fits well with local RAG setups using a vector database.[web:40][web:42][web:43]

- **Alternative: Hosted API (e.g., Grok / other OpenAI-compatible)**
  - You may explore free tiers:
    - Grok APIs usually have limited free credits and then pay-as-you-go.[web:29][web:35]
  - For simplicity and cost control, Ollama is more predictable.

- **HTTP Client: `requests`**
  - Used to send JSON requests to Ollama or any other API and read JSON responses.

### 3.4 RAG Components

- **PyPDF / pdf loaders**
  - To extract text from PDF policy documents (salary policy, HR handbook, terms).
  - Often used together with LangChain document loaders or vanilla `pypdf`/`PyPDF2`.

- **Embedding Model**
  - You need to convert text chunks (policy paragraphs) and user queries into vector representations (embeddings).[web:17][web:39][web:43]
  - Common choices:
    - `sentence-transformers` models via `langchain-huggingface`, or
    - Any embedding API you choose.
  - These embeddings are then stored and searched within Chroma.

- **Chroma (ChromaDB)**[web:27][web:33][web:39][web:43]
  - An open-source vector database for storing and searching embeddings.
  - In your project:
    - Stores embeddings of salary policies, HR rules, terms, etc.
    - At query time, finds the most relevant text chunks for a user’s question.
  - Good for local, embedded RAG use cases (does not require a separate server).[web:27][web:33]

- **RAG Orchestration (plain Python or LangChain)**
  - You can build the RAG pipeline manually in Python or use **LangChain**:
    - Load documents.
    - Chunk text into smaller pieces.
    - Embed and store in Chroma.
    - On query, retrieve top‑k chunks and build the final prompt.
  - LangChain is very common for RAG apps and integrates well with both Ollama and Chroma.[web:36][web:40][web:42][web:43]

### 3.5 Speech to Text

- **SpeechRecognition**[web:31]
  - Python library that provides a unified API over multiple STT engines.
  - You can:
    - Accept audio uploaded from the Streamlit frontend.
    - Use `SpeechRecognition` to convert it to text using e.g. Google Web Speech API or another backend.
  - Good enough for a student project; not perfect but practical.

- **Audio Handling**
  - Either:
    - Use a Streamlit audio recorder component (community).
    - Or allow users to upload a short `.wav`/`.mp3` file.

### 3.6 Storage / Logging

- **SQLite**
  - Built-in Python module `sqlite3`.
  - In this project:
    - Store chat logs (user, query, answer, timestamp).
    - Optionally store metadata like which policy document chunk was used.
  - SQLite is file-based and suitable for small/medium workloads and local demos.[web:19][web:23]

### 3.7 Optional: Telegram Bot (Future)

- **python-telegram-bot** or **aiogram**
  - Libraries to build Telegram bots.
  - Later, you can route Telegram messages to the same RAG pipeline function you use in Streamlit.

---

## 4. Data from Company – How It Fits Into RAG

**Company-provided data:**

1. **Documents:**
   - Salary policies.
   - Leave rules.
   - Bonus and appraisal guidelines.
   - Terms and conditions.
   - Any salary-related HR documents.

   → These go into the **RAG document store**:
   - Extract text.
   - Chunk into smaller segments.
   - Embed and store in Chroma.

2. **Employee data:**
   - Employee ID, name, role, department.
   - Salary bands, grade.
   - Entry/exit logs (if relevant).
   - Maybe payroll history (if allowed).

   → For privacy and scope, v1 could:
   - Ignore personalized “my salary” queries and only answer **generic policy** questions.
   - Or, if you include personalized answers:
     - Keep structured employee data in a secure DB (SQLite, or company DB via API).
     - Only access the record for the authenticated user.
   - Employee tables are **structured** and belong in SQLite or a proper company DB, not in the vector store.

---

## 5. Phase-by-Phase Framework

### Phase 1 – Requirements & Scope

- Define what the bot will and will not do in v1:
  - **Will do:**
    - Answer generic salary policy questions.
    - Read and explain policy rules.
    - Show FAQ list.
    - Accept voice or text input.
  - **Won’t do (or optional):**
    - Show exact personal salary numbers (unless access is clearly defined).
    - Perform complex HR actions (e.g., apply for leave).

- Decide:
  - Initial focus: generic policy Q&A → easier + safe.
  - Personalized features can be “future work.”

---

### Phase 2 – Environment Setup

1. Install Python and create a virtual environment.
2. Install core libraries:
   - `streamlit`
   - `requests`
   - `langchain`, `langchain-community`, `langchain-chroma`, `langchain-huggingface` (if using LangChain)
   - `chromadb`
   - `SpeechRecognition`
   - `python-dotenv`
   - `sqlite3` (builtin)
3. Install **Ollama** and pull an LLM (e.g., `ollama pull mistral` or `ollama pull llama3`).[web:40][web:42][web:43]
4. Create a Firebase project and configure authentication.

---

### Phase 3 – RAG Data Ingestion

1. **Collect documents:**
   - All salary-related policies as PDFs, DOCX, or text.
2. **Document loading:**
   - Use a PDF loader to extract text.
3. **Chunking:**
   - Split large text into smaller chunks (e.g., 500–1000 characters) to keep each piece manageable.[web:36][web:39][web:43]
4. **Embedding:**
   - Use an embedding model to convert each chunk to a vector.[web:17][web:39][web:43]
5. **Store in Chroma:**
   - Create a Chroma collection and store:
     - Chunk text.
     - Embedding vector.
     - Metadata (document name, section, page, etc.).[web:27][web:39][web:43]

This is the one-time **ingestion pipeline**.  
You re-run it when policies change.

---

### Phase 4 – RAG Query Pipeline

When a user asks a question (text or from STT):

1. **Preprocess question:**
   - Clean up text (strip, normalize).
2. **Embed question:**
   - Convert user query to an embedding using the same embedding model used during ingestion.[web:17][web:39][web:43]
3. **Retrieve from Chroma:**
   - Query Chroma for top‑k similar chunks (e.g., top 3–5).[web:27][web:39][web:43]
4. **Build prompt:**
   - System message:
     - “You are a salary assistant for Company X. Use only the provided context from company policies to answer. If it is not covered, say you don’t know.”
   - Context: concatenation of retrieved chunks.
   - User message: the actual question.
5. **Call LLM (Ollama):**
   - Send messages via HTTP.
6. **Return answer:**
   - Show nicely formatted answer in Streamlit.
   - Optionally, show “sources” (which policy sections were used).

This follows the standard RAG pattern: **retrieve → augment prompt → generate.**[web:17][web:41][web:44]

---

### Phase 5 – Streamlit UI & FAQ

1. **Layout:**
   - Sidebar:
     - Firebase login / user info.
     - FAQ dropdown.
   - Main area:
     - Chat history.
     - Input box (text).
     - Button for “Use microphone” / audio upload.

2. **FAQ box:**
   - A list of common salary questions.
   - When a FAQ is selected:
     - Option 1: Show a prepared answer directly.
     - Option 2: Treat it like a user query and send it through the RAG pipeline (good for consistency).

3. **Chat display:**
   - Show messages from both user and bot in a chat-like format.

---

### Phase 6 – Speech-to-Text Integration

1. In UI:
   - Add a control to record or upload an audio file.
2. Backend:
   - Use `SpeechRecognition` to convert audio to text.[web:31]
3. Once text is obtained:
   - Treat it exactly like typed input:
     - Send it into the RAG query pipeline.
   - Show the recognized text so the user can verify.

---

### Phase 7 – Firebase Authentication Integration

1. Configure Firebase to accept:
   - Google login.
   - Phone number login.
2. In Streamlit:
   - Integrate a Firebase auth component or custom JS-based auth.
   - After login:
     - Store user info (name, email, uid) in session state.
3. Pass `user_id` to the backend:
   - So the RAG/LLM pipeline can log who asked what.
   - So you can implement future personalization (if allowed).

---

### Phase 8 – SQLite Logging and Analytics

1. Define tables, e.g. `chats`:
   - `id`, `user_id`, `question`, `answer`, `timestamp`, maybe `retrieved_docs`.
2. After each answer:
   - Insert a log row.
3. Use logs to:
   - See popular questions.
   - Debug bad answers.
   - Prepare a small analytics page (top 10 questions, etc.) if you have time.

---

### Phase 9 – Testing and Evaluation

1. Test with:
   - Simple questions that exactly match policy wording.
   - Paraphrased questions (“How is my salary decided?”, “How do you calculate our CTC?”).
2. Verify:
   - The retrieved policy chunks actually match the question.
   - The LLM answers according to the policy and doesn’t hallucinate.
3. Iterate:
   - Adjust chunk size.
   - Tune number of retrieved chunks.
   - Improve system prompt instructions.

---

### Phase 10 – Future Extensions

- **Telegram Bot**
  - Add a Telegram interface that sends messages into the same RAG pipeline.
- **Personalized Answers**
  - For authenticated employees, answer questions like “How much was my last salary?” by:
    - Retrieving from employee data (SQLite or company DB).
    - Combining that with general policy context in the prompt.
- **Better STT**
  - Use Whisper or another advanced STT engine.
- **Production-ready DB**
  - If scaling beyond small internal use, move from SQLite to a more robust DB (PostgreSQL), and from local Chroma to a managed vector DB.

---

## 6. Summary

This framework gives you:

- A **RAG-based chatbot** so the model actually uses the company’s long salary policies and terms, not just generic knowledge.[web:17][web:36][web:40][web:42][web:43]
- A clear separation of concerns:
  - Streamlit UI
  - Firebase auth
  - RAG pipeline (embeddings + Chroma + LLM)
  - Speech-to-text
  - SQLite logging
- A realistic roadmap you and your friend can implement step by step, starting with:
  1. Basic Streamlit + RAG Q&A (no auth, no STT).
  2. Then add Firebase auth.
  3. Then add STT.
  4. Then refine UX and possibly Telegram.

You can paste this file as `PROJECT_FRAMEWORK.md` in your GitHub repo and build from there.
