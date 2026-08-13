# SupportPilot - Member 1 (Database & Backend Foundation)

## Project Overview

This repository contains my contribution as **Member 1** for the **SupportPilot** project.

My responsibility was to design the database foundation of the project, configure the MySQL database connection, create the SQLAlchemy ORM models, and finalize the database schema that the remaining team members would use during development.

---

# Responsibilities

As **Member 1 – DB & Backend Foundation**, I completed the following tasks:

- Designed the database schema.
- Created the Users and Tickets tables.
- Configured the MySQL database connection.
- Implemented SQLAlchemy ORM models.
- Defined relationships between database tables.
- Finalized the database schema for team integration.
- Initialized the database using SQLAlchemy.

---

# Technologies Used

- Python 3
- FastAPI
- MySQL
- SQLAlchemy ORM
- PyMySQL
- Uvicorn

---

# Database Schema

The database includes the following tables:

- Users
- Tickets
- Ticket Responses
- Activity Logs
- Escalations
- Jira Tickets
- Knowledge Base

---

# Core Database Tables

## Users

Fields:

- user_id
- name
- email
- department
- role
- created_at

---

## Tickets

Fields:

- ticket_id
- user_id
- subject
- description
- priority
- severity
- status
- created_at

---

# Database Relationships

- One User can have multiple Tickets.
- Each Ticket belongs to one User.
- Ticket Responses are linked to Tickets.
- Activity Logs are linked to Tickets.
- Escalations are linked to Tickets.
- Jira Tickets are linked to Tickets.

---

# Project Structure

```
supportpilot-member1-backend
│
├── app
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── database
│   └── Dump20260701.sql
│
├── requirements.txt
├── README.md



---


# Database Initialization

When the application starts, SQLAlchemy automatically creates the database tables from the ORM models.

---

# Deliverables

- MySQL Database Configuration
- SQLAlchemy ORM Models
- Database Schema Design
- SQL Database Export (`Dump20260701.sql`)
- Backend Foundation Initialization

---

# Member Information

**Role:** Member 1 – Database & Backend Foundation

**Responsibilities Completed:**

- Database Design
- MySQL Configuration
- SQLAlchemy ORM Models
- Database Initialization
- Schema Finalization

---

# Note

This repository contains **only the work completed by Member 1 (Database & Backend Foundation)**.

The Ticket Intake API, request validation, and ticket submission endpoints were developed as separate responsibilities by other team members.