import os
# import pymysql
import PyPDF2
# from langchain.embeddings import OpenAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

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

# Generate Embeddings using LangChain
def generate_embeddings(text):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return embeddings.embed_query(text)

# Calculate similarity score
def calculate_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

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
def generate_ats_score(user_id, resume_pdf, job_description):
    resume_text = extract_text_from_pdf(resume_pdf)
    resume_embedding = generate_embeddings(resume_text)
    job_description_embedding = generate_embeddings(job_description)

    similarity_score = calculate_similarity(resume_embedding, job_description_embedding)
    # store_ats_score(user_id, resume_text, job_description, similarity_score)
    
    return similarity_score

def evaluate_resume_ats_score(user_id, resume_pdf, job_description):
    resume_text = extract_text_from_pdf(resume_pdf)
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
    ats_prompt = PromptTemplate(
        input_variables=["job_description","resume_text"],
        template="""
        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, Data Analyst, Big Data Engineering,
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
