import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Path to your JSON file containing employee emails
json_file = "resources/data/data.json"  # Ensure this path is correct

def employees_emails():
    """Retrieve a list of employee emails from the JSON file."""
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)  # Load JSON data

    # Extract emails from the JSON data
    emails = [employee["email"] for employee in data.get("employees", {}).values()]
    return emails

def send_emails(api_key, sender_email, target_email):
    """Send emails to the specified target email if it exists in the employee emails list."""
    recipient_emails = employees_emails()

    # Check if the target email is in the list of recipient emails
    if target_email in recipient_emails:
        # Email content
        subject = "Your Schedule for the Upcoming Week"
        body = """
        Dear Team Member,

        Please find attached your schedule for the upcoming week.

        Best regards,
        Management Team
        """

        # Initialize SendGrid client
        sg = SendGridAPIClient(api_key)

        # Create the email message
        message = Mail(
            from_email=sender_email,
            to_emails=target_email,
            subject=subject,
            plain_text_content=body
        )

        try:
            response = sg.send(message)
            print(f"Email sent to {target_email}: {response.status_code}")
        except Exception as e:
            print(f"Failed to send email to {target_email}: {str(e)}")
    else:
        print(f"{target_email} not found in the recipient list.")

if __name__ == "__main__":
    # Retrieve SendGrid API key from environment variables
    api_key = "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"
    if not api_key:
        raise ValueError("SENDGRID_API_KEY environment variable not set")

    # Sender's email address (must be verified with SendGrid)
    sender_email = 'schedulemaker@gmx.com'  # Replace with your SendGrid verified sender email

    # Target email to send the schedule
    target_email = 'scheduleMaker@gmx.com'

    # Send email
    send_emails(api_key, sender_email, target_email)