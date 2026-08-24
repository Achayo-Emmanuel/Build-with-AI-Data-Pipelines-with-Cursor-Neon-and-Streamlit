Build with AI: Data Pipelines with Cursor, Neon, and Streamlit

An automated, end-to-end data pipeline built using Vibe Coding techniques with Cursor AI. This project monitors real-time AI research paper publications by fetching data from the OpenAlex API, processing and deduplicating records, storing them in a cloud-hosted Neon PostgreSQL database, and presenting interactive insights via a Streamlit web application.

Key Features
Automated Data Extraction: Fetches and parses AI research publication metadata from the OpenAlex API with built-in pagination handling.

Cloud Database & Quality Assurance: Stores processed paper metadata into a cloud Neon PostgreSQL database with robust record deduplication and automated schema/data quality checks.

Interactive Visualization Dashboard: Web-based Streamlit dashboard delivering real-time analytics, trend filtering, and research metrics.

Production-Grade Security: Environment variable management (.env) for database connections and API keys ensuring credentials remain secure.

Accelerated AI Development: Built through natural language collaboration with Cursor AI agents to achieve rapid, production-ready code delivery.


System Architecture & Workflow

┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌───────────────────┐
│   OpenAlex API  │ ──> │   Cursor AI Pipeline │ ──> │   Neon PostgreSQL    │ ──> │ Streamlit Dashboard│
│ (Research Data) │     │ (Extract & Transform)│     │  (Cloud DB Storage)  │     │  (Web Analytics)  │
└─────────────────┘     └──────────────────────┘     └──────────────────────┘     └───────────────────┘

Extraction: Daily automated fetching of hundreds of AI papers using pagination logic.

Transformation & Validation: Data cleanup, deduplication check against existing primary keys, and schema validation.

Storage: Direct ingestion into Neon PostgreSQL over secure SSL connections.

Presentation: Dynamic queries executed by the Streamlit application to render metrics, charts, and interactive filtering.

Tech Stack
AI Code Assistant / Editor: Cursor AI
Primary Language: Python 3.10+
Database: Neon PostgreSQL (Serverless Postgres)
Data Sources: OpenAlex API
Frontend / Dashboard: Streamlit
Data Manipulation: Pandas, SQLAlchemy / psycopg2
Configuration & Environment: python-dotenv

Getting Started
Prerequisites
Python 3.10 or higher

A free account on Neon for PostgreSQL database setup

Git installed on your system


Running the Project
1. Execute Data Extraction & Ingestion
Run the pipeline script to fetch latest research papers and populate the Neon DB:


2. Launch the Streamlit Dashboard
Run the web application locally:


📊 Dashboard Features
Publication Trends: Volume of research papers published over time.
Top Authors & Institutions: Breakdown of leading contributors in specific AI domains.
Keyword & Field Analytics: Filter papers by domain, subject area, and citation count.
Real-Time Data Refresh: Fetch latest metrics directly from the Neon database.
