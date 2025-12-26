"""
metrics.py
Push metrics to CloudWatch or Prometheus.
Provides latency and performance tracking for the pipeline.
"""

import os
import time
import logging
from typing import Optional

try:
    import boto3
    from botocore.exceptions import NoCredentialsError
except ImportError:
    boto3 = None  # Graceful fallback if AWS is not being used

# Logging setup
logger = logging.getLogger("metrics")
logger.setLevel(logging.INFO)

# Determine metrics backend
USE_CLOUDWATCH = os.getenv("USE_CLOUDWATCH", "false").lower() == "true"
AWS_REGION = os.getenv("AWS_REGION", "us-gov-west-1")

cloudwatch = None
if USE_CLOUDWATCH and boto3:
    try:
        cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)
    except NoCredentialsError:
        logger.warning("AWS credentials not found. CloudWatch metrics disabled.")
        cloudwatch = None

# Namespace for CloudWatch
METRICS_NAMESPACE = "Clarivox/ASR"


def log_metric(name: str, value: float, unit: str = "None"):
    """
    Log a metric value.
    
    Args:
        name: Metric name
        value: Metric value
        unit: CloudWatch unit (Milliseconds, Seconds, Count, etc.)
    """
    logger.info(f"Metric | {name}: {value} {unit}")

    if cloudwatch:
        try:
            cloudwatch.put_metric_data(
                Namespace=METRICS_NAMESPACE,
                MetricData=[
                    {
                        "MetricName": name,
                        "Value": value,
                        "Unit": unit,
                    }
                ],
            )
        except Exception as e:
            logger.error(f"Failed to push metric to CloudWatch: {e}")


def log_transcription_metrics(duration_ms: float, audio_duration_sec: float, confidence: Optional[float] = None):
    """Log transcription-related metrics."""
    log_metric("TranscriptionLatency", duration_ms, unit="Milliseconds")
    log_metric("AudioDuration", audio_duration_sec, unit="Seconds")
    if confidence is not None:
        log_metric("TranscriptionConfidence", confidence, unit="None")


def log_intent_metrics(intent_confidence: float, latency_ms: float, crisis_detected: bool = False):
    """Log intent extraction metrics."""
    log_metric("IntentConfidence", intent_confidence, unit="None")
    log_metric("IntentLatency", latency_ms, unit="Milliseconds")
    if crisis_detected:
        log_metric("CrisisDetected", 1, unit="Count")


def log_end_to_end_latency(start_time: float):
    """Log total pipeline latency."""
    total_time = (time.time() - start_time) * 1000  # ms
    log_metric("TotalPipelineLatency", total_time, unit="Milliseconds")


class MetricsLogger:
    """Class-based metrics logger for more structured usage."""
    
    def __init__(self, service_name: str, use_cloudwatch: bool = True):
        self.service_name = service_name
        self.use_cloudwatch = use_cloudwatch
        self.cloudwatch = None

        if use_cloudwatch and boto3:
            try:
                self.cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION)
            except Exception as e:
                logging.warning(f"CloudWatch setup failed: {e}")

    def log_metric(self, name: str, value: float, unit: str = "Milliseconds"):
        if not self.cloudwatch:
            logging.debug(f"[METRIC] {name}: {value} {unit}")
            return

        try:
            self.cloudwatch.put_metric_data(
                Namespace=f"Clarivox/{self.service_name}",
                MetricData=[
                    {
                        'MetricName': name,
                        'Value': value,
                        'Unit': unit
                    }
                ]
            )
        except Exception as e:
            logging.error(f"Error logging metric {name}: {e}")

    def log_latency(self, start_time: float, label: str):
        duration = (time.time() - start_time) * 1000  # ms
        self.log_metric(f"Latency_{label}", duration)
