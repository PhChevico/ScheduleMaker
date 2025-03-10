from flask import Flask, render_template_string, request, redirect, url_for
import json
import scheduler
import markdown
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
app = Flask(__name__)

SCHEDULE_FILE = './resources/data/schedule.json'


def send_email(api_key, sender_email, target_email):
    """Function to send the email using SendGrid."""
    sg = sendgrid.SendGridAPIClient(api_key)
    from_email = Email(sender_email)
    to_email = To(target_email)
    subject = "Weekly Schedule"
    content = Content("text/plain", "Please find the schedule attached.")

    mail = Mail(from_email, to_email, subject, content)
    response = sg.send(mail)
    return response


def load_schedule():
    """Load schedule data from JSON and convert markdown table to HTML."""
    try:
        with open(SCHEDULE_FILE, 'r', encoding="utf-8") as file:
            data = json.load(file)

            # Extract Markdown schedule text from JSON
            schedule_text = data.get("schedule", {}).get("choices", [{}])[0].get("message", {}).get("content", "")

            # Remove triple backticks (```) if they exist at the start and end
            if schedule_text.startswith("```") and schedule_text.endswith("```"):
                schedule_text = schedule_text.strip("```").strip()

            # Convert Markdown to HTML (ensuring tables are properly formatted)
            schedule_html = markdown.markdown(schedule_text, extensions=["tables"])

            return schedule_text, schedule_html  # Return both text and formatted HTML

    except FileNotFoundError:
        return "", "<p>Schedule file not found.</p>"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission for schedule update
        additional_prompt = request.form.get('additional_prompt', '').strip()
        scheduler.generate_schedule(additional_prompt)
        return redirect(url_for('index'))

    # Handle email send request
    if request.method == 'POST' and request.form.get('send_email'):
        # Call the SendGrid API to send the email
        api_key = "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"
        sender_email = 'schedulemaker@gmx.com'
        target_email = 'scheduleMaker@gmx.com'

        send_email(api_key, sender_email, target_email)
        return redirect(url_for('index'))  # Redirect after sending email

    # Load the current schedule
    current_prompt, schedule_html = load_schedule()

    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Schedule - Sunset Boho</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            padding: 20px; 
            background-color: #f9f9f9; 
            color: #333;
            text-align: center;
        }

        h1 {
            color: #444; 
            margin-bottom: 10px;
        }

        form {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            margin: 20px auto;
        }

        textarea {
            width: 100%; 
            height: 120px; 
            border: 1px solid #ccc; 
            border-radius: 5px; 
            padding: 10px; 
            font-size: 16px;
            resize: vertical;
        }

        input[type="submit"] {
            background-color: #5c67f2;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }

        input[type="submit"]:hover {
            background-color: #4752c4;
        }

        .schedule-container {
            max-width: 1200px;
            margin: 20px auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        table { 
            width: 100%; 
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td { 
            padding: 12px; 
            border: 1px solid #ddd; 
            text-align: left; 
        }

        th {
            background-color: #5c67f2;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f3f3f3;
        }
    </style>
</head>
<body>
    <h1>Weekly Schedule - Sunset Boho</h1>

    <form method="POST">
        <textarea name="additional_prompt" placeholder="Enter additional instructions to modify the schedule..."></textarea>
        <br>
        <input type="submit" value="Update Schedule">
    </form>
    
    <button>
    <input type="submit" value="Send Schedule Email">
    </button>

    <div class="schedule-container">
        <h3>Current Schedule:</h3>
        <div>
            {{ schedule_html | safe }}  <!-- Render the markdown-converted table -->
        </div>
    </div>
</body>
</html>

    ''', schedule_html=schedule_html)


if __name__ == '__main__':
    app.run(debug=True)
