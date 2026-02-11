from fastapi import FastAPI, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import base64 # Import base64 for encoding PDF content
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

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
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "your_sendgrid_verified_email@example.com") # Use a verified sender email in SendGrid
    to_email = "ractenopen@gmail.com" # Your target email for testing

    if not sendgrid_api_key:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "SendGrid API Key is not configured."}
        )
    
    # Ensure FROM_EMAIL is set and verified in SendGrid
    if from_email == "your_sendgrid_verified_email@example.com":
         return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "FROM_EMAIL is not configured or is not a verified sender in SendGrid. Please check .env and SendGrid settings."}
        )

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject="Test Email from FastAPI Backend (SendGrid)",
        html_content="This is a test email sent from the FastAPI backend using SendGrid."
    )

    try:
        sendgrid_client = SendGridAPIClient(sendgrid_api_key)
        response = sendgrid_client.send(message)

        if response.status_code == 202:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Test email sent successfully via SendGrid!"})
        else:
            print(f"SendGrid Error: Status Code: {response.status_code}, Body: {response.body}, Headers: {response.headers}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": f"Failed to send test email via SendGrid. Status: {response.status_code}, Response: {response.body.decode()}"}
            )
    except Exception as e:
        print(f"Error sending test email with SendGrid: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Failed to send test email with SendGrid: {e}"}
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
    encoded_pdf = base64.b64encode(pdf_content).decode() # Base64 encode for SendGrid attachment

    # --- Email Sending Logic ---
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "your_sendgrid_verified_email@example.com") # Use a verified sender email in SendGrid
    to_email = "ractenopen@gmail.com" # Your target email

    if not sendgrid_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SendGrid API Key is not configured."
        )
    
    # Ensure FROM_EMAIL is set and verified in SendGrid
    if from_email == "your_sendgrid_verified_email@example.com":
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="FROM_EMAIL is not configured or is not a verified sender in SendGrid. Please check .env and SendGrid settings."
        )


    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=f"New Print Request from {recipient_name}",
        html_content=f"""
            <p>Hello,</p>
            <p>A new print request has been submitted.</p>
            <p><strong>Recipient Name:</strong> {recipient_name}</p>
            <p>Please find the PDF file attached.</p>
        """
    )

    attachedFile = Attachment(
        FileContent(encoded_pdf),
        FileName(pdf_file.filename),
        FileType(pdf_file.content_type),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    try:
        sendgrid_client = SendGridAPIClient(sendgrid_api_key)
        response = sendgrid_client.send(message)

        if response.status_code == 202:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "PDF uploaded and email sent successfully via SendGrid!"})
        else:
            print(f"SendGrid Error: Status Code: {response.status_code}, Body: {response.body}, Headers: {response.headers}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send email via SendGrid. Status: {response.status_code}, Response: {response.body.decode()}"
            )
    except Exception as e:
        print(f"Error sending email with SendGrid: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email with SendGrid: {e}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))