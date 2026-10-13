# 服务映射: sample-otel-cloudwatch-no-collector

## AWS → 华为云 服务映射表

| # | AWS 服务 | 华为云对标 | 对齐度 | 映射说明 |
|---|----------|-----------|--------|----------|
| 1 | CloudWatch Logs | LTS (Log Tank Service) | 🟢 完全对标 | 日志存储服务，功能对等 |
| 2 | CloudWatch Metrics | CES (Cloud Eye) | 🟢 完全对标 | 指标监控服务，功能对等 |
| 3 | AWS X-Ray | APM (Application Performance Management) | 🟢 完全对标 | 分布式追踪，性能监控 |
| 4 | Elastic Beanstalk | CCE / ECS | 🟡 部分对标 | 容器编排/应用托管 |
| 5 | IAM | IAM | 🟢 完全对标 | 身份认证与授权 |

## 详细说明

### 1. CloudWatch Logs → LTS 🟢 完全对标

**映射**:
- Python: 使用华为云 LTS SDK 或 HTTP API
- 端点: `logs.{region}.myhuaweicloud.com`

**兼容层**:
- OBS 兼容 S3 协议，但日志服务使用专属 API
- 需要使用华为云 Log Tank Service API

### 2. CloudWatch Metrics → CES 🟢 完全对标

**映射**:
- Python: 使用华为云 CES SDK
- 指标命名空间: 自定义命名空间

**对齐度**:
- CES 支持自定义指标上报
- 支持维度 (Dimensions)
- 支持统计周期设置

### 3. X-Ray → APM 🟢 完全对标

**映射**:
- Python: 使用华为云 APM SDK (Java Agent / Node.js Agent)
- 注意: APM 主要使用 Agent 方式接入，与 X-Ray 方式略有不同

**对齐度**:
- APM 支持分布式追踪
- 支持性能监控
- 需要使用华为云 APM Agent

### 4. Elastic Beanstalk → CCE/ECS 🟡 部分对标

**映射**:
- CCE: Kubernetes 容器编排
- ECS: 弹性容器服务（即将上线）

**替代方案**:
| 方案 | 说明 | 复杂度 |
|------|------|--------|
| CCE + Nginx Ingress | Kubernetes 部署 | 中 |
| ECS + ELB | 容器 + 负载均衡 | 低 |

### 5. IAM → IAM 🟢 完全对标

**映射**:
- 使用华为云 IAM 服务
- 创建委托并授予相应权限

## 关键适配点

### OpenTelemetry 适配

原架构使用 OTLP HTTP Exporter 直连 CloudWatch:

```
Flask App → OTLP HTTP + SigV4 → CloudWatch
```

华为云适配:

```
Flask App → OTLP HTTP + Huawei Cloud Sig → LTS/CES/APM
```

### 需要修改的代码

1. **SigV4 签名**: 改为华为云签名算法
2. **端点 URL**: 改为华为云 API 端点
3. **指标格式**: CES 指标格式略有不同
4. **追踪接入**: APM 使用 Agent 方式，与 OTel 集成方式不同

## 风险评估

### 🟡 黄色风险 (1 项)

| 风险 | 说明 | 影响 |
|------|------|------|
| APM Agent 接入方式 | APM 主要使用 Agent 方式，OTel 集成需要额外配置 | 需要适配 |

### 架构变更

- Elastic Beanstalk → CCE/ECS (容器化部署)
- OTel Collector → 直接上报 (保持不变)
- SigV4 签名 → 华为云签名算法
