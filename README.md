<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=180&section=header&text=Royette%20Printing%20Service%20🖨️&fontSize=38&fontAlignY=32&desc=Automated%20PDF%20Print%20Request%20System&descAlignY=51&descAlign=50&animation=twinkling"/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=00D4FF&center=true&vCenter=true&width=435&lines=FastAPI+Backend;SendGrid+Integration;Automated+PDF+Workflow;Clean+Web+Frontend)](https://git.io/typing-svg)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![SendGrid](https://img.shields.io/badge/SendGrid-00B2E2?style=for-the-badge&logo=sendgrid&logoColor=white)

</div>

---

# Royette Printing Service

An automated system for handling print requests. Users can upload PDF files which are then automatically forwarded to the service via email.

## 🚀 Features

- **PDF Upload:** Seamlessly upload documents for printing.
- **Automated Notifications:** Uses SendGrid to send email notifications with attachments.
- **FastAPI Backend:** High-performance Python backend for handling file uploads.
- **CORS Support:** Ready for cross-origin frontend integration.

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript.
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python).
- **Email Service:** [SendGrid API](https://sendgrid.com/).
- **Server:** Uvicorn.

## 📦 Getting Started

### Prerequisites

- Python 3.8+
- SendGrid API Key

### Backend Setup

1. **Navigate to the backend folder:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the `backend/` directory:
   ```env
   SENDGRID_API_KEY=your_api_key
   FROM_EMAIL=your_verified_sender@example.com
   ```

4. **Run the server:**
   ```bash
   python main.py
   ```

### Frontend Setup

Open `index.html` in your browser or serve it using a local web server.

---

<div align="center">

💡 *Built with ❤️ by [RactOpen](https://github.com/ractopen)* 💡

</div>
