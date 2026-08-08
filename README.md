# SpamGuard Frontend

A clean and lightweight **Streamlit frontend** for the SpamGuard AI email spam detection system.

SpamGuard Frontend provides a user-friendly interface where users can paste email content and receive a machine-learning-based spam classification from the separate SpamGuard FastAPI backend.

---

## Overview

SpamGuard Frontend acts as the presentation layer for the SpamGuard AI system.

The frontend does **not** contain or load the machine-learning model. Instead, it communicates with the separate FastAPI backend through a REST API.

```text
```
┌─────────────────────────────┐
│      SpamGuard Frontend     │
│                             │
│          Streamlit          │
│                             │
│   Email Input               │
│   Prediction Results        │
│   Probability Visualization │
└──────────────┬──────────────┘
               │
               │ HTTP / JSON
               ▼
┌─────────────────────────────┐
│      SpamGuard Backend      │
│                             │
│           FastAPI           │
│              │              │
│              ▼              │
│     Feature Extraction      │
│              │              │
│              ▼              │
│      Random Forest Model    │
└─────────────────────────────┘
#Features
Email text analysis
Machine-learning-based spam classification
Spam / Not Spam prediction
Prediction confidence
Spam probability
Not Spam probability
Probability visualization
FastAPI REST API integration
Environment-based backend URL configuration
Backend connection error handling
Request timeout handling
Clean and responsive Streamlit interface
Custom cream, red, and orange visual theme
Architecture

SpamGuard is divided into two independent repositories.

#Frontend
Streamlit
    │
    │ POST /predict
    ▼
FastAPI Backend
Backend
FastAPI
    │
    ▼
Feature Extraction
    │
    ▼
57 Spambase Features
    │
    ▼
Random Forest Model
    │
    ▼
Prediction
#Complete System
                  USER
                   │
                   ▼
        ┌────────────────────┐
        │ Streamlit Frontend │
        │      :8501         │
        └─────────┬──────────┘
                  │
             HTTP Request
                  │
                  ▼
        ┌────────────────────┐
        │   FastAPI Backend  │
        │      :8000         │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Feature Extraction │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │   Random Forest    │
        │       Model        │
        └─────────┬──────────┘
                  │
                  ▼
             Prediction
                  │
                  ▼
        ┌────────────────────┐
        │ Streamlit Result   │
        └────────────────────┘
#Tech Stack
Technology	Purpose
Python 3.12	Runtime
Streamlit	Frontend UI
Requests	HTTP communication
python-dotenv	Environment variable management
FastAPI	Backend API
Scikit-learn	Machine learning
Random Forest	Spam classification
Project Structure
spamguard-frontend/
│
├── .venv/
│
├── app.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
File Description

app.py	Main Streamlit application
.env	Local environment configuration
.env.example	Example environment configuration
.gitignore	Git ignored files
requirements.txt	Python dependencies
README.md	Project documentation
Requirements
Python

The project uses:

Python 3.12

Python 3.12 is used for consistency with the SpamGuard backend development environment.

The frontend does not load the machine-learning model directly, so it does not require the backend's machine-learning dependencies.

#Installation
1. Clone the Repository
git clone <YOUR_REPOSITORY_URL>

Navigate into the project:

cd spamguard-frontend
2. Create the Virtual Environment

#Windows:

py -3.12 -m venv .venv
3. Activate the Virtual Environment
.\.venv\Scripts\Activate.ps1

After activation, the terminal should display:

(.venv)
4. Install Dependencies
pip install -r requirements.txt
Environment Variables

The frontend communicates with the FastAPI backend through the BACKEND_URL environment variable.

Create a .env file in the project root:

BACKEND_URL=http://127.0.0.1:8000
.env.example

The repository should contain:

BACKEND_URL=http://127.0.0.1:8000

The .env file should not be committed to Git.

#Production

When the backend is deployed, change the value:

BACKEND_URL=https://your-backend-domain.com

No changes to the Streamlit application code are required.

Running the Application

SpamGuard requires both the backend and frontend to be running during local development.

Start the Backend

Open a terminal for the backend repository:

cd spamguard-backend

Activate its environment:

.\.venv\Scripts\Activate.ps1

Start FastAPI:

uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000
Start the Frontend

Open another terminal:

cd spamguard-frontend

Activate the frontend environment:

.\.venv\Scripts\Activate.ps1

Run Streamlit:

streamlit run app.py

The application will normally be available at:

http://localhost:8501
API Integration

The frontend communicates with the backend through:

POST /predict
Request

The frontend sends:

{
  "email": "Congratulations! You have won $5000!"
}
Response

The backend returns:

{
  "prediction": "SPAM",
  "confidence": 0.92,
  "spam_probability": 0.92,
  "ham_probability": 0.08
}

The Streamlit application uses these values to render the prediction results.

#Prediction Flow
Email
  │
  ▼
Streamlit Input
  │
  ▼
POST /predict
  │
  ▼
FastAPI
  │
  ▼
Feature Extraction
  │
  ▼
57 Features
  │
  ▼
Random Forest
  │
  ├───────────────┐
  ▼               ▼
SPAM          NOT SPAM
  │               │
  └───────┬───────┘
          ▼
    Probability
          │
          ▼
     JSON Response
          │
          ▼
     Streamlit UI
#User Interface

The interface follows a minimal, product-oriented design.

Design
Cream background
Deep red primary color
Orange accent color
Dark brown typography
Off-white cards
Light red spam classification state
Warm orange safe classification state
Minimal visual decoration
No unnecessary emojis
No oversized centered hero text
Left-aligned typography
Clear information hierarchy
Main Interface
SPAMGUARD

Email Spam Detection
Analyze email content using a trained machine learning model.

#Email content

┌───────────────────────────────────────────────┐
│                                               │
│ Paste the email you want to analyze here...  │
│                                               │
│                                               │
└───────────────────────────────────────────────┘

                 Analyze Email

#Classification

┌───────────────────────────────────────────────┐
│ Spam detected                                 │
│ The model identified characteristics          │
│ commonly associated with spam.                │
└───────────────────────────────────────────────┘

#Model Results

┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ CONFIDENCE   │ │ SPAM         │ │ NOT SPAM     │
│ 92.0%        │ │ 92.0%        │ │ 8.0%         │
└──────────────┘ └──────────────┘ └──────────────┘
#Prediction Results
Spam

When the model predicts spam, the application displays:

Classification

Spam detected

The model identified characteristics
commonly associated with spam.

The interface also displays:

Confidence
Spam probability
Not Spam probability
Prediction probability chart
Not Spam

When the model predicts a legitimate message:

#Classification

Not spam

The model did not identify strong
spam characteristics in this email.

The interface displays the same probability and confidence information.

Error Handling

The frontend handles common backend communication problems.

Backend Unavailable

If FastAPI is not running:

Unable to connect to the backend.
Request Timeout

If the backend takes too long:

The backend took too long to respond.
HTTP Errors

HTTP errors returned by the backend are caught and displayed in the Streamlit interface.

#Development

During local development, two terminals are required.

Terminal 1 — Backend
cd spamguard-backend
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
Terminal 2 — Frontend
cd spamguard-frontend
.\.venv\Scripts\Activate.ps1
streamlit run app.py

The resulting architecture is:

Frontend
localhost:8501
     │
     │ HTTP
     ▼
Backend
localhost:8000
     │
     ▼
Machine Learning Model
Repository Separation

SpamGuard uses separate repositories for the frontend and backend.

spamguard-frontend

Responsible for:

User interface
Email input
API communication
Prediction visualization
Frontend configuration
spamguard-backend

Responsible for:

FastAPI API
Feature extraction
Machine-learning model
Prediction logic
Model artifacts

This separation allows the frontend and backend to be developed, deployed, and maintained independently.
