# Real-Time Stock Data Pipeline

---

## ![Real-Time Stock Data Pipeline Diagram](/Project_Structure.PNG)

---

## Project Overview

This project demonstrates a **Real-Time Stock Data Pipeline** designed to collect, process, and analyze stock data in near real-time. The architecture integrates **Apache Airflow**, **Snowflake**, **Amazon S3**, and **Power BI** to ensure seamless data flow from extraction to visualization.

---

## Pipeline Stages

### Data Extraction

- The pipeline initiates with **Apache Airflow**, which orchestrates the flow.
- **Data** is extracted from the **Twelve Data API**, providing reliable real-time stock data.

### Data Transformation and Loading

- Extracted data is transformed with **Python** and loaded into **Amazon S3** for intermediate storage.

### Data Integration

- Using **Snowflake's External Stage**, the data in S3 is accessed and loaded into **Snowflake tables**.
- This stage prepares the data for efficient querying and storage.

### Data Visualization

- **Power BI** is used for data visualization, creating interactive dashboards that provide real-time insights into stock trends and metrics.

---

## Key Technologies Used

- **Apache Airflow**: Orchestration of pipeline stages
- **Twelve Data API**: Real-time stock data extraction
- **Python**: Data transformation
- **Amazon S3**: Intermediate storage
- **Snowflake**: Data integration and querying
- **Power BI**: Data visualization and dashboarding
