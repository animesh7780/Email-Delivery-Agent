# Quick Start Guide

## 🚀 Fastest Way to Get Started

### Step 1: Get Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (you'll need it in Step 3)

### Step 2: Start the Backend

Open Command Prompt in the project directory and run:
```bash
start-backend.bat
```

This script will:
- Create a virtual environment
- Install Python dependencies
- Create .env file (you'll need to add your API key)
- Initialize database with 20 sample emails
- Start the FastAPI server

### Step 3: Configure API Key

When prompted, edit the `.env` file and replace:
```
OPENAI_API_KEY=your_openai_api_key_here
```
with your actual OpenAI API key:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

Then restart the backend script.

### Step 4: Start the Frontend

Open a NEW Command Prompt window and run:
```bash
start-frontend.bat
```

This script will:
- Install Node.js dependencies
- Start React development server
- Open browser at http://localhost:3000

### Step 5: Explore the Application!

🎉 You're all set! The application should now be running.

## 🎯 What to Try First

1. **Browse Emails**: Check out the 20 pre-loaded sample emails
2. **Analyze Email**: Click any email and hit "Analyze Email" button
3. **Generate Reply**: Click "Generate Draft Reply" to see AI in action
4. **Try Chat**: Go to "AI Chat" and ask "What are my most urgent emails?"
5. **Edit Prompts**: Navigate to "Prompts" to customize AI behavior

## ⚡ Quick Commands

**Backend Only:**
```bash
cd "d:\College\Company-Assignments\OcenaAI\Email Delivery Agent"
venv\Scripts\activate
python backend\main.py
```

**Frontend Only:**
```bash
cd "d:\College\Company-Assignments\OcenaAI\Email Delivery Agent\frontend"
npm start
```

**Reset Database:**
```bash
del email_agent.db
python backend\seed_data.py
```

## 🆘 Common Issues

**"Module not found" error:**
- Make sure you activated the virtual environment
- Run: `pip install -r requirements.txt`

**"Cannot connect to API" error:**
- Ensure backend is running (should see "Uvicorn running on...")
- Check that it's on port 8000

**"Invalid API key" error:**
- Verify your OpenAI API key in `.env` file
- Make sure you have credits in your OpenAI account
- Restart the backend after updating .env

## 📹 Recording Your Demo

While recording, show these features:
1. ✅ Email inbox with categorized emails
2. ✅ Clicking and viewing email details
3. ✅ AI analyzing an email (categorization + tasks)
4. ✅ Generating a draft reply
5. ✅ Chat interface asking questions
6. ✅ Editing a prompt template

Recommended tool: OBS Studio (free) or Windows Game Bar (Win+G)

---

Need more details? Check the main README.md file!
