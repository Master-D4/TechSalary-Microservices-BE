-- ==========================================
-- 1. SCHEMAS
-- ==========================================
CREATE SCHEMA IF NOT EXISTS identity;
CREATE SCHEMA IF NOT EXISTS salary;
CREATE SCHEMA IF NOT EXISTS community;

-- ==========================================
-- 2. IDENTITY SCHEMA (User Management)
-- ==========================================
-- Users table: Stores credentials securely.
-- NO other service can access this table directly.
CREATE TABLE identity.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Roles table: Defines authority (e.g., USER, ADMIN).
CREATE TABLE identity.roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- User_Roles table: Many-to-Many relationship.
CREATE TABLE identity.user_roles (
    user_id INTEGER REFERENCES identity.users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES identity.roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Insert default roles
INSERT INTO identity.roles (name) VALUES ('USER'), ('ADMIN') ON CONFLICT DO NOTHING;

-- ==========================================
-- 3. SALARY SCHEMA (The Core Data)
-- ==========================================
-- Salary Submissions: The main dataset.
-- PRIVACY RULE: No user_id here to link back to identity.users (unless strictly needed for editing, but spec implies anonymity).
-- We use a "reference_id" if we need to let users delete their own, but strictly speaking, it's anonymous.
CREATE TABLE salary.salary_submissions (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    company VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL, -- e.g., "Colombo, Sri Lanka"
    salary_amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'LKR',
    years_experience INTEGER NOT NULL,

    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),

    -- Anonymity Flag: If TRUE, we hide specific company/job details in public search
    is_anonymous BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast searching by the Search Service
CREATE INDEX idx_salary_search ON salary.salary_submissions(job_title, company, location) WHERE status = 'APPROVED';

-- ==========================================
-- 4. COMMUNITY SCHEMA (Interaction)
-- ==========================================
-- Votes: Links a User (by ID) to a Salary Submission (by ID).
-- LOGICAL SEPARATION: We store IDs, but NO Foreign Key constraints enforce referential integrity
-- across schemas because in a pure microservice world, these might be separate databases.
CREATE TABLE community.votes (
    id SERIAL PRIMARY KEY,
    salary_submission_id INTEGER NOT NULL, -- Logical link to salary.salary_submissions(id)
    user_id INTEGER NOT NULL,              -- Logical link to identity.users(id)
    vote_type VARCHAR(10) CHECK (vote_type IN ('UP', 'DOWN')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraint: One user can only vote once per submission
    UNIQUE(salary_submission_id, user_id)
);

-- Reports (Optional Add-on): Users reporting fake data.
CREATE TABLE community.reports (
    id SERIAL PRIMARY KEY,
    salary_submission_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);