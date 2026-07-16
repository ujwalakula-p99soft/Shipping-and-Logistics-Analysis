# 🚚 Shipping & Logistics Analysis Pipeline

A production-oriented **Incremental ELT Data Engineering Pipeline** built using **Python, Snowflake, SQL, and AWS Secrets Manager**, implementing the **Medallion Architecture (Bronze → Silver → Gold)** and **Star Schema** for logistics analytics.

The pipeline processes the **Global Superstore Dataset**, incrementally loads data into Snowflake, performs SQL-based transformations, and generates analytical reports to improve shipping efficiency.

---

# 📌 Business Problem

The logistics team wants to improve delivery efficiency by answering questions such as:

- What is the average shipping time for each shipping mode?
- Which shipments are delayed?
- Which shipping mode is most frequently used?
- Which regions experience the highest delivery delays?
- Where can logistics operations be optimized?

---

# 🏗️ Architecture

```
                +-------------------------+
                | Global Superstore CSV   |
                +-----------+-------------+
                            |
                            |
                      Python Orchestration
                            |
      -----------------------------------------------
      |               |               |             |
 Schema Validation  Data Profiling  Logging   AWS Secrets Manager
      |               |               |             |
      ----------------+---------------+-------------
                            |
                            |
                    Snowflake Internal Stage
                            |
                            |
                     COPY INTO BRONZE
                            |
                            |
                 Append Only Stream (CDC)
                            |
                            |
                         SILVER Layer
                 (Cleaning & Standardization)
                            |
                            |
                    Standard Stream (CDC)
                            |
                            |
                     MERGE INTO GOLD
                            |
           ---------------------------------
           |               |               |
      Dimensions        Fact Table       Views
                            |
                            |
                     Analytical Reports
```

---

# 🏛️ Medallion Architecture

## 🥉 Bronze Layer

- Raw data ingestion
- Stores source data with minimal modification
- Loaded using `COPY INTO`
- Append-only design
- Preserves historical raw data

---

## 🥈 Silver Layer

Responsible for data cleansing and standardization.

Operations performed:

- Remove duplicates
- Handle missing values
- Convert dates
- Standardize text values
- Data type conversion
- Business rule validation

---

## 🥇 Gold Layer

Business-ready analytical model.

Implemented using a **Star Schema**.

### Dimension Tables

- DIM_DATE
- DIM_LOCATION
- DIM_SHIP_MODE
- DIM_ORDER_PRIORITY

### Fact Table

- FACT_SHIPPING

Contains

- Shipping Duration
- Shipping Cost
- Delay Flag
- Foreign Keys to Dimensions

---

# ⭐ Star Schema

```
                    DIM_DATE
                       |
                       |
DIM_LOCATION ---- FACT_SHIPPING ---- DIM_SHIP_MODE
                       |
                       |
              DIM_ORDER_PRIORITY
```

---

# 📊 Analytical Reports

The pipeline generates the following reports:

### Average Shipping Time

- Average shipping days
- Median shipping days
- Minimum shipping days
- Maximum shipping days

---

### Shipping Mode Distribution

- Total Orders
- Order Share %
- Average Shipping Cost
- Delay Rate

---

### Delayed Orders

Displays

- Order ID
- Shipping Mode
- Region
- Shipping Duration
- Delay Status

---

### Region-wise Shipping Performance

- Total Orders
- Average Shipping Time
- Delay Rate
- Average Shipping Cost
- Regional Ranking

---

# 🔄 Incremental ELT Pipeline

Instead of reprocessing the complete dataset, the project simulates incremental data ingestion.

```
Batch_01.csv
        ↓
Bronze
        ↓
Bronze Stream
        ↓
Silver
        ↓
Silver Stream
        ↓
MERGE Gold

Batch_02.csv

↓

Only New Records Processed
```

Benefits

- Faster processing
- Reduced compute cost
- Production-style ELT workflow
- Supports Change Data Capture (CDC)

---

# ⚙️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Pipeline Orchestration |
| Pandas | Schema Validation & Data Profiling |
| Snowflake | Data Warehouse |
| SQL | Data Transformation |
| AWS Secrets Manager | Secure Credential Management |
| Boto3 | Access AWS Secrets |
| Loguru | Logging |
| Python Dotenv | Environment Configuration |

---

# 📁 Project Structure

```
shipping-logistics-analysis/

│
├── data/
│
├── logs/
│
├── sql/
│   ├── setup/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   │   ├── dimensions/
│   │   ├── facts/
│   │   └── views/
│   └── reports/
│
├── src/
│   ├── config/
│   ├── database/
│   ├── ingestion/
│   ├── pipeline/
│   ├── utils/
│   ├── validation/
│   └── main.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# 🔐 Security

Sensitive credentials are **not hardcoded**.

Snowflake credentials are securely stored in **AWS Secrets Manager** and retrieved at runtime using **Boto3**.

Environment-specific configuration is managed through `.env`.

---

# 📝 Logging

The project maintains two log files.

### application.log

Contains

- Pipeline execution
- SQL execution
- Snowflake connection
- Batch processing

---

### quality.log

Contains

- Schema validation
- Null counts
- Duplicate counts
- Data profiling summary

---

## 4 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5 Configure Environment

Create

```
.env
```

with

```
AWS_REGION=

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

SECRET_NAME=
```

---

## 6 Execute

```bash
python src/main.py
```

---

# 📈 Key Features

- Incremental ELT Pipeline
- Medallion Architecture
- Star Schema
- Snowflake Streams (CDC)
- Secure Credential Management
- SQL-based Transformations
- Production-ready Project Structure
- Data Quality Profiling
- Comprehensive Logging
- Analytical SQL Reports

---

# 📌 Future Enhancements

- Apache Airflow for Scheduling
- Snowpipe for Automatic File Ingestion
- Streamlit / Power BI Dashboard
- dbt for SQL Transformations
- Unit & Integration Testing
- CI/CD using GitHub Actions
- Docker Containerization

---

# 👨‍💻 Author

**Ujwal Akula**
