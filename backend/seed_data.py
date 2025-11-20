"""
Script to populate the database with sample emails and default prompts
"""
from datetime import datetime, timedelta
from database import SessionLocal, init_db, Email, Prompt
import random


def seed_sample_emails():
    """Create 20 sample emails"""
    db = SessionLocal()
    
    # Check if emails already exist
    existing_count = db.query(Email).count()
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} emails. Skipping email seeding.")
        db.close()
        return
    
    sample_emails = [
        {
            "sender": "john.manager@company.com",
            "sender_name": "John Manager",
            "recipient": "you@company.com",
            "subject": "Q4 Project Deadline - Action Required",
            "body": "Hi Team,\n\nWe need to finalize the Q4 project report by Friday, November 22nd. Please review the attached documents and submit your sections by EOD Thursday.\n\nKey deliverables:\n1. Budget analysis\n2. Performance metrics\n3. Future recommendations\n\nLet me know if you have any questions.\n\nBest regards,\nJohn"
        },
        {
            "sender": "newsletter@techcrunch.com",
            "sender_name": "TechCrunch Daily",
            "recipient": "you@company.com",
            "subject": "Today's Top Tech Stories",
            "body": "Good morning! Here are today's most important tech stories:\n\n- AI startup raises $100M in Series B\n- New smartphone release announced\n- Tech giant reports quarterly earnings\n\nRead more at techcrunch.com"
        },
        {
            "sender": "sarah.client@clientco.com",
            "sender_name": "Sarah Client",
            "recipient": "you@company.com",
            "subject": "Meeting Request - Partnership Discussion",
            "body": "Hi,\n\nI'd like to schedule a meeting next week to discuss the potential partnership between our companies. Would Tuesday or Wednesday afternoon work for you?\n\nLooking forward to hearing from you.\n\nBest,\nSarah"
        },
        {
            "sender": "noreply@promotions.com",
            "sender_name": "Super Store",
            "recipient": "you@company.com",
            "subject": "🎉 50% OFF Everything - Today Only!",
            "body": "FLASH SALE! \n\nGet 50% off ALL items in our store today only! Use code: FLASH50\n\nShop now: www.superstore.com\n\nOffer expires at midnight!"
        },
        {
            "sender": "hr@company.com",
            "sender_name": "Human Resources",
            "recipient": "you@company.com",
            "subject": "Annual Performance Review - Schedule Your Meeting",
            "body": "Dear Team Member,\n\nIt's time for annual performance reviews. Please schedule a 1-hour meeting with your manager before December 1st.\n\nPlease prepare:\n- Self-assessment document\n- Achievement highlights\n- Goals for next year\n\nThank you,\nHR Team"
        },
        {
            "sender": "mom@familymail.com",
            "sender_name": "Mom",
            "recipient": "you@company.com",
            "subject": "Thanksgiving Dinner Plans",
            "body": "Hi sweetheart,\n\nJust wanted to confirm you're coming for Thanksgiving dinner on Thursday at 3 PM. Let me know if you have any dietary restrictions or if you're bringing anyone.\n\nLove,\nMom"
        },
        {
            "sender": "security@company.com",
            "sender_name": "IT Security",
            "recipient": "you@company.com",
            "subject": "URGENT: Security Update Required",
            "body": "ATTENTION:\n\nA critical security vulnerability has been detected. You must update your system immediately.\n\nAction Required:\n1. Restart your computer\n2. Install pending updates\n3. Change your password\n\nDeadline: Today, 5 PM\n\nIT Security Team"
        },
        {
            "sender": "linkedin@notifications.com",
            "sender_name": "LinkedIn",
            "recipient": "you@company.com",
            "subject": "You have 5 new connection requests",
            "body": "Hi there,\n\nYou have 5 new connection requests on LinkedIn:\n\n- Alex Thompson (Software Engineer at Google)\n- Maria Garcia (Product Manager)\n- James Wilson (Data Scientist)\n- Emily Chen (UX Designer)\n- Robert Brown (CEO at StartupCo)\n\nView all requests on LinkedIn"
        },
        {
            "sender": "david.coworker@company.com",
            "sender_name": "David Coworker",
            "recipient": "you@company.com",
            "subject": "Team Lunch Tomorrow?",
            "body": "Hey!\n\nWant to grab lunch with the team tomorrow? We're thinking of trying that new Italian place downtown around 12:30.\n\nLet me know if you're in!\n\nDavid"
        },
        {
            "sender": "support@cloudservice.com",
            "sender_name": "Cloud Service Support",
            "recipient": "you@company.com",
            "subject": "Your Support Ticket #12345 - Resolved",
            "body": "Hello,\n\nYour support ticket #12345 regarding login issues has been resolved. The problem was caused by a temporary server outage which has now been fixed.\n\nIf you continue to experience issues, please reply to this email.\n\nBest regards,\nSupport Team"
        },
        {
            "sender": "billing@software.com",
            "sender_name": "Software Subscriptions",
            "recipient": "you@company.com",
            "subject": "Invoice #789 - Payment Due",
            "body": "Dear Customer,\n\nYour invoice #789 for $299.00 is due on November 25th, 2025.\n\nSubscription: Professional Plan (Annual)\n\nPlease ensure payment is made by the due date to avoid service interruption.\n\nView invoice: software.com/invoices/789"
        },
        {
            "sender": "events@conference.com",
            "sender_name": "Tech Conference 2025",
            "recipient": "you@company.com",
            "subject": "Reminder: Conference Registration Closing Soon",
            "body": "Hi,\n\nThis is a reminder that registration for Tech Conference 2025 closes this Friday!\n\nEarly bird discount: Save $200\nDates: January 15-17, 2026\nLocation: San Francisco, CA\n\nRegister now at techconf2025.com"
        },
        {
            "sender": "recruiter@topcompany.com",
            "sender_name": "Jane Recruiter",
            "recipient": "you@company.com",
            "subject": "Exciting Opportunity - Senior Developer Role",
            "body": "Hello,\n\nI came across your profile and think you'd be a great fit for a Senior Developer position at our company.\n\nDetails:\n- Remote-friendly\n- Competitive salary ($150K-180K)\n- Excellent benefits\n- Innovative projects\n\nWould you be interested in a quick call this week?\n\nBest,\nJane"
        },
        {
            "sender": "mike.colleague@company.com",
            "sender_name": "Mike Colleague",
            "recipient": "you@company.com",
            "subject": "Code Review Request - Feature Branch",
            "body": "Hey,\n\nCould you review my PR for the new authentication feature? It's about 200 lines of code.\n\nGitHub link: github.com/company/project/pull/456\n\nI'd appreciate feedback by tomorrow if possible.\n\nThanks!\nMike"
        },
        {
            "sender": "admin@gym.com",
            "sender_name": "Fitness Center",
            "recipient": "you@company.com",
            "subject": "Your Membership Expires Soon",
            "body": "Hi,\n\nYour gym membership expires on December 1st, 2025.\n\nRenew now and get:\n- 10% discount\n- Free personal training session\n- No enrollment fee\n\nVisit us or renew online at gym.com/renew"
        },
        {
            "sender": "professor@university.edu",
            "sender_name": "Dr. Smith",
            "recipient": "you@company.com",
            "subject": "Guest Lecture Invitation",
            "body": "Dear Alumni,\n\nWe'd like to invite you to give a guest lecture about your career in software development to our current students.\n\nProposed dates:\n- December 5th, 2 PM\n- December 12th, 3 PM\n\nThe session would be 1 hour including Q&A.\n\nPlease let me know if you're available.\n\nBest regards,\nDr. Smith"
        },
        {
            "sender": "notifications@github.com",
            "sender_name": "GitHub",
            "recipient": "you@company.com",
            "subject": "Security Alert: New SSH Key Added",
            "body": "A new SSH key was added to your GitHub account.\n\nFingerprint: SHA256:abc123...\nAdded: November 19, 2025 at 10:30 AM\n\nIf this wasn't you, please secure your account immediately.\n\nGitHub Security"
        },
        {
            "sender": "team@startup.io",
            "sender_name": "Startup Founder",
            "recipient": "you@company.com",
            "subject": "Collaboration Opportunity",
            "body": "Hi,\n\nWe're building an exciting new product and think your expertise would be valuable. Would you be interested in discussing a potential collaboration or advisory role?\n\nWe're well-funded and have an amazing team.\n\nLet's chat!\n\nFounder"
        },
        {
            "sender": "accountant@company.com",
            "sender_name": "Finance Department",
            "recipient": "you@company.com",
            "subject": "Expense Report Submission Reminder",
            "body": "Hello,\n\nThis is a reminder to submit your expense reports for October by November 22nd.\n\nMissing receipts:\n- Travel expenses\n- Client dinner on 10/15\n\nPlease upload to the expense system ASAP.\n\nThanks,\nFinance"
        },
        {
            "sender": "updates@productapp.com",
            "sender_name": "Product Updates",
            "recipient": "you@company.com",
            "subject": "New Features Released!",
            "body": "Hi there!\n\nWe've just released some exciting new features:\n\n✨ Dark mode\n✨ Advanced search\n✨ Mobile app improvements\n✨ API webhooks\n\nCheck them out in your dashboard!\n\nThe Product Team"
        }
    ]
    
    # Add emails with varying timestamps
    for i, email_data in enumerate(sample_emails):
        email = Email(
            **email_data,
            received_at=datetime.utcnow() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        )
        db.add(email)
    
    db.commit()
    print(f"✅ Added {len(sample_emails)} sample emails")
    db.close()


def seed_default_prompts():
    """Create default prompt templates"""
    db = SessionLocal()
    
    # Check if prompts already exist
    existing_count = db.query(Prompt).count()
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} prompts. Skipping prompt seeding.")
        db.close()
        return
    
    default_prompts = [
        {
            "name": "Email Categorization",
            "prompt_type": "categorization",
            "content": """Analyze the following email and categorize it into one of these categories:
- Work: Professional emails, meetings, projects
- Personal: Family, friends, personal matters
- Promotional: Marketing, sales, advertisements
- Social: Social media notifications, community updates
- Important: Urgent matters, time-sensitive information
- Spam: Unsolicited or suspicious emails
- Newsletter: Subscriptions, regular updates

Also determine:
- Priority: High (urgent/important), Medium (normal), Low (FYI)
- Sentiment: Positive, Neutral, Negative

Email Subject: {subject}
Email Body: {body}

Return as JSON with keys: category, priority, sentiment, reasoning""",
            "is_active": True
        },
        {
            "name": "Task Extraction",
            "prompt_type": "task_extraction",
            "content": """Analyze this email and extract all action items, tasks, and requests.

Email Subject: {subject}
Email Body: {body}

Identify:
1. Explicit tasks (clear requests like "Please submit by...")
2. Implicit tasks (implied actions like "Let me know...")
3. Deadlines or due dates mentioned
4. Priority indicators

Return as JSON:
{{
    "has_action_items": boolean,
    "action_items": [
        {{
            "task": "description",
            "deadline": "date or null",
            "priority": "High/Medium/Low"
        }}
    ],
    "summary": "brief overview"
}}""",
            "is_active": True
        },
        {
            "name": "Professional Auto-Reply",
            "prompt_type": "auto_reply",
            "content": """Generate a professional email reply based on the context.

Original Email Subject: {subject}
Original Email Body: {body}

Guidelines:
- Be professional and courteous
- Address all questions/requests
- Keep it concise (3-5 paragraphs max)
- Use appropriate greeting and closing
- Match the tone of the original email

Return as JSON:
{{
    "subject": "Re: [original subject]",
    "body": "full email reply text",
    "key_points": ["point 1", "point 2"]
}}""",
            "is_active": True
        }
    ]
    
    for prompt_data in default_prompts:
        prompt = Prompt(**prompt_data)
        db.add(prompt)
    
    db.commit()
    print(f"✅ Added {len(default_prompts)} default prompts")
    db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    
    print("Seeding sample emails...")
    seed_sample_emails()
    
    print("Seeding default prompts...")
    seed_default_prompts()
    
    print("\n✨ Database seeded successfully!")
