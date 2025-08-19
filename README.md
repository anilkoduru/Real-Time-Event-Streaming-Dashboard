# 🚀 Real-Time Event Streaming Dashboard

A real-time pipeline that streams **GitHub events → Kafka → Elasticsearch → Kibana** and visualizes activity trends.  

## ⚡ Features
- Producer fetches GitHub events and pushes to Kafka  
- Consumer reads from Kafka and indexes into Elasticsearch  
- Kibana dashboards for real-time analytics  
- Fully containerized with Docker Compose  

## 🏗️ Architecture
```mermaid
flowchart LR
    A[GitHub API] --> B[Producer Service]
    B --> C[Kafka]
    C --> D[Consumer Service]
    D --> E[Elasticsearch]
    E --> F[Kibana Dashboard]
