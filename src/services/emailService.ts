import { User, Contact } from '../types';

// Interface for email sending options
interface SendEmailOptions {
  to: string[];
  subject: string;
  body: string;
}

// URL for our Python backend API
const EMERGENCY_API_URL = import.meta.env.VITE_EMERGENCY_API_URL || 'http://localhost:8000';

/**
 * Sends an email via a hypothetical API endpoint
 * In a real application, this would connect to an email service API
 */
export const sendEmail = async (options: SendEmailOptions): Promise<boolean> => {
  // In a real app, this would use an actual email service API
  console.log('Sending email:', options);
  
  // Simulate API call
  try {
    // Mock successful email sending
    await new Promise(resolve => setTimeout(resolve, 500));
    return true;
  } catch (error) {
    console.error('Failed to send email:', error);
    return false;
  }
};

/**
 * Sends an email notification using the Python SMTP backend
 */
export const sendMIMENotification = async (
  user: User,
  emotionScore: number,
  message: string,
  relationships?: Contact['relationship'][]
): Promise<boolean> => {
  try {
    // Filter out contacts without emails
    const validContacts = user.contacts.filter(contact => 
      contact.email && contact.email.trim() !== ''
    );
    
    // Create a user object with only valid contacts
    const userWithValidContacts = {
      ...user,
      contacts: validContacts
    };
    
    const response = await fetch(`${EMERGENCY_API_URL}/api/notify/emergency`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user: userWithValidContacts,
        emotionScore,
        message,
        relationships
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Failed to send MIME notification:', errorData);
      return false;
    }
    
    const data = await response.json();
    console.log('MIME notification sent successfully:', data);
    return true;
    
  } catch (error) {
    console.error('Error sending MIME notification:', error);
    return false;
  }
};

/**
 * Sends an emergency alert email to all contacts of specified relationships
 * @param user - The user whose contacts should be notified
 * @param emotionScore - The score indicating distress level
 * @param message - The message content that triggered the alert
 * @param relationships - Types of contacts to notify (defaults to counselor and parent only for high priority)
 * @param useMIME - Whether to use the Python SMTP backend for sending (defaults to true)
 */
export const sendEmergencyAlert = async (
  user: User,
  emotionScore: number,
  message: string,
  relationships: Contact['relationship'][] = ['counselor', 'parent'],
  useMIME: boolean = true
): Promise<boolean> => {
  // Filter contacts by specified relationships and ensure they have email addresses
  const contactsToAlert = user.contacts.filter(contact => 
    relationships.includes(contact.relationship) && 
    contact.email && 
    contact.email.trim() !== ''
  );
  
  if (contactsToAlert.length === 0) {
    console.warn(`No emergency contacts found for user ${user.id} with specified relationships: ${relationships.join(', ')}`);
    
    // Show user-friendly message about missing contacts
    if (typeof window !== 'undefined') {
      const missingContacts = relationships.filter(rel => 
        !user.contacts.some(c => c.relationship === rel && c.email)
      );
      
      if (missingContacts.length > 0) {
        console.warn(`Missing emergency contacts: ${missingContacts.join(', ')}`);
        // You could show a toast notification here
      }
    }
    
    return false;
  }
  
  // Use MIME notification if requested (and available)
  if (useMIME) {
    try {
      console.log(`Sending emergency alert for user ${user.id} with distress score ${emotionScore}`);
      return await sendMIMENotification(user, emotionScore, message, relationships);
    } catch (error) {
      console.error('MIME notification failed, falling back to regular email:', error);
      // Continue with regular email as fallback
    }
  }
  
  // Format the email (used as fallback if MIME fails)
  const severity = emotionScore >= 90 ? 'CRITICAL' : emotionScore >= 80 ? 'HIGH' : 'ELEVATED';
  
  const emailOptions: SendEmailOptions = {
    to: contactsToAlert.map(contact => contact.email).filter(Boolean) as string[],
    subject: `🚨 ${severity} ALERT: Emotional Support Needed for ${user.name}`,
    body: `
      <h2>🚨 Emergency Alert: High Emotional Distress Detected</h2>
      <p><strong>${user.name}</strong> is experiencing significant emotional distress and may need immediate support.</p>
      
      <h3>Alert Details:</h3>
      <ul>
        <li><strong>Severity Level:</strong> ${severity}</li>
        <li><strong>Distress Score:</strong> ${emotionScore}/100</li>
        <li><strong>Timestamp:</strong> ${new Date().toLocaleString()}</li>
        <li><strong>Message Content:</strong> "${message}"</li>
      </ul>
      
      <h3>🤝 Recommended Actions:</h3>
      <ul>
        <li>Reach out to ${user.name} immediately via phone or text</li>
        <li>Ask open-ended questions about their feelings</li>
        <li>Listen actively and validate their emotions</li>
        <li>Encourage professional help if needed</li>
        <li>Follow up within 24 hours</li>
      </ul>
      
      <h3>📞 Crisis Resources:</h3>
      <ul>
        <li><strong>National Suicide Prevention Lifeline:</strong> 988</li>
        <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
      </ul>
      
      <hr>
      <p><small>This is an automated message from the BrightSide Emotional Support Platform.</small></p>
    `
  };
  
  return sendEmail(emailOptions);
};
