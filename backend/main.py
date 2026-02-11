from fastapi import FastAPI, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import mimetypes
import aiosmtplib
from email.message import EmailMessage

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow CORS for the frontend
# In production, change allow_origins to the specific URL of your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "FastAPI backend for Royette Printing Service is running!"}

@app.get("/test-email")
async def test_email():
    mailgun_smtp_login = os.getenv("MAILGUN_SMTP_LOGIN")
    mailgun_smtp_password = os.getenv("MAILGUN_SMTP_PASSWORD")
    mailgun_smtp_host = os.getenv("MAILGUN_SMTP_HOST", "smtp.mailgun.org")
    mailgun_smtp_port = int(os.getenv("MAILGUN_SMTP_PORT", 587))
    from_email = os.getenv("FROM_EMAIL")
    receiver_email = "ractenopen@gmail.com" # Your target email for testing

    if not all([mailgun_smtp_login, mailgun_smtp_password, from_email]):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Mailgun SMTP credentials (MAILGUN_SMTP_LOGIN, MAILGUN_SMTP_PASSWORD, FROM_EMAIL) are not configured."}
        )

    test_msg = EmailMessage()
    test_msg["From"] = from_email
    test_msg["To"] = receiver_email
    test_msg["Subject"] = "Test Email from FastAPI Backend (Mailgun)"
    test_msg.set_content("This is a test email sent from the FastAPI backend using Mailgun.")

    try:
        await aiosmtplib.send(
            test_msg,
            hostname=mailgun_smtp_host,
            port=mailgun_smtp_port,
            start_tls=True, # Use STARTTLS for port 587
            username=mailgun_smtp_login,
            password=mailgun_smtp_password,
            timeout=30
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Test email sent successfully via Mailgun!"})
    except Exception as e:
        print(f"Error sending test email via Mailgun: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Failed to send test email via Mailgun: {e}"}
        )

@app.post("/upload")
async def upload_pdf(
    pdf_file: UploadFile,
    recipient_name: str = Form(...)
):
    if not recipient_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recipient name is required."
        )

    # Server-side validation for PDF file type
    if (not pdf_file.filename.lower().endswith(".pdf") or
            pdf_file.content_type != "application/pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # Read the PDF content
    pdf_content = await pdf_file.read()

    # --- Email Sending Logic ---
    mailgun_smtp_login = os.getenv("MAILGUN_SMTP_LOGIN")
    mailgun_smtp_password = os.getenv("MAILGUN_SMTP_PASSWORD")
    mailgun_smtp_host = os.getenv("MAILGUN_SMTP_HOST", "smtp.mailgun.org")
    mailgun_smtp_port = int(os.getenv("MAILGUN_SMTP_PORT", 587))
    from_email = os.getenv("FROM_EMAIL")
    receiver_email = "ractenopen@gmail.com" # Your target email

    if not all([mailgun_smtp_login, mailgun_smtp_password, from_email]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Mailgun SMTP credentials (MAILGUN_SMTP_LOGIN, MAILGUN_SMTP_PASSWORD, FROM_EMAIL) are not configured."
        )

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = receiver_email
    msg["Subject"] = f"New Print Request from {recipient_name}"
    msg.set_content(f"""
        Hello,

        A new print request has been submitted.
        Recipient Name: {recipient_name}

        Please find the PDF file attached.
    """)

    # Attach the PDF file
    maintype, subtype = "application", "pdf"
    msg.add_attachment(pdf_content, maintype=maintype, subtype=subtype, filename=pdf_file.filename)

    try:
        await aiosmtplib.send(
            msg,
            hostname=mailgun_smtp_host,
            port=mailgun_smtp_port,
            start_tls=True, # Use STARTTLS for port 587
            username=mailgun_smtp_login,
            password=mailgun_smtp_password,
            timeout=30 # Set a timeout for email sending
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "PDF uploaded and email sent successfully!"})
    except Exception as e:
        print(f"Error sending email via Mailgun: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email via Mailgun: {e}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))