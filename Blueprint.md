# **Salary-Bot – Project Blueprint**

**Team:** 2 students
**Class:** 12 (PCM)  
**Time:** 2 weeks, 1 hour/day  
**Budget:** ₹0

***

## **1. What Are We Building?**

A chatbot for company employees to ask HR questions like:

- "How many leave days do I get?"
- "What's the payroll date?"
- "How do I request IT support?"

**Why this project:** Our dad works in a company. Employees always ask the same HR questions. A chatbot would save time.

**What makes it special:**
- Uses AI (Llama 3.2) to understand questions
- Searches HR docs automatically (RAG approach)
- No fine-tuning needed (simpler for Class 12)
- Runs on laptop (no GPU required)
- 100% free tools

***

## **2. Architecture (How It Works)**

**Flow:**
```
User (types question in UI)
    ↓
Streamlit UI
    ↓ sends to API
FastAPI Server
    ↓ calls chatbot
Chatbot Logic
    ↓ asks RAG for context
RAG System
    ↓ searches HR PDF
Chroma Vector DB + hr_policy.pdf
    ↓ returns context
Chatbot combines context + Llama 3.2
    ↓ generates answer
FastAPI returns answer → UI shows it
```

**Simple version:** User asks → UI sends → API receives → Chatbot finds HR info → AI generates answer → Answer shows back

***

## **3. Tech Stack**

| Component | Tool | Why |
|-----------|------|-----|
| **AI Model** | Llama 3.2 via Ollama | Free, open-source, runs offline |
| **AI Approach** | RAG (not fine-tuning) | Easier, no GPU needed, works well |
| **Backend** | FastAPI + Uvicorn | Fast, async, auto API docs |
| **Database** | SQLite | Built into Python, 0 setup |
| **AI Framework** | LangChain | Makes AI code 10x simpler |
| **Vector DB** | Chroma | Stores HR docs for searching |
| **Frontend** | Streamlit | Chat UI in 15 lines, no HTML |
| **PDF Reader** | PyPDFLoader | Extracts text from HR handbook |

**Total libraries:** 10 (all free, all in requirements.txt)

***

## **4. File Structure**

```
Salary-Bot/
│
├── README.md                 ← How to run (copy to GitHub)
├── requirements.txt          ← All libraries
├── .gitignore                ← Ignore database & models
│
├── data/
│   └── hr_policy.pdf         ← PUT YOUR HR HANDBOOK HERE
│
├── src/                      ← Person A (chatbot)
│   ├── rag.py                ← Finds info from HR docs
│   ├── chatbot.py            ← Main AI logic
│   ├── config.py             ← Settings
│   └── __init__.py           ← Empty, needed for imports
│
├── api/                      ← Person B (backend)
│   └── main.py               ← FastAPI server
│
└── ui/                       ← Person B (frontend)
    └── app.py                ← Streamlit chat UI
```

**Total code:** 7 Python files, ~75 lines total

***

## **5. Team Roles**

### **Person A (You) – Chatbot Side**

**Files to write:**
- `src/rag.py` (finds info from HR docs)
- `src/chatbot.py` (main AI logic)
- `src/config.py` (settings)

**Tasks:**
- Download HR PDF to `data/`
- Write RAG code (finds info from PDF)
- Write chatbot code (calls AI model)
- Test chatbot manually

**Time:** 30 min/day, 5 days total

***

### **Person B (Friend) – Backend + UI Side**

**Files to write:**
- `api/main.py` (FastAPI server)
- `ui/app.py` (Streamlit chat UI)

**Tasks:**
- Write FastAPI server (receives queries)
- Write Streamlit UI (chat interface)
- Connect UI to API
- Test full system

**Time:** 30 min/day, 4 days total

***

### **Both Together**

**Tasks:**
- Install Ollama + Python libraries (Day 1)
- Connect chatbot + API + UI (Day 7)
- Final testing (Day 10)
- Presentation prep (Day 14)

**Meetings:**
- Saturday: 30 min sync (test together)
- Sunday: 30 min review (fix bugs)

***

## **6. Week-by-Week Plan**

### **Week 1: Setup + Individual Code**

| Day | Task | Who | Time |
|-----|------|-----|------|
| **Mon** | Install Ollama: `ollama pull llama3.2` | Both | 20 min |
| **Tue** | Install libs: `pip install -r requirements.txt` | Both | 10 min |
| **Wed** | Write `src/rag.py` | Person A | 30 min |
| **Thu** | Write `src/chatbot.py` | Person A | 20 min |
| **Fri** | Write `api/main.py` | Person B | 30 min |
| **Sat** | Test individually | Both | 20 min |
| **Sun** | Fix bugs + prepare for Week 2 | Both | 30 min |

***

### **Week 2: Connect + Final Test**

| Day | Task | Who | Time |
|-----|------|-----|------|
| **Mon** | Write `ui/app.py` | Person B | 30 min |
| **Tue** | Run both: server + UI together | Both | 20 min |
| **Wed** | Add HR PDF to `data/hr_policy.pdf` | Person A | 20 min |
| **Thu** | Index PDF (re-run RAG setup) | Person A | 20 min |
| **Fri** | Test with 10 real questions | Both | 30 min |
| **Sat** | Final demo + screenshot | Both | 30 min |
| **Sun** | Submit to teacher | Both | 20 min |

***

## **7. Step-by-Step Implementation**

### **Phase 1: Setup (Day 1-2)**

**Step 1:** Install Ollama from https://ollama.com  
**Step 2:** Run `ollama pull llama3.2` in terminal  
**Step 3:** Run `pip install -r requirements.txt`  
**Step 4:** Create folders: `data`, `src`, `api`, `ui`

***

### **Phase 2: Person A Writes Chatbot (Day 3-4)**

**File 1: `src/rag.py`**

**Purpose:** Reads HR PDF → stores in Chroma → searches for relevant info when user asks question.

**What it does:**
- Loads PDF from `data/hr_policy.pdf`
- Converts text to numbers (embeddings)
- Stores in Chroma vector database
- Searches for top 3 similar docs when query comes

***

**File 2: `src/chatbot.py`**

**Purpose:** Gets user question → finds HR context → sends to Llama → returns answer.

**What it does:**
- Imports RAG function
- Initializes Llama 3.2 model
- Builds prompt with HR context + user query
- Calls AI model
- Returns just the answer

***

**File 3: `src/config.py`**

**Purpose:** Stores settings (Ollama URL).

**What it does:**
- Loads environment variables from `.env`
- Sets default Ollama URL

***

### **Phase 3: Person B Writes Backend + UI (Day 5-6)**

**File 4: `api/main.py`**

**Purpose:** Creates API endpoint `/chat` → receives query → calls chatbot → saves to SQLite → returns answer.

**What it does:**
- Initializes FastAPI server
- Creates SQLite database (chat history)
- Defines `/chat` endpoint
- Calls chatbot function
- Saves query + response to database
- Returns JSON response

***

**File 5: `ui/app.py`**

**Purpose:** Shows chat UI → user types → sends to API → displays answer.

**What it does:**
- Creates Streamlit chat window
- Stores chat history in browser
- Shows all previous messages
- Gets user input
- Calls FastAPI endpoint
- Displays assistant response

***

### **Phase 4: Connect + Test (Day 7-10)**

**Step 1:** Put HR PDF in `data/hr_policy.pdf`  
**Step 2:** Index PDF (run RAG setup once)  
**Step 3:** Start server: `uvicorn api.main:app --reload`  
**Step 4:** Start UI: `streamlit run ui/app.py`  
**Step 5:** Open `http://localhost:8501` and test

**Test questions:**
- "How many leave days?"
- "What's payroll date?"
- "How to request IT support?"

***

## **8. Library Explanations (For Presentation)**

| Library | One-Liner |
|---------|-----------|
| **FastAPI** | Makes web server so UI can talk to chatbot |
| **Uvicorn** | Runs the FastAPI server |
| **SQLite** | Saves chat history (built into Python) |
| **LangChain** | AI toolkit – makes AI code 10x shorter |
| **Ollama** | Downloads Llama 3.2, runs it locally |
| **Chroma** | Vector database – stores HR docs for searching |
| **Streamlit** | Makes chat UI in 15 lines (no HTML) |
| **PyPDFLoader** | Reads PDF files and extracts text |
| **Requests** | UI calls API to get answers |

**Bonus:** HuggingFaceEmbeddings – converts text to numbers for searching

***

## **9. Testing Checklist**

Before submitting:

| Test | Expected Result |
|------|----------------|
| Server starts | `http://localhost:8000` shows "API is running" |
| UI starts | `http://localhost:8501` shows chat window |
| Ask "leave days" | Gets answer from HR PDF |
| Ask "payroll date" | Gets answer from HR PDF |
| Ask 10 questions | All get answers |
| Restart server | Chat history saved in SQLite |
| Multiple users | No errors |

***

## **10. Future Scaling (If Company Deploys to 90K Employees)**

**Current:** SQLite (works for 5K employees, 100K chats)

**If scales to 90K:**
- Migrate SQLite → PostgreSQL (1.5 hours)
- Add database indexing (10 min)
- Deploy to cloud (AWS/GCP) (1 hour)

**We don't need to do this now.** Just build with SQLite. IT team migrates later.

| Employee Count | Database |
|----------------|----------|
| 5K | SQLite ✅ |
| 90K | PostgreSQL ✅ |
| Excel | Never (crashes) ❌ |

***

## **11. Costs**

| Thing | Cost |
|-------|------|
| Ollama | Free |
| Llama 3.2 | Free (open-source) |
| Python libraries | Free (all open-source) |
| Hosting | Free (run on laptop) |
| GPU | Not needed (CPU works) |
| **Total** | **₹0** |

***

## **12. What We'll Learn**

- How RAG works (search + AI)
- FastAPI for web servers
- SQLite for databases
- LangChain for AI
- Ollama for local models
- Streamlit for UIs
- Git for collaboration

***

## **13. Final Deliverables**

**Day 14 (Submission):**

1. Working chatbot (live demo on laptop)
2. GitHub repo (all 7 files)
3. Screenshot (chat window with 5 questions)
4. 5-minute presentation (what we built + what we learned)
5. README.md (how to run)

***

## **14. Troubleshooting**

| Problem | Solution |
|---------|----------|
| `ollama pull` fails | Check internet, retry |
| `pip install` fails | Use `python -m pip install` |
| `uvicorn` not found | Run `pip install uvicorn` |
| `streamlit` not found | Run `pip install streamlit` |
| Chatbot returns garbage | Check HR PDF is in `data/` |
| No answer from AI | Run `ollama run llama3.2` first |
| SQLite error | Delete `database.sqlite` and restart |

***

## **15. Next Steps (Start Today)**

1. Clone this blueprint to your notebook
2. Create GitHub repo: `employee-chatbot`
3. Paste blueprint as `PROJECT_BLUEPRINT.md`
4. Invite friend to repo
5. Day 1: Both install Ollama + Python libs
6. Day 2: Start coding

**Let's build this!** 🚀

***

**Made by:** [Your Name] & [Friend's Name]  
**Class 12, PCM**  
**[School Name]**
