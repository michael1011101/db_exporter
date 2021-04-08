from prometheus_client import CollectorRegistry
from prometheus_client.metrics import Gauge, Counter

baseRegistry = CollectorRegistry()

metric_usage = Gauge("metrics_usage", "Description of guage", registry=baseRegistry)
metric_usage.set(93.52)

alphaRegistry = CollectorRegistry()

metric_total = Gauge("metric_total", "metric_usage of total", registry=alphaRegistry)
metric_total.set(88.62)

metric_count = Counter("metric_count", "Description of metric_count", registry=alphaRegistry)
metric_count.inc() 
