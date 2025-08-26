#!/usr/bin/env python3
"""
Emergency Email Notification Service

This script provides functionality to send MIMEText SMTP email notifications
to emergency contacts when a user is experiencing emotional distress.
"""

import os
import json
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Email configuration
# These should be set in environment variables for security
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
DEFAULT_FROM = os.environ.get("DEFAULT_FROM", SMTP_USERNAME)
EMERGENCY_ALERT_ENABLED = os.environ.get("EMERGENCY_ALERT_ENABLED", "true").lower() == "true"
MAX_ALERTS_PER_HOUR = int(os.environ.get("MAX_ALERTS_PER_HOUR", "5"))

# Rate limiting storage (in production, use Redis or database)
alert_history = []

def validate_email_config():
    """Validate that required email configuration is present."""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.error("SMTP_USERNAME and SMTP_PASSWORD must be set in environment variables")
        return False
    if "@" not in SMTP_USERNAME:
        logger.error("SMTP_USERNAME must be a valid email address")
        return False
    return True

def is_rate_limited(user_id: str) -> bool:
    """Check if user has exceeded the rate limit for emergency alerts."""
    global alert_history
    current_time = datetime.now()
    hour_ago = current_time - timedelta(hours=1)
    
    # Clean old entries
    alert_history = [entry for entry in alert_history if entry['timestamp'] > hour_ago]
    
    # Count alerts for this user in the last hour
    user_alerts = len([entry for entry in alert_history if entry['user_id'] == user_id])
    
    if user_alerts >= MAX_ALERTS_PER_HOUR:
        logger.warning(f"Rate limit exceeded for user {user_id}: {user_alerts} alerts in last hour")
        return True
    
    return False

def record_alert(user_id: str):
    """Record an alert in the rate limiting history."""
    global alert_history
    alert_history.append({
        'user_id': user_id,
        'timestamp': datetime.now()
    })

class Contact:
    """Represents an emergency contact."""
    def __init__(self, name: str, email: str, relationship: str, phone: Optional[str] = None):
        self.name = name
        self.email = email
        self.relationship = relationship
        self.phone = phone

    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create a Contact from a dictionary."""
        return cls(
            name=data.get("name", ""),
            email=data.get("email", ""),
            relationship=data.get("relationship", ""),
            phone=data.get("phone")
        )

class User:
    """Represents a user with emergency contacts."""
    def __init__(self, id: str, name: str, email: str, contacts: List[Contact]):
        self.id = id
        self.name = name
        self.email = email
        self.contacts = contacts
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create a User from a dictionary."""
        contacts = [Contact.from_dict(c) for c in data.get("contacts", [])]
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email", ""),
            contacts=contacts
        )


def send_mime_email(
    to_addresses: List[str], 
    subject: str, 
    html_content: str, 
    from_address: str = DEFAULT_FROM
) -> bool:
    """
    Send a MIME email to a list of recipients.
    
    Args:
        to_addresses: List of recipient email addresses
        subject: Email subject
        html_content: HTML content of the email
        from_address: Sender email address
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not validate_email_config():
        logger.error("Email configuration is invalid")
        return False
    
    if not EMERGENCY_ALERT_ENABLED:
        logger.info("Emergency alerts are disabled")
        return False
    
    if not to_addresses:
        logger.warning("No recipients specified")
        return False

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = ', '.join(to_addresses)
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        msg.attach(html_part)
        
        # Create plain text version as fallback
        plain_text = html_content.replace('<h2>', '').replace('</h2>', '\n\n')
        plain_text = plain_text.replace('<h3>', '').replace('</h3>', '\n')
        plain_text = plain_text.replace('<p>', '').replace('</p>', '\n')
        plain_text = plain_text.replace('<strong>', '').replace('</strong>', '')
        plain_text = plain_text.replace('<ul>', '\n').replace('</ul>', '\n')
        plain_text = plain_text.replace('<li>', '- ').replace('</li>', '\n')
        plain_text = plain_text.replace('<hr>', '-' * 40 + '\n')
        plain_text = plain_text.replace('<small>', '').replace('</small>', '')
        
        text_part = MIMEText(plain_text, 'plain')
        msg.attach(text_part)
        
        # Connect to server and send
        logger.info(f"Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"Successfully sent emergency alert email to {len(to_addresses)} recipients: {', '.join(to_addresses)}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {str(e)}. Check your username and password.")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"Recipients refused: {str(e)}")
        return False
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"SMTP server disconnected: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False


def send_emergency_alert(
    user_data: Dict, 
    emotion_score: float, 
    message: str, 
    relationships: Optional[List[str]] = None
) -> bool:
    """
    Send emergency alert emails to specified contacts.
    
    Args:
        user_data: User data including contacts
        emotion_score: Score indicating distress level
        message: The message that triggered the alert
        relationships: Types of contacts to notify (defaults to all types)
        
    Returns:
        bool: True if emails were sent successfully, False otherwise
    """
    # Create User object from dictionary
    user = User.from_dict(user_data)
    
    # Check rate limiting
    if is_rate_limited(user.id):
        logger.warning(f"Rate limit exceeded for user {user.id}. Skipping alert.")
        return False
    
    # Filter contacts by relationship if specified
    relationships = relationships or ["counselor", "parent", "friend"]
    # Ensure relationship is always a string (in case it comes from TypeScript enum)
    sanitized_relationships = [str(r).lower() for r in relationships]
    contacts_to_alert = [c for c in user.contacts if c.relationship.lower() in sanitized_relationships and c.email]
    
    if not contacts_to_alert:
        logger.warning(f"No emergency contacts found for user {user.id} with specified relationships: {sanitized_relationships}")
        return False
    
    # Determine severity level
    severity = "CRITICAL" if emotion_score >= 90 else "HIGH" if emotion_score >= 80 else "ELEVATED"
    
    # Create email content
    subject = f"🚨 {severity} ALERT: Emotional Support Needed for {user.name}"
    html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">🚨 Emergency Alert</h1>
                <p style="margin: 5px 0 0 0; font-size: 16px;">High Emotional Distress Detected</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 0 0 10px 10px; border: 1px solid #dee2e6;">
                <h2 style="color: #dc3545; margin-top: 0;">Immediate Attention Required</h2>
                <p><strong>{user.name}</strong> is experiencing significant emotional distress and may need immediate support.</p>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #dc3545;">
                    <h3 style="margin-top: 0; color: #495057;">Alert Details:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li><strong>Severity Level:</strong> <span style="color: #dc3545; font-weight: bold;">{severity}</span></li>
                        <li><strong>Distress Score:</strong> {emotion_score}/100</li>
                        <li><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                        <li><strong>Your Relationship:</strong> {contacts_to_alert[0].relationship.title()}</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h3 style="margin-top: 0; color: #495057;">Recent Message:</h3>
                    <p style="font-style: italic; color: #6c757d; border-left: 3px solid #6c757d; padding-left: 15px; margin: 10px 0;">
                        "{message}"
                    </p>
                </div>
                
                <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #b3d9ff;">
                    <h3 style="margin-top: 0; color: #0066cc;">🤝 Recommended Actions:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; color: #333;">
                        <li>Reach out to {user.name} immediately via phone or text</li>
                        <li>Ask open-ended questions about their feelings</li>
                        <li>Listen actively and validate their emotions</li>
                        <li>Encourage professional help if needed</li>
                        <li>Follow up within 24 hours</li>
                    </ul>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #ffeaa7;">
                    <h3 style="margin-top: 0; color: #856404;">📞 Crisis Resources:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; color: #333;">
                        <li><strong>National Suicide Prevention Lifeline:</strong> 988</li>
                        <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
                        <li><strong>International Association for Suicide Prevention:</strong> <a href="https://www.iasp.info/resources/Crisis_Centres/">iasp.info</a></li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                    <p style="color: #6c757d; font-size: 14px; margin: 0;">
                        This is an automated alert from the BrightSide Emotional Support Platform.<br>
                        For technical issues, please contact support.
                    </p>
                </div>
            </div>
        </div>
    """
    
    # Send the email
    success = send_mime_email(
        to_addresses=[c.email for c in contacts_to_alert if c.email],
        subject=subject,
        html_content=html_content
    )
    
    if success:
        # Record the alert for rate limiting
        record_alert(user.id)
        logger.info(f"Emergency alert sent successfully for user {user.id} to {len(contacts_to_alert)} contacts")
    
    return success


def main():
    """Command line interface for sending emergency alerts."""
    parser = argparse.ArgumentParser(description='Send emergency email notifications')
    parser.add_argument('--user', '-u', required=True, help='JSON string or file path with user data')
    parser.add_argument('--score', '-s', type=float, required=True, help='Emotional distress score')
    parser.add_argument('--message', '-m', required=True, help='Message that triggered the alert')
    parser.add_argument('--relationships', '-r', nargs='+', help='Relationships to notify (defaults to all)')
    
    args = parser.parse_args()
    
    # Process user data (either from file or direct JSON)
    user_data = None
    if os.path.isfile(args.user):
        with open(args.user, 'r') as f:
            user_data = json.load(f)
    else:
        try:
            user_data = json.loads(args.user)
        except json.JSONDecodeError:
            print("Error: User data must be valid JSON or a path to a JSON file")
            return False
    
    # Send the alert
    return send_emergency_alert(
        user_data=user_data,
        emotion_score=args.score,
        message=args.message,
        relationships=args.relationships
    )


if __name__ == "__main__":
    main()
