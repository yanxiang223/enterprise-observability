# Enterprise Observability Direct Reporting Solution

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

This solution demonstrates how to send OpenTelemetry logs, metrics, and traces directly to Huawei Cloud observability services without deploying OpenTelemetry Collector or sidecar containers.

### What is Enterprise Observability?

Enterprise observability refers to the unified collection, analysis, and visualization of application logs, metrics, and traces, enabling operations teams to monitor system health in real-time and quickly diagnose issues.

### Core Features

- **Direct Reporting**: Send data directly to Huawei Cloud via native OTLP HTTP endpoints
- **Three Signals**: Support for Logs (LTS), Metrics (CES), and Traces (APM)
- **Signed Authentication**: Authenticate requests using Huawei Cloud signature algorithm
- **Containerized Deployment**: Support CCE cluster deployment
- **No Collector**: Simplified architecture, reduced operational overhead

## Key Highlights

- No Collector architecture - applications connect directly to cloud services
- Standard OTLP protocol - excellent compatibility
- Containerized deployment with elastic scaling
- Native Huawei Cloud signature authentication
- Supports logs, metrics, and traces

## Use Cases

- **Application Performance Monitoring**: Real-time application health monitoring
- **Fault Diagnosis**: Quickly locate anomalous requests
- **Capacity Planning**: Metric-based capacity analysis
- **Security Audit**: Log compliance and auditing

## Prerequisites

- Huawei Cloud account
- IAM user AK/SK (with LTS, CES, APM access permissions)
- Python 3.11+
- Docker (optional)
- CCE cluster (optional)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Set environment variables:

```bash
export HW_ACCESS_KEY="your_access_key"
export HW_SECRET_KEY="your_secret_key"
export HW_REGION="cn-north-4"
```

### 3. Run Application

```bash
python src/application.py
```

### 4. Test

```bash
# Send test logs and metrics
curl -X POST http://localhost:8000/api/test
```

## Usage

### Local Run

```bash
python src/application.py
```

The application will start at http://localhost:8000.

### Docker Run

```bash
docker build -t otel-demo:latest .
docker run -p 8000:8000 \
  -e HW_ACCESS_KEY=your_ak \
  -e HW_SECRET_KEY=your_sk \
  -e HW_REGION=cn-north-4 \
  otel-demo:latest
```

### CCE Deployment

```bash
# Build image
docker build -t otel-demo:latest .
docker push your-registry/otel-demo:latest

# Deploy to CCE
kubectl apply -f infra/deployment.yaml
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Flask App  │────▶│  OTLP HTTP  │────▶│  Huawei    │
│  (OTel)    │     │  + SigV4    │     │  Cloud      │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    ▼                          ▼                          ▼
              ┌─────────┐               ┌─────────┐               ┌─────────┐
              │   LTS   │               │   CES   │               │   APM   │
              │ (Logs)  │               │(Metrics)│               │(Traces) │
              └─────────┘               └─────────┘               └─────────┘
```

### Components

| Component | Description |
|-----------|-------------|
| Flask App | Demo application with OpenTelemetry instrumentation |
| OTLP HTTP | Standard OTLP protocol transport |
| SigV4 | Huawei Cloud signature algorithm |
| LTS | Log Tank Service |
| CES | Cloud Eye Service |
| APM | Application Performance Management |

See [docs/architecture.md](docs/architecture.md) for detailed architecture.

## Involved Cloud Services

- **LTS** (Log Tank Service) - Application log collection and storage
- **CES** (Cloud Eye Service) - Metric data collection and visualization
- **APM** (Application Performance Management) - Distributed tracing
- **CCE** (Cloud Container Engine) - Containerized deployment
- **IAM** (Identity and Access Management) - Access control
- **OBS** (Object Storage Service) - Log archiving

## Technical Specifications

| Specification | Value |
|--------------|-------|
| Python Version | 3.11+ |
| Flask Version | 2.0+ |
| OTel SDK Version | 1.0+ |
| Deployment | Docker / CCE |
| Authentication | Huawei Cloud SigV4 Signature |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| HW_ACCESS_KEY | Huawei Cloud AK | - |
| HW_SECRET_KEY | Huawei Cloud SK | - |
| HW_REGION | Region | cn-north-4 |
| SERVICE_NAME | Service name | otel-huawei-demo |
| HOST | Listen address | 0.0.0.0 |
| PORT | Listen port | 8000 |

### Endpoint Configuration

| Variable | Description | Default Endpoint |
|----------|-------------|-----------------|
| LTS_ENDPOINT | LTS log endpoint | lts.{region}.myhuaweicloud.com |
| CES_ENDPOINT | CES metrics endpoint | ces.{region}.myhuaweicloud.com |
| APM_ENDPOINT | APM traces endpoint | apm.{region}.myhuaweicloud.com |

## Cleanup

```bash
# Remove CCE deployment
kubectl delete -f infra/deployment.yaml

# Remove Terraform resources
terraform destroy
```

## License

MIT No Attribution - Copyright (c) 2026 Huawei Cloud

## Contact

For issues, please submit an Issue or contact the maintenance team.
