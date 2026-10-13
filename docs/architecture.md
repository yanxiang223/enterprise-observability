# 架构说明: OpenTelemetry 直报华为云方案

## 1. 方案概述

本解决方案演示如何将 OpenTelemetry 的日志、指标和追踪直接发送到华为云观测服务，无需 OpenTelemetry Collector、无需 sidecar 容器。

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        应用层                                    │
│                                                                 │
│  ┌──────────────┐    ┌────────────────┐    ┌───────────────┐  │
│  │ Flask 应用   │───>│ OpenTelemetry  │───>│ 华为云签名   │  │
│  │              │    │ SDK            │    │ (HMAC-SHA256) │  │
│  └──────────────┘    └────────────────┘    └───────┬───────┘  │
│                                                      │          │
└──────────────────────────────────────────────────────┼──────────┘
                                                       │
        ┌─────────────────────┬───────────────────────┘
        │                     │
        ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   LTS         │    │    CES        │    │    APM        │
│ (日志服务)    │    │   (云监控)    │    │  (性能监控)   │
│               │    │               │    │               │
│ /otel/logs   │    │ namespace     │    │ traces        │
└───────────────┘    └───────────────┘    └───────────────┘
```

### 2.2 核心组件

| 组件 | 说明 |
|------|------|
| **Flask 应用** | Web 服务，提供 API 端点 |
| **OpenTelemetry SDK** | 采集日志、指标、追踪数据 |
| **华为云签名** | 使用 HMAC-SHA256 算法签名请求 |
| **LTS** | 日志存储服务 |
| **CES** | 指标监控服务 |
| **APM** | 应用性能监控服务 |

## 3. 数据流程

### 3.1 日志流程

```
Flask Request
     │
     ▼
OpenTelemetry Logger
     │
     ▼
OTLP HTTP Exporter
     │
     ▼
华为云签名 (HMAC-SHA256)
     │
     ▼
LTS API (/log ingest)
```

### 3.2 指标流程

```
OpenTelemetry Metrics SDK
     │
     ▼
OTLP HTTP Exporter
     │
     ▼
华为云签名
     │
     ▼
CES API (/metric-data)
```

### 3.3 追踪流程

```
OpenTelemetry Tracer
     │
     ▼
OTLP HTTP Exporter
     │
     ▼
华为云签名
     │
     ▼
APM Agent / API
```

## 4. 技术细节

### 4.1 华为云签名算法

```python
import hmac
import hashlib
import base64

def sign(secret_key, string_to_sign):
    signature = hmac.new(
        secret_key.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')
```

### 4.2 端点配置

| 服务 | 端点格式 |
|------|----------|
| LTS | `https://logs.{region}.myhuaweicloud.com` |
| CES | `https://ces.{region}.myhuaweicloud.com` |
| APM | `https://apm.{region}.myhuaweicloud.com` |

### 4.3 容器化部署

使用 CCE 部署:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: otel-demo
  template:
    metadata:
      labels:
        app: otel-demo
    spec:
      containers:
      - name: app
        image: otel-demo:latest
        ports:
        - containerPort: 8000
```

## 5. 限制说明

- APM 主要使用 Agent 方式，OTel 集成需要额外配置
- CES 指标格式需要适配
- LTS 日志摄入需要使用特定 API
