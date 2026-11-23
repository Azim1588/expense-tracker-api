# Expense Tracker API

A RESTful backend API built with Python, FastAPI,
SQLAlchemy, and PostgreSQL.

This project is part of my Backend Engineering 101
learning journey.

## Project Overview

The Expense Tracker API allows users to create,
retrieve, update, and delete expense records.

The project demonstrates backend API development,
request validation, relational database integration,
and database migrations.

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- PostgreSQL
- Psycopg
- Alembic
- Docker

## Features

- Create expenses
- Retrieve all expenses
- Retrieve expenses by ID
- Update expenses
- Delete expenses
- Optional expense notes
- Request validation
- Persistent database storage
- Database schema migrations

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /expenses/ | Create expense |
| GET | /expenses/ | Retrieve expenses |
| GET | /expenses/{id} | Retrieve expense by ID |
| PUT | /expenses/{id} | Update expense |
| DELETE | /expenses/{id} | Delete expense |

## Backend Architecture

Client
  |
Uvicorn
  |
FastAPI
  |
Pydantic
  |
SQLAlchemy
  |
Psycopg
  |
PostgreSQL

## Implementation Practice

I document each backend feature using the workflow:

**Requirement → Logic → Code → Test**

Each feature's documentation explains:

1. What problem the feature solves.
2. What functionality is required.
3. How the implementation logic is designed.
4. How the code is implemented.
5. How the feature is tested and verified.

[View Implementation Documentation](docs/implementation/README.md)

## Learning Progress

- [x] Session 1: FastAPI Fundamentals
- [x] Session 2: PostgreSQL and SQLAlchemy
- [x] Session 3: CRUD, Transactions, and Alembic
- [ ] Independent Implementation Practice
- [ ] Session 4: Layered Backend Architecture