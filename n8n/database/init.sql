-- =====================================
-- AI Business Assistant Database
-- =====================================

CREATE TABLE workflow_state (
    workflow_name VARCHAR(100) PRIMARY KEY,
    last_processed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workflow_execution (
    id SERIAL PRIMARY KEY,

    workflow_name VARCHAR(100) NOT NULL,

    started_at TIMESTAMP,

    finished_at TIMESTAMP,

    status VARCHAR(20),

    processed_count INT DEFAULT 0,

    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_log (
    id SERIAL PRIMARY KEY,

    gmail_message_id VARCHAR(255) UNIQUE,

    thread_id VARCHAR(255),

    sender VARCHAR(255),

    subject TEXT,

    category VARCHAR(50),

    priority VARCHAR(20),

    action_required BOOLEAN DEFAULT FALSE,

    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO workflow_state
(
    workflow_name,
    last_processed_at
)
VALUES
(
    'gmail_assistant',
    NOW() - INTERVAL '1 day'
);