import os
# import pymysql
import PyPDF2
# from langchain.embeddings import OpenAIEmbeddings
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from sklearn.metrics.pairwise import cosine_similarity
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from docx import Document
from fpdf import FPDF
from io import BytesIO
import markdown2
import weasyprint
from html2docx import html2docx

load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["HUGGINGFACE_API_KEY"] = os.getenv("HUGGINGFACE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Database connection
# def get_db_connection():
#     return pymysql.connect(
#         host=os.getenv("MYSQL_HOST"),
#         user=os.getenv("MYSQL_USER"),
#         password=os.getenv("MYSQL_PASSWORD"),
#         database=os.getenv("MYSQL_DATABASE"),
#         cursorclass=pymysql.cursors.DictCursor
#     )

# Convert PDF to Text
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Summarize Resume using LLM
def summarize_resume(resume_text):
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    ats_prompt = PromptTemplate(
        input_variables=["job_description","resume_text"],
        template="""
        You are an experienced Human Resource Manager with technical experience in the field of data science, Data Analyst, Big Data Engineering,
        Full Stack Web Development, Mobile App Development, DEVOPS, your task is to review the provided resume against the job description for these profiles. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

        Resume Text: "{resume_text}"
        """
    )
    # Output must be in JSON format with score, missing_keys, final_thought.
    ats_chain = ats_prompt | llm
    response = ats_chain.invoke({'resume_text': resume_text})
    return response.content.strip()
# Generate Embeddings using LangChain
# def generate_embeddings(text):
#     # embeddings = OpenAIEmbeddings()
#     embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
#     return embeddings.embed_query(text)

# # Calculate similarity score
# def calculate_similarity(embedding1, embedding2):
#     return cosine_similarity([embedding1], [embedding2])[0][0]

# Store ATS Score in Database
# def store_ats_score(user_id, resume_text, job_description, score):
#     connection = get_db_connection()
#     with connection.cursor() as cursor:
#         cursor.execute(
#             "INSERT INTO ats_scores (user_id, resume_text, job_description, similarity_score) VALUES (%s, %s, %s, %s)",
#             (user_id, resume_text, job_description, score)
#         )
#     connection.commit()
#     connection.close()

# ATS Score Generation Function
# def generate_ats_score(user_id, resume_pdf, job_description):
#     resume_text = extract_text_from_pdf(resume_pdf)
#     resume_embedding = generate_embeddings(resume_text)
#     job_description_embedding = generate_embeddings(job_description)

#     similarity_score = calculate_similarity(resume_embedding, job_description_embedding)
#     # store_ats_score(user_id, resume_text, job_description, similarity_score)
    
#     return similarity_score

def evaluate_resume_ats_score(user_id, resume_pdf, job_description):
    resume_text = extract_text_from_pdf(resume_pdf)
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    ats_prompt = PromptTemplate(
        input_variables=["job_description","resume_text"],
        template="""
        You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, Data Analyst, Big Data Engineering,
        Full Stack Web Development, Mobile App Development, DEVOPS and ATS functionality, your task is to evaluate the resume against the provided 
        job description. Give me the percentage of match if the resume matchesthe job description. 
        First the output should come as percentage and then keywords missing and last final thoughts.

        Job Description: "{job_description}"
        Resume Text: "{resume_text}"
        """
    )
    # Output must be in JSON format with score, missing_keys, final_thought.
    ats_chain = ats_prompt | llm
    response = ats_chain.invoke({'resume_text': resume_text, 'job_description': job_description})
    return response.content.strip()

# Resume Summarization Function
def generate_resume_summary(user_id, resume_pdf):
    resume_text = extract_text_from_pdf(resume_pdf)
    summarized_text = summarize_resume(resume_text)
    return summarized_text

# Generate ATS-Friendly Resume using LLM
def generate_ats_friendly_resume(resume_pdf, job_description):
    resume_text = extract_text_from_pdf(resume_pdf)
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    
    ats_prompt = PromptTemplate(
        input_variables=["job_description", "resume_text"],
        template="""
        You are an experienced Human Resource Manager with technical expertise in data science, data analysis, big data engineering, 
        full stack web development, mobile app development, and DevOps. Your task is to generate a professional resume that closely 
        matches the provided resume format and structure. Ensure that the resume highlights relevant skills, experiences, 
        and accomplishments effectively, maintaining a clean, modern, and visually appealing layout.

        Don't add any ATS generated resume information in the output. Output should contain the resume in the following format.

        Use the following format:

        Header:
            - Name: {Your Full Name}
            - Address: {Your Address}
            - Contact Number: {Your Contact Number}
            - Email: {Your Email}

        Personal Summary:
            {Write a concise, impactful summary highlighting your expertise, experience, and specializations.}

        Highlights:
            - {List of relevant skills and technologies, grouped under suitable categories like Programming Languages, Frameworks, Tools, etc.}

        Experience:
            {List professional experiences in reverse chronological order. Include role title, company name, location, duration, and key responsibilities.}

        Education:
            {Provide educational qualifications in reverse chronological order. Include degree, institution, year of completion, and GPA if applicable.}

        Accomplishments:
            {List key accomplishments, projects, or contributions relevant to the job description. Include web or mobile applications, systems developed, or other significant achievements.}

        Personal Information:
            - Date of Birth: {Your Date of Birth}
            - Nationality: {Your Nationality}
            - Marital Status: {Your Marital Status}

        Languages:
            {List languages you are proficient in.}

        Guardian Name:
            {Your Guardian's Name}

        Job Description: "{job_description}"
        Resume Text: "{resume_text}"

        """
    )

    ats_chain = ats_prompt | llm
    response = ats_chain.invoke({"job_description": job_description, "resume_text": resume_text})
    return response.content.strip()

# Save resume to Word file
def save_to_word(content, filename):
    # Ensure the folder exists
    os.makedirs("generated_resumes", exist_ok=True)
    
    doc = Document()
    doc.add_paragraph(content)
    file_path = os.path.join("generated_resumes", f"{filename}.docx")
    doc.save(file_path)
    return file_path

# Save resume to PDF file
def save_to_pdf(content, filename):
    # Ensure the folder exists
    os.makedirs("generated_resumes", exist_ok=True)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    file_path = os.path.join("generated_resumes", f"{filename}.pdf")
    pdf.output(file_path)
    return file_path

# Convert Markdown to DOCX
def get_docx(proposal):
    """Converts Markdown to DOCX using html2docx"""
    docx_stream = BytesIO()

    # Convert Markdown to HTML first
    html_content = markdown2.markdown(proposal)

    # Convert HTML to DOCX
    docx_bytes = html2docx(html_content, "Proposal")

    # Write to BytesIO
    docx_stream.write(docx_bytes.getvalue())
    docx_stream.seek(0)

    return docx_stream

# Convert Markdown to PDF Using WeasyPrint
def get_pdf(proposal):
    html_content = markdown2.markdown(proposal)
    pdf_stream = BytesIO()
    
    # Convert HTML to PDF
    pdf = weasyprint.HTML(string=html_content).write_pdf()
    pdf_stream.write(pdf)
    pdf_stream.seek(0)

    return pdf_stream