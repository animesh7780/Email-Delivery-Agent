"""
Script to remove duplicate emails from the database
"""
from database import SessionLocal, Email, Prompt, Draft

def cleanup_duplicates():
    db = SessionLocal()
    
    # Get all emails
    emails = db.query(Email).all()
    print(f"Total emails before cleanup: {len(emails)}")
    
    # Track unique emails by subject + sender + body
    seen = set()
    duplicates = []
    
    for email in emails:
        key = (email.subject, email.sender, email.body)
        if key in seen:
            duplicates.append(email)
        else:
            seen.add(key)
    
    # Delete duplicates
    for email in duplicates:
        db.delete(email)
    
    db.commit()
    print(f"Removed {len(duplicates)} duplicate emails")
    print(f"Total emails after cleanup: {len(emails) - len(duplicates)}")
    
    db.close()

if __name__ == "__main__":
    print("Cleaning up duplicate emails...")
    cleanup_duplicates()
    print("\n✨ Cleanup complete!")
