# 架构对比: AWS vs 华为云

> 本文件记录 AWS 原架构与华为云适配架构的对比，仅供内部参考，不对外发布。

## 组件对比

| 组件 | AWS 版本 | 华为云版本 | 差异 |
|------|----------|-----------|------|
| 日志 | CloudWatch Logs | LTS | API 格式略有不同 |
| 指标 | CloudWatch Metrics | CES | 命名空间概念不同 |
| 追踪 | X-Ray | APM | Agent 接入方式 |
| 部署 | Elastic Beanstalk | CCE | 容器化部署 |

## 详细差异

### 日志服务

| 特性 | AWS CloudWatch Logs | 华为云 LTS |
|------|---------------------|-------------|
| 协议 | OTLP HTTP | OTLP HTTP |
| 认证 | SigV4 | HMAC-SHA256 |
| 端点 | logs.{region}.amazonaws.com | logs.{region}.myhuaweicloud.com |

### 指标服务

| 特性 | AWS CloudWatch Metrics | 华为云 CES |
|------|------------------------|------------|
| 协议 | OTLP HTTP | OTLP HTTP |
| 认证 | SigV4 | HMAC-SHA256 |
| 命名空间 | AWS/Namespace | 自定义命名空间 |

### 追踪服务

| 特性 | AWS X-Ray | 华为云 APM |
|------|-----------|-------------|
| 协议 | OTLP HTTP | OTLP HTTP / Agent |
| 认证 | SigV4 | HMAC-SHA256 |
| 接入方式 | OTLP Exporter | Agent / OTLP |

### 部署平台

| 特性 | AWS Elastic Beanstalk | 华为云 CCE |
|------|----------------------|-------------|
| 类型 | PaaS 托管 | CaaS 容器 |
| 部署方式 | 平台自动管理 | Kubernetes |
| 扩展性 | 自动扩展 | 手动配置 |
