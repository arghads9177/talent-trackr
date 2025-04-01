# TalentTrackr

TalentTrackr is an AI-powered Applicant Tracking System (ATS) designed to simplify and enhance the recruitment process by leveraging LLMs for resume matching, summarization, and optimization. Built using **LangChain**, **ChromaDB**, **MySQL**, and **Streamlit**.

---

## 📌 Features

### 1. User Authentication System
- **Signup System:**
  - Collects `email`, `firstname`, `lastname`, `username`, and `password`.
  - Stores user data securely in MySQL using hashed passwords.
  - Prevents duplicate usernames and emails.

- **Sign In System:**
  - Verifies the username and password from the MySQL database.
  - Generates session tokens for authenticated users.

---

### 2. ATS Score Generation System
- Upload a resume (PDF) and provide a Job Description.
- Uses LLM (Groq’s LLaMA via LangChain) to generate embeddings for both.
- Calculates a percentage match between resume and job description.
- Stores results in MySQL for analysis and retrieval.

---

### 3. Resume Summarization System
- Upload a resume (PDF) and summarize it using LLM.
- Generates a concise summary highlighting key skills and experience.
- Stores summaries in MySQL for future use.

---

### 4. ATS-friendly Resume Generation System
- Upload a resume (PDF) and provide a Job Description.
- Uses LLM to optimize the resume for the given job description.
- Provides download options for optimized resumes in Word and PDF formats.

---

## 🛠️ Tech Stack
- **Backend:** LangChain, ChromaDB, MySQL
- **Frontend:** Streamlit
- **LLM:** Groq’s LLaMA

---

## 📁 Project Structure
```
TalentTrackr/
├── backend/          # LangChain backend logic
├── frontend/         # Streamlit app code
├── data/             # Sample resumes, job descriptions, embeddings
├── database/         # MySQL database schemas and migration scripts
├── models/           # Fine-tuned LLMs
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```
git clone https://github.com/argha9177/talent-trackr.git
cd talent-trackr
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Configure MySQL Database
- Create a database named `talenttrackr` and execute the provided SQL schema.
- Update database connection details in the backend code.

### 4. Run the Application
```
streamlit run frontend/app.py
```

---

## 📌 Future Enhancements
- Implement user role management (Applicant, Recruiter, Admin).
- Add detailed analytics and reporting for ATS scores.
- Enhance resume optimization capabilities using fine-tuned LLMs.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Contact
For inquiries, contact [email2argha@gmail.com].

https://www.youtube.com/watch?v=EECUXqFrwbc
