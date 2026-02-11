require('dotenv').config();
const express = require('express');
const multer = require('multer');
const nodemailer = require('nodemailer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000;

// Enable CORS for all origins during development. For production, restrict to your frontend origin.
app.use(cors());

// Configure Multer for file uploads
const storage = multer.memoryStorage(); // Store file in memory as a Buffer
const upload = multer({
    storage: storage,
    limits: { fileSize: 10 * 1024 * 1024 }, // 10MB file size limit
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Only PDF files are allowed!'), false);
        }
    }
});

// Nodemailer transporter configuration
const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false, // use TLS
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    },
    tls: {
        rejectUnauthorized: false
    }
});

// Serve the static frontend files (if both frontend and backend are in the same Render service)
// In this case, the frontend will be a separate static site on Render, so this part is commented out or removed.
// If you decide to serve frontend from this backend, uncomment and adjust path.
// app.use(express.static(path.join(__dirname, '../../'))); // Adjust path to your 'printing service' root

// Upload endpoint
app.post('/upload', upload.single('pdfFile'), async (req, res) => {
    // Server-side validation check (Multer's fileFilter already handles this, but good to have)
    if (!req.file) {
        return res.status(400).json({ message: 'No PDF file uploaded or invalid file type.' });
    }

    if (!req.body.recipientName) {
        return res.status(400).json({ message: 'Recipient name is required.' });
    }

    const recipientName = req.body.recipientName;
    const pdfBuffer = req.file.buffer;
    const originalname = req.file.originalname;

    try {
        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: 'ractenopen@gmail.com', // Your target email
            subject: `New Print Request from ${recipientName}`,
            html: `
                <p>Hello,</p>
                <p>A new print request has been submitted.</p>
                <p><strong>Recipient Name:</strong> ${recipientName}</p>
                <p>Please find the PDF file attached.</p>
            `,
            attachments: [
                {
                    filename: originalname,
                    content: pdfBuffer,
                    contentType: 'application/pdf'
                }
            ]
        };

        await transporter.sendMail(mailOptions);
        res.status(200).json({ message: 'PDF uploaded and email sent successfully!' });
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).json({ message: 'Failed to send email.', error: error.message });
    }
});

// Basic route for health check or testing
app.get('/', (req, res) => {
    res.send('Royette Printing Service Backend is running!');
});

// Error handling for Multer
app.use((err, req, res, next) => {
    if (err instanceof multer.MulterError) {
        return res.status(400).json({ message: `Multer error: ${err.message}` });
    } else if (err) {
        return res.status(400).json({ message: err.message });
    }
    next();
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
