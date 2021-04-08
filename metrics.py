import os
import json
import yaml
from prometheus_client import core

DEFAULT_ENABLE = True,
DEFAULT_ENDPOINT = "/metrics/itself"
DEFAULT_VERSION = "1.0.0"

class MetricItem():

    def __init__(self, name, value, labels=[], desc="", **kwargs):
        if not value:
            raise ValueError('No value specified for {}:{}'.format(self.__class__, name))

        '''
        format and lowercase name, labels and value to be consumered by Prometheus
        '''
        self.name = name
        self.value = value
        self.labels = labels
        self.description = desc
    
    def __repr__(self):
        return ",".join(["{}={}".format(key, value) for key, value in self.__dict__.items()])

    def get_prometheus_metric(self):
        return core.GaugeMetricFamily(self.name, self.description, None, self.labels)
    
    def load_value(self, columns, one_result):
        _index_list = [columns.index(label) for label in self.labels]

        if isinstance(self.value, (int, float)):
            metric_value = self.value
        else:
            _metric_index = columns.index(self.value)
            metric_value = one_result[_metric_index]
        
        metric_labels = ["{}".format(one_result[index]) for index in _index_list]

        return metric_value, metric_labels


class QueryConfigItem():
    def __init__(self, query="", json=False, **kwargs):
        self.query = query
        self.isJson = json
        self.metrics = self.load_metric_list(kwargs.get("metrics"))
    
    def load_metric_list(self, metric_string_list):
        return [MetricItem(**metric) for metric in metric_string_list]

    def add_metric(self, metric):
        self.metrics.append(metric)

    def __repr__(self):
        return ",".join(["{}='{}'".format(key, value) for key, value in self.__dict__.items()])
    
    def load_metrics(self, raw_response, columns):
        metricFamilies = [metric.get_prometheus_metric() for metric in self.metrics]

        for one_result in raw_response:
            metric_list_key = ("value", "labels")
            metric_list = [
                dict( zip(metric_list_key, metricItem.load_value(columns, one_result)) )
                for metricItem in self.metrics
            ]
            
            assert len(metricFamilies) == len(metric_list)

            for index, metric in enumerate(metric_list):
                metricFamilies[index].add_metric(metric["labels"], metric["value"])
        return metricFamilies

class QueryConfig:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.enable = kwargs.get("enable", None)
        self.endpoint = kwargs.get("endpoint", DEFAULT_ENDPOINT)
        self.queryConfigItems = self.load_config_list(kwargs.get("queryConfigs"))
    
    def load_config_list(self, config_string_list):
        return [QueryConfigItem(**config) for config in config_string_list]

    def __repr__(self):
        class_str_format = "{class_name}:{attr_list}"
        return class_str_format.format(
            class_name = self.__class__,
            attr_list = ",".join(["{}='{}'".format(key, value) for key, value in self.__dict__.items()])
        )

    @staticmethod
    def make_object(cls, **kwargs):
        return cls(**kwargs)

    def add_config_item(self, configItem):
        self.queryConfigItems.append(configItem)


def load_metric_yaml_config(filename):
    with open(filename, "r") as f:
        data = yaml.full_load(f)
    
    return QueryConfig.make_object(QueryConfig, **data)

def load_metric_config_filename(filename):
    # check if the file exists
    if not os.path.exists(filename):
        return None
    
    queryConfig = None
    if filename.endswith(".yaml"):
        queryConfig = load_metric_yaml_config(filename)
    elif filename.endswith(".json"):
        # load_metric_json_config(filename)
        pass
    else:
        # do not support this file type
        pass

    return queryConfig
    
if __name__ == "__main__":
    filename = os.path.abspath(__file__)
    filedir = os.path.dirname(filename)
    config_filename = os.path.join(filedir, "config", "config.yaml")
    print("config_filename: {}".format(config_filename))

    load_metric_config_filename(config_filename)

