#!/usr/bin/python

import requests
import time
import os
from sonarqube import SonarCloudClient
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# SonarQube API endpoint
#SONARQUBE_API_ENDPOINT = 'http://localhost:9000/api/measures/component?component=sam-alpha-uno&metricKeys=coverage&additionalFields=metrics'
SONARCLOUD_URL = 'http://localhost:9000/'
# SonarQube Token
#SONARQUBE_TOKEN = "sqp_d1c95b943ec072c25906eb4432047eb541e0384f"
SONARCLOUD_TOKEN = "squ_c06649c70def5a44e8aceb52f5d9de999fec5dac"

# Prometheus Pushgateway endpoint
PROMETHEUS_PUSHGATEWAY_ENDPOINT = 'http://localhost:9091'

# Metric to collect from SonarQube
SONARQUBE_METRIC = 'coverage'

# Component key in SonarQube
SONARQUBE_COMPONENT_KEY = 'sam-alpha-uno'

# Prometheus metric name
PROMETHEUS_METRIC_NAME = 'sam_alpha_uno_coverage'

# Main function
def main():
    while True:
        # Get the metric value from SonarQube
        sonarqube_metric_value = get_sonarqube_metric_value(SONARQUBE_METRIC, SONARQUBE_COMPONENT_KEY)
        print('SQ-metric-value :', sonarqube_metric_value)
        # Push the metric to Prometheus Pushgateway
        push_to_prometheus_pushgateway(PROMETHEUS_METRIC_NAME, sonarqube_metric_value)

        # Wait for 5 minutes before collecting the metric again
        time.sleep(300)

# Function to get the metric value from SonarQube
def get_sonarqube_metric_value(metric, component_key):
    # Make the API request to SonarQube
    #sonarqube_api_url = SONARQUBE_API_ENDPOINT.format(component=component_key, metric=metric)
    #response = requests.get(sonarqube_api_url, auth=('<user-name>', '<password>'))
    # Parse the API response and get the metric value
    #response_json = response.json()
    #metric_value = response_json['component']['measures'][0]['value']
    sonar = SonarCloudClient(sonarcloud_url=SONARCLOUD_URL,token=SONARCLOUD_TOKEN)
    component = sonar.measures.get_component_with_specified_measures(component=SONARQUBE_COMPONENT_KEY,fields="metrics,periods",metricKeys="coverage")
    measures = component['component']['measures']

    for metric_data in measures:
        print(metric_data['metric'])
        if metric_data['metric'] == 'coverage':
            metric_value = metric_data['value']
            break
    print('metric_value : ', metric_value)
    return metric_value

# Function to push the metric to Prometheus Pushgateway
def push_to_prometheus_pushgateway(metric_name, metric_value):
    # Create a Prometheus Gauge metric
    registry = CollectorRegistry()
    gauge_metric = Gauge(metric_name, 'Sam Alpha UNO project Coverage', registry=registry)

    # Set the metric value
    gauge_metric.set(metric_value)

    # Push the metric to the Pushgateway
    push_to_gateway(PROMETHEUS_PUSHGATEWAY_ENDPOINT, job='sam_uno_job', registry=registry)

if __name__ == '__main__':
    main()
