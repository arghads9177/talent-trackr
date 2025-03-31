-- TalentTrackr Database Schema

CREATE DATABASE IF NOT EXISTS talenttrackr;
USE talenttrackr;

-- Users Table (Admin / Recruiters / Applicants)
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    resume_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    resume_path VARCHAR(255) NOT NULL,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Job Descriptions Table
CREATE TABLE IF NOT EXISTS job_descriptions (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    job_title VARCHAR(100),
    job_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ATS Score Table
CREATE TABLE IF NOT EXISTS ats_scores (
    score_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    resume_id INT,
    job_id INT,
    ats_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id),
    FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id)
);
