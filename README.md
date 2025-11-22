# Email Productivity Agent

An intelligent, prompt-driven Email Productivity Agent that automates email management using Large Language Models (LLMs). This system categorizes emails, extracts action items, generates draft replies, and provides an interactive chat interface for inbox management.

## Features

- **AI-Powered Email Categorization**: Automatically categorizes emails (Work, Personal, Promotional, Important, etc.)
- **Smart Action Item Extraction**: Identifies tasks, deadlines, and priorities from email content
- **Auto-Draft Generation**: Creates professional email replies with customizable tone
- **Chat Interface**: Natural language interaction with your inbox
- **Prompt Configuration**: Fully customizable prompt templates for all AI operations
- **Real-time Statistics**: Dashboard showing inbox metrics and insights
- **Mock Data**: 20 pre-loaded sample emails for immediate testing

## Architecture

### Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- Google Gemini via `google-generativeai` (LLM integration)
- Pydantic (Data validation)

**Frontend:**
- React.js
- Axios (API communication)
- CSS3 (Styling)

**AI/LLM:**
- Google Gemini (via `google-generativeai`)
- Custom prompt templates
- JSON-structured responses

## 📁 Project Structure

```
Email Delivery Agent/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & endpoints
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database models & setup
│   ├── models.py            # Pydantic schemas
│   ├── llm_service.py       # OpenAI integration
│   └── seed_data.py         # Sample data generator
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── EmailList.js
│   │   │   ├── EmailDetail.js
│   │   │   ├── PromptEditor.js
│   │   │   └── ChatInterface.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── api.js
│   │   └── index.js
│   └── package.json
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Backend Setup (Gemini)

1. **Clone the repository**
   ```bash
   cd "d:\College\Company-Assignments\OcenaAI\Email Delivery Agent"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key and chosen model:
   ```dotenv
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   DATABASE_URL=sqlite:///./email_agent.db
   HOST=0.0.0.0
   PORT=8000
   ```

5. **Start the backend server (recommended)**

   A convenience script `start-backend.bat` will initialize the database **only if** the `email_agent.db` file is missing (prevents duplicate seeding) and then start the server:
   ```bash
   start-backend.bat
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

6. **Seed / Cleanup (optional)**

   - If you need to re-seed from scratch, delete the DB then start the backend:
     ```bash
     del email_agent.db
     start-backend.bat
     ```

   - To remove duplicates (keeps other records), run the cleanup script:
     ```bash
     cd backend
     python cleanup_duplicates.py
     ```

### Frontend Setup

1. **Open a new terminal and navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   
   The application will open at `http://localhost:3000`

## Sample Data

The system includes 20 pre-loaded sample emails covering various scenarios:

- Work-related emails (project deadlines, meetings, code reviews)
- Personal emails (family, friends)
- Important notifications (security alerts, HR communications)
- Promotional emails (marketing, offers)
- Social notifications (LinkedIn, GitHub)
- Newsletters (tech news, updates)

## Default Prompt Templates

### 1. Email Categorization
Analyzes email content and assigns:
- **Category**: Work, Personal, Promotional, Social, Important, Spam, Newsletter
- **Priority**: High, Medium, Low
- **Sentiment**: Positive, Neutral, Negative

### 2. Task Extraction
Identifies:
- Explicit and implicit action items
- Deadlines and due dates
- Priority levels for each task

### 3. Auto-Reply Generation
Creates professional email responses with:
- Appropriate subject line
- Well-structured body
- Key points addressed

## Usage Guide

### Managing Emails

1. **View Inbox**: Browse all emails in the main view
2. **Filter by Category**: Use sidebar to filter by Work, Personal, Important, etc.
3. **Read Email**: Click any email to view full details
4. **Process Email**: Click "Analyze Email" to categorize and extract tasks
5. **Generate Reply**: Click "Generate Draft Reply" to create an AI-powered response

### Chat with AI Assistant

1. Navigate to "AI Chat" in the sidebar
2. Ask questions like:
   - "What are my urgent tasks?"
   - "Summarize unread emails"
   - "Which emails need replies?"
   - "Show me work-related action items"

### Customizing Prompts

1. Go to "Prompts" in the sidebar
2. View existing prompt templates
3. Click "Edit" to modify a prompt
4. Click "Create New Prompt" to add custom templates
5. Toggle "Active" to enable/disable prompts

## API Endpoints

### Emails
- `GET /api/emails` - List all emails (with optional category filter)
- `GET /api/emails/{id}` - Get specific email
- `POST /api/emails` - Create new email
- `PUT /api/emails/{id}/read` - Mark email as read
- `POST /api/emails/{id}/process` - Process email with AI

### Prompts
- `GET /api/prompts` - List all prompts
- `GET /api/prompts/{id}` - Get specific prompt
- `POST /api/prompts` - Create new prompt
- `PUT /api/prompts/{id}` - Update prompt
- `DELETE /api/prompts/{id}` - Delete prompt

### Drafts
- `GET /api/drafts` - List all drafts (with optional email filter)
- `GET /api/drafts/{id}` - Get specific draft

### Chat & Stats
- `POST /api/chat` - Send message to AI assistant
- `GET /api/stats` - Get inbox statistics

## Development

### Adding More Sample Emails

Edit `backend/seed_data.py` and add entries to the `sample_emails` list, for example:

```python
{
   "sender": "user@example.com",
   "sender_name": "John Doe",
   "recipient": "you@company.com",
   "subject": "Your Subject",
   "body": "Email content here..."
}
```

Because the project now seeds only when the DB file is absent, to re-seed you must delete the DB and re-run the backend (see seeding section).

### Customizing AI Behavior

Modify prompt templates in the UI or directly in the database to change:
- Categorization logic
- Task extraction patterns
- Reply generation style

Note: The backend LLM integration uses Google Gemini via the `google-generativeai` package. You can switch `GEMINI_MODEL` in your `.env` to a different supported model.

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- The `.env.example` is provided as a template
- Keep your OpenAI API key secure
- This is a development/demo application - add authentication for production use

## Key Implementation Details

### Prompt-Driven Architecture

All AI operations are driven by customizable prompts stored in the database:

1. **User defines prompts** via the UI
2. **System retrieves active prompts** when processing emails
3. **LLM receives prompt + email content** and returns structured responses
4. **Results are stored** and displayed to the user

### Email Processing Flow

```
Email Received → User Triggers Processing → System Retrieves Prompt Template
→ LLM Analyzes Email → Structured Response → Database Update → UI Display
```