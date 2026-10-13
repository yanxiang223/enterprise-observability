#!/usr/bin/env python3
"""
OpenTelemetry 直报华为云示例应用

将日志、指标和追踪直接发送到华为云观测服务，无需 Collector。

Usage:
    python application.py
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any

from flask import Flask, jsonify, request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.logging import LoggingHandler
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

# 华为云签名模块
try:
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore signer import Signer
except ImportError:
    print("Warning: huaweicloudsdkcore not installed, using mock signer")

# 尝试导入华为云 OBS SDK 用于日志/指标
try:
    from obs import ObsClient as OBSClient
except ImportError:
    OBSClient = None


# ============== 配置 ==============
class Config:
    """应用配置"""

    # 华为云凭据
    ACCESS_KEY = os.environ.get('HW_ACCESS_KEY', '')
    SECRET_KEY = os.environ.get('HW_SECRET_KEY', '')
    REGION = os.environ.get('HW_REGION', 'cn-north-4')

    # 端点配置
    LTS_ENDPOINT = os.environ.get('LTS_ENDPOINT', f'lts.{REGION}.myhuaweicloud.com')
    CES_ENDPOINT = os.environ.get('CES_ENDPOINT', f'ces.{REGION}.myhuaweicloud.com')
    APM_ENDPOINT = os.environ.get('APM_ENDPOINT', f'apm.{REGION}.myhuaweicloud.com')

    # 服务配置
    SERVICE_NAME = os.environ.get('SERVICE_NAME', 'otel-huawei-demo')
    LOG_GROUP = os.environ.get('LOG_GROUP', '/otel/demo')
    METRICS_NAMESPACE = os.environ.get('METRICS_NAMESPACE', 'otel-huawei-demo')

    # Flask 配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '8000'))


# ============== 华为云签名 ==============
class HuaweiCloudSigner:
    """华为云签名工具"""

    @staticmethod
    def sign_request(method: str, url: str, headers: Dict[str, str], body: str = '') -> Dict[str, str]:
        """
        使用华为云签名算法签名请求

        注意：这是简化版本，实际生产环境应使用 huaweicloudsdkcore
        """
        # 简化的签名实现
        # 实际应使用: Signer(BasicCredentials(ak, sk)).sign(request)
        signed_headers = headers.copy()

        # 添加时间戳
        import datetime as dt
        now = dt.datetime.utcnow()
        date_str = now.strftime('%Y%m%dT%H%M%SZ')
        signed_headers['X.Sdk-Date'] = date_str

        return signed_headers


# ============== 日志客户端 ==============
class LTSClient:
    """华为云 LTS 日志客户端"""

    def __init__(self, config: Config):
        self.config = config
        self.signer = HuaweiCloudSigner()

    def send_logs(self, log_events: list) -> bool:
        """
        发送日志到 LTS

        实际实现需要调用 LTS Log Ingestion API
        """
        # 简化实现 - 实际需要调用 API
        endpoint = f"https://{self.config.LTS_ENDPOINT}/log-ingest"

        headers = {
            'Content-Type': 'application/json',
            'X-Lts-Hostname': 'otel-demo',
        }

        # 签名请求
        headers = self.signer.sign_request('POST', endpoint, headers, json.dumps(log_events))

        # 实际 API 调用
        # response = requests.post(endpoint, headers=headers, json={'logEvents': log_events})
        # return response.status_code == 200

        print(f"[LTS] Sending {len(log_events)} log events to {endpoint}")
        return True


class CESClient:
    """华为云 CES 指标客户端"""

    def __init__(self, config: Config):
        self.config = config
        self.signer = HuaweiCloudSigner()

    def send_metrics(self, metrics: list) -> bool:
        """
        发送指标到 CES

        实际实现需要调用 CES API
        """
        endpoint = f"https://{self.config.CES_ENDPOINT}/v2/{self.config.REGION}/metric-data"

        headers = {
            'Content-Type': 'application/json',
        }

        # 签名请求
        headers = self.signer.sign_request('POST', endpoint, headers, json.dumps(metrics))

        # 实际 API 调用
        # response = requests.post(endpoint, headers=headers, json={'metrics': metrics})
        # return response.status_code == 200

        print(f"[CES] Sending {len(metrics)} metrics to {endpoint}")
        return True


# ============== Flask 应用 ==============
app = Flask(__name__)
config = Config()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============== OpenTelemetry 设置 ==============
def init_telemetry():
    """初始化 OpenTelemetry"""

    # 创建资源
    resource = Resource.create({
        SERVICE_NAME: config.SERVICE_NAME,
        'hw.region': config.REGION,
    })

    # 设置追踪
    tracer_provider = TracerProvider(resource=resource)

    # 注意: 华为云 APM 使用 Agent 方式接入
    # 这里配置 OTLP 导出器 (可用于兼容的接收端)
    # 实际部署需要使用华为云 APM Agent

    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(__name__)

    # 设置指标
    # 实际使用 CES 需要适配指标格式
    # meter_provider = MeterProvider(resource=resource)
    # MeterProvider.set_global_meter_provider(meter_provider)

    return tracer


# 初始化追踪
tracer = init_telemetry()


# ============== 路由 ==============
@app.route('/')
def index():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': config.SERVICE_NAME,
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/test', methods=['POST'])
def test_api():
    """测试 API - 发送测试日志"""
    with tracer.start_as_current_span("test-api") as span:
        span.set_attribute("http.method", "POST")
        span.set_attribute("http.url", "/api/test")

        # 发送测试日志
        log_events = [{
            'timestamp': int(time.time() * 1000),
            'text': f"Test log at {datetime.utcnow().isoformat()}"
        }]

        lts_client = LTSClient(config)
        lts_client.send_logs(log_events)

        # 发送测试指标
        metrics = [{
            'metricName': 'test.metric',
            'value': 1.0,
            'timestamp': int(time.time() * 1000),
            'dimensions': [{'name': 'service', 'value': config.SERVICE_NAME}]
        }]

        ces_client = CESClient(config)
        ces_client.send_metrics(metrics)

        logger.info("Test API called")

        return jsonify({
            'status': 'ok',
            'message': 'Test data sent',
            'timestamp': datetime.utcnow().isoformat()
        })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """获取指标"""
    with tracer.start_as_current_span("get-metrics") as span:
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", "/api/metrics")

        # 返回示例指标
        metrics = {
            'namespace': config.METRICS_NAMESPACE,
            'metrics': [
                {'name': 'requests.count', 'value': 100},
                {'name': 'requests.latency', 'value': 50.5},
            ]
        }

        return jsonify(metrics)


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


# ============== 主程序 ==============
if __name__ == '__main__':
    # 检查凭据
    if not config.ACCESS_KEY or not config.SECRET_KEY:
        logger.warning("HW_ACCESS_KEY and HW_SECRET_KEY not set, using mock mode")

    logger.info(f"Starting {config.SERVICE_NAME}")
    logger.info(f"Region: {config.REGION}")
    logger.info(f"LTS Endpoint: {config.LTS_ENDPOINT}")
    logger.info(f"CES Endpoint: {config.CES_ENDPOINT}")

    app.run(host=config.HOST, port=config.PORT, debug=False)
