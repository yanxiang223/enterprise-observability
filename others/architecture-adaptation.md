# 架构适配与降级决策: sample-otel-cloudwatch-no-collector

## 架构模式识别

该解决方案采用 **OpenTelemetry 直接上报** 架构:

```
Flask App (OTel SDK) → OTLP HTTP + SigV4 → CloudWatch (Logs/Metrics/Traces)
```

### 核心组件
1. **Flask 应用**: Web 服务
2. **OpenTelemetry SDK**: 日志、指标、追踪采集
3. **SigV4 认证**: AWS IAM 凭据签名
4. **CloudWatch**: 日志/指标/追踪存储

## 阶段 2.5: 止损检查

### 🔴 无对标服务

**无**: 所有 AWS 服务在华为云均有对标产品。

### 🟡 部分对标服务

| AWS 服务 | 华为云 | 对齐度 | 说明 |
|----------|--------|--------|------|
| Elastic Beanstalk | CCE/ECS | 🟡 | 需要容器化部署 |
| X-Ray | APM | 🟢 | Agent 接入方式略有不同 |

## 降级方案

### 方案 A: CCE 部署 (推荐)

**架构**:
```
Flask App (OTel) → OTLP HTTP + Huawei Sig → CES/LTS/APM
                                   ↓
                              CCE 容器
```

**优点**:
- Kubernetes 标准化部署
- 弹性伸缩
- 易于运维

**缺点**:
- 需要容器化改造

### 方案 B: ECS 部署

**架构**:
```
Flask App (OTel) → OTLP HTTP + Huawei Sig → CES/LTS/APM
                                   ↓
                              ECS 容器 + ELB
```

**优点**:
- 简单易用
- 与 Elastic Beanstalk 概念接近

**缺点**:
- 即将上线，需等待

## 架构变更

### 原架构 (AWS)

```
┌──────────────┐    ┌────────────────┐    ┌─────────────────┐
│ Flask App    │───>│ OTel SDK      │───>│ CloudWatch     │
│ + OTel       │    │ + SigV4       │    │ Logs/Metrics/  │
│              │    │                │    │ X-Ray          │
└──────────────┘    └────────────────┘    └─────────────────┘
         │                                      ▲
         │          Elastic Beanstalk            │
         └──────────────────────────────────────┘
```

### 适配后架构 (华为云)

```
┌──────────────┐    ┌────────────────┐    ┌─────────────────┐
│ Flask App    │───>│ OTel SDK      │───>│ CES/LTS/APM    │
│ + OTel       │    │ + Huawei Sig  │    │                 │
│              │    │                │    │                 │
└──────────────┘    └────────────────┘    └─────────────────┘
         │                                      ▲
         │                CCE/ECS                │
         └──────────────────────────────────────┘
```

### 关键变更点

1. **部署平台**: Elastic Beanstalk → CCE
2. **签名算法**: AWS SigV4 → 华为云签名算法
3. **日志端点**: CloudWatch Logs → LTS
4. **指标端点**: CloudWatch Metrics → CES
5. **追踪端点**: X-Ray → APM

## 决策记录

| 日期 | 决策 | 说明 |
|------|------|------|
| 2026-08-24 | 方案A | 用户选择 CCE 部署方案 |
