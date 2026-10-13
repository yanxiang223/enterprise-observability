# 企业可观测性直报方案

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 简介

本方案演示如何将 OpenTelemetry 的日志、指标和追踪直接发送到华为云观测服务，无需部署 OpenTelemetry Collector、无需 sidecar 容器。

### 什么是企业可观测性？

企业可观测性是指通过统一的方式收集、分析和展示应用的日志、指标和追踪数据，帮助运维团队实时掌握系统运行状态，快速定位问题。

### 核心功能

- **直接上报**: 使用原生 OTLP HTTP 端点发送到华为云观测服务
- **三种信号**: 支持日志 (LTS)、指标 (CES)、追踪 (APM)
- **签名认证**: 使用华为云签名算法认证请求
- **容器化部署**: 支持 CCE 集群部署
- **无 Collector**: 简化架构，降低运维成本

## 方案亮点

- 无 Collector 架构，应用直连云端观测服务
- 标准 OTLP 协议，兼容性好
- 容器化部署，支持弹性伸缩
- 华为云原生签名认证，安全可靠
- 支持日志、指标、追踪三种观测信号

## 适用场景

- **应用性能监控**: 实时掌握应用运行状态
- **故障定位**: 快速定位异常请求
- **容量规划**: 基于指标的容量分析
- **安全审计**: 日志合规与审计

## 前置条件

- 华为云账号
- IAM 用户 AK/SK（需具备 LTS、CES、APM 访问权限）
- Python 3.11+
- Docker (可选)
- CCE 集群 (可选)

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭据

设置环境变量：

```bash
export HW_ACCESS_KEY="your_access_key"
export HW_SECRET_KEY="your_secret_key"
export HW_REGION="cn-north-4"
```

### 3. 运行应用

```bash
python src/application.py
```

### 4. 测试

```bash
# 发送测试日志和指标
curl -X POST http://localhost:8000/api/test
```

## 使用方法

### 本地运行

```bash
python src/application.py
```

应用将在 http://localhost:8000 启动。

### Docker 运行

```bash
docker build -t otel-demo:latest .
docker run -p 8000:8000 \
  -e HW_ACCESS_KEY=your_ak \
  -e HW_SECRET_KEY=your_sk \
  -e HW_REGION=cn-north-4 \
  otel-demo:latest
```

### CCE 部署

```bash
# 构建镜像
docker build -t otel-demo:latest .
docker push your-registry/otel-demo:latest

# 部署到 CCE
kubectl apply -f infra/deployment.yaml
```

## 架构说明

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Flask App  │────▶│  OTLP HTTP  │────▶│  华为云    │
│  (OTel)    │     │  + SigV4    │     │  观测服务   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    ▼                          ▼                          ▼
              ┌─────────┐               ┌─────────┐               ┌─────────┐
              │   LTS   │               │   CES   │               │   APM   │
              │ (日志)  │               │  (指标)  │               │ (追踪)  │
              └─────────┘               └─────────┘               └─────────┘
```

### 组件说明

| 组件 | 说明 |
|------|------|
| Flask App | 演示应用，内置 OpenTelemetry 埋点 |
| OTLP HTTP | 标准 OTLP 协议传输 |
| SigV4 | 华为云签名算法 |
| LTS | 日志服务 (Log Tank Service) |
| CES | 云监控服务 (Cloud Eye Service) |
| APM | 应用性能监控 |

详细架构说明请参考 [docs/architecture.md](docs/architecture.md)。

## 涉及云服务

- **LTS** (日志服务) - 应用日志收集与存储
- **CES** (云监控) - 指标数据收集与展示
- **APM** (应用性能监控) - 分布式追踪
- **CCE** (云容器引擎) - 容器化部署
- **IAM** (统一身份认证) - 访问控制
- **OBS** (对象存储) - 日志归档

## 技术规格

| 指标 | 规格 |
|------|------|
| Python 版本 | 3.11+ |
| Flask 版本 | 2.0+ |
| OTel SDK 版本 | 1.0+ |
| 部署方式 | Docker / CCE |
| 认证方式 | 华为云 SigV4 签名 |

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| HW_ACCESS_KEY | 华为云 AK | - |
| HW_SECRET_KEY | 华为云 SK | - |
| HW_REGION | 区域 | cn-north-4 |
| SERVICE_NAME | 服务名称 | otel-huawei-demo |
| HOST | 监听地址 | 0.0.0.0 |
| PORT | 监听端口 | 8000 |

### 端点配置

| 变量名 | 说明 | 默认端点 |
|--------|------|----------|
| LTS_ENDPOINT | LTS 日志端点 | lts.{region}.myhuaweicloud.com |
| CES_ENDPOINT | CES 指标端点 | ces.{region}.myhuaweicloud.com |
| APM_ENDPOINT | APM 追踪端点 | apm.{region}.myhuaweicloud.com |

## 清理资源

```bash
# 删除 CCE 部署
kubectl delete -f infra/deployment.yaml

# 删除 Terraform 资源
terraform destroy
```

## 许可证

MIT No Attribution - Copyright (c) 2026 Huawei Cloud

## 联系方式

如有问题，请提交 Issue 或联系维护团队。
