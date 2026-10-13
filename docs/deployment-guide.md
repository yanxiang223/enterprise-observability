# 部署指导书: OpenTelemetry 直报华为云方案

## 1. 前置条件

### 1.1 华为云账号

- 已注册华为云账号
- 已完成实名认证

### 1.2 环境要求

| 要求 | 说明 |
|------|------|
| Python | 3.11 或更高版本 |
| Docker | 用于构建容器镜像 |
| kubectl | 用于部署到 CCE |
| helm | 用于包管理 |

### 1.3 必需的华为云资源

| 资源 | 说明 |
|------|------|
| CCE 集群 | 容器化部署 |
| LTS 日志组 | 日志存储 |
| CES 指标命名空间 | 指标存储 |
| APM 应用 | 追踪监控 |
| IAM 委托 | 授予观测服务权限 |

## 2. 资源创建

### 2.1 创建 CCE 集群

通过控制台或 Terraform 创建 CCE 集群:

```bash
# Terraform 方式 (infra/main.tf)
resource "huaweicloud_cce_cluster" "cluster" {
  name        = "otel-cluster"
  flavor_id   = "cce.s1.small"
  vpc_id      = huaweicloud_vpc.vpc.id
  subnet_id   = huaweicloud_vpc_subnet.subnet.id
}
```

### 2.2 配置 IAM 委托

创建委托并授予以下权限:
- LTS: 日志摄入权限
- CES: 指标上报权限
- APM: 追踪数据权限

### 2.3 创建 LTS 日志组

```bash
# 使用 API 创建日志组
huaweicloud_lts_group "demo" {
  group_name  = "otel-demo"
  ttl_in_days = 7
}
```

## 3. 环境配置

### 3.1 安装依赖

```bash
pip install -r requirements.txt
```

### 3.2 配置凭据

设置华为云访问凭据 (选择一种):

**方式 1: 环境变量**
```bash
export HW_ACCESS_KEY="your_access_key"
export HW_SECRET_KEY="your_secret_key"
export HW_REGION="cn-north-4"
```

**方式 2: 配置文件**
```bash
# ~/.huaweicloud/config
[default]
access_key = your_access_key
secret_key = your_secret_key
region = cn-north-4
```

## 4. 使用方法

### 4.1 本地运行

```bash
python application.py
```

### 4.2 Docker 构建

```bash
docker build -t otel-demo:latest .
docker run -p 8000:8000 \
  -e HW_ACCESS_KEY=your_ak \
  -e HW_SECRET_KEY=your_sk \
  -e HW_REGION=cn-north-4 \
  otel-demo:latest
```

### 4.3 CCE 部署

```bash
# 构建并推送镜像
docker build -t otel-demo:latest .
docker push your-registry/otel-demo:latest

# 部署到 CCE
kubectl apply -f deployment.yaml
```

## 5. 验证

### 5.1 API 验证

```bash
# 测试应用是否正常运行
curl http://localhost:8000/

# 测试日志上报
curl -X POST http://localhost:8000/api/test

# 测试指标上报
curl http://localhost:8000/api/metrics
```

### 5.2 控制台验证

1. 登录华为云控制台
2. 检查 LTS 日志组是否有日志
3. 检查 CES 是否有指标数据
4. 检查 APM 是否有追踪数据

## 6. 配置说明

### 6.1 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| HW_ACCESS_KEY | 访问密钥 AK | - |
| HW_SECRET_KEY | 访问密钥 SK | - |
| HW_REGION | 区域 | cn-north-4 |
| LTS_ENDPOINT | LTS 端点 | logs.{region}.myhuaweicloud.com |
| CES_ENDPOINT | CES 端点 | ces.{region}.myhuaweicloud.com |
| APM_ENDPOINT | APM 端点 | apm.{region}.myhuaweicloud.com |

### 6.2 日志配置

日志发送到 LTS 的日志组: `/otel/demo`

### 6.3 指标配置

CES 指标命名空间: `otel-huawei-demo`

## 7. 故障排除

### 7.1 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 403 Forbidden | IAM 权限不足 | 检查委托策略 |
| 404 Not Found | 端点错误 | 检查区域配置 |
| Connection Timeout | 网络问题 | 检查安全组规则 |

### 7.2 日志调试

启用调试日志:

```bash
export OTEL_PYTHON_LOG_LEVEL=DEBUG
python application.py
```

## 8. 清理资源

### 8.1 删除 CCE 资源

```bash
kubectl delete -f deployment.yaml
```

### 8.2 删除观测服务数据

```bash
# 删除 LTS 日志组
# 通过控制台删除

# 删除 CES 指标
# 通过控制台删除

# 删除 APM 应用
# 通过控制台删除
```
