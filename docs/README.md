# 🧬 Telecom Churn Data Pipeline

This project orchestrates and visualizes automated KNIME workflows using **Apache Airflow**, **Docker**, and **Metabase**.

---

## 📦 Overview

### 🔧 Technologies Used
- **Apache Airflow** (`CeleryExecutor`) – Workflow scheduling
- **KNIME** – Workflow execution in batch mode
- **PostgreSQL** – Metadata database for Airflow
- **Redis** – Broker for Celery
- **Metabase** – Data visualization dashboard
- **Docker Compose** – Multi-service orchestration

---

## 📁 Project Structure

.
├── dags/ # Airflow DAGs (including KNIME scheduler)
├── config/ # Airflow config files
├── plugins/ # Airflow plugins (optional)
├── logs/ # Airflow logs (auto-generated)
├── Dockerfile.airflow # Dockerfile for custom Airflow image
├── Dockerfile.knime # Dockerfile for KNIME batch image
├── docker-compose.yaml # Multi-container setup
├── knime/ # Folder with KNIME workflows
│ └── HG_Insights_project/ # Specific KNIME project
├── knime_workspace/ # Temporary KNIME workspace for execution
└── README.md


---

## 🚀 Getting Started

### 1. ✅ Prerequisites
- Docker Desktop (WSL2 backend recommended)
- Python 3.8+ (optional, for local DAG development)
- Ensure `D:` drive is shared in Docker Desktop settings (for volume mounts)

---

### 2. 🧰 Environment Setup

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   
Start all services:

docker-compose up --build

Access services:
Airflow Web UI: http://localhost:8080

Metabase: http://localhost:3000

⚙️ Airflow Setup
DAG: knime_hourly_pipeline
This DAG runs the KNIME workflow from the knime/HG_Insights_project directory every hour (or on a schedule defined by Airflow Variables).

Features:
Executes KNIME using batch mode and xvfb-run

Mounts workflow and workspace as volumes

Customizable schedule via Airflow Variable: knime_feed_interval

Modify DAG schedule:
Update or create the variable in Airflow UI:

Key: knime_feed_interval

Value: @hourly (or cron-style)

🐳 Docker Services Overview
Service	Description	Ports
airflow-webserver	Airflow web UI	8081
airflow-scheduler	Airflow DAG scheduler	Internal
airflow-worker	Celery worker for Airflow tasks	Internal
airflow-apiserver	Airflow REST API server	8080
airflow-init	Initializes DB and creates admin user	-
postgres	PostgreSQL DB for Airflow metadata	5432 (int.)
redis	Redis queue backend	6379 (int.)
knime	Container for running KNIME workflows	-
metabase	Business Intelligence dashboard	3000

🧪 Testing KNIME Container
Run the KNIME container independently for testing:


docker-compose run knime

📈 Metabase
After setup, Metabase is available at http://localhost:3000. You can connect it to the same PostgreSQL database (report_db) used by Airflow or to any other data sources your KNIME workflows produce.

🔐 Security Notes
Default Airflow credentials: airflow / airflow

Secrets like FERNET_KEY and JWT should be rotated in production

PostgreSQL password (root@123) is hardcoded and should be updated securely

🧹 Cleanup
To stop and remove containers:

docker-compose down -v
