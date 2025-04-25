import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_HOST_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

def send_task_assignment_email(to_email, task_title, assigned_by):
    try:
        # Establish a connection to Gmail's SMTP server using SSL
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        # Log in to your Gmail account
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Create the email message
        msg = EmailMessage()
        msg['From'] = 'Task Management'
        msg['To'] = to_email
        msg['Subject'] = f"📌 New Task Assigned: {task_title}"

        # Beautified email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
                <h2 style="color: #4CAF50;">🔔 Task Assignment Notification</h2>
                <p>Hello,</p>
                <p>
                    You have been assigned a new task titled:
                    <strong style="color: #2F80ED;">{task_title}</strong>
                    by <strong>{assigned_by}</strong>.
                </p>
                <p>
                    Kindly log in to your Task Management Dashboard to view more details.
                </p>
                <a href="http://127.0.0.1:8000/api/auth/login/" style="display: inline-block; padding: 10px 15px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px;">
                    View Task
                </a>
                <p style="margin-top: 30px; font-size: 12px; color: #999;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """

        msg.add_alternative(html_content, subtype='html')

        # Send the email
        server.send_message(msg)

        # Close the SMTP connection
        server.quit()

        print('Email sent')
        return {"status_code": 200, "message": "Email sent successfully."}

    except smtplib.SMTPException as e:
        return {"status_code": 500, "message": f"SMTP Error: {str(e)}"}

    except Exception as e:
        return {"status_code": 500, "message": f"Error: {str(e)}"}
