#!/usr/bin/python
import requests
import influxdb
import time
import csv
import os
from sonarqube import SonarCloudClient
from influxdb import InfluxDBClient

# SonarQube API endpoints
SONARCLOUD_URL = 'http://localhost:9000/'

# SonarQube Token
SONARCLOUD_TOKEN = "squ_c06649c70def5a44e8aceb52f5d9de999fec5dac"

# Metric to collect from SonarQube
SONARQUBE_METRIC = 'code_smells'

# Component key in SonarQube
SONARQUBE_COMPONENT_KEY = 'sam-alpha-uno'

# Prometheus metric name
PROMETHEUS_METRIC_NAME = 'code_smells'

# Main function
def main():
    while True:
        # Get the metric value from SonarQube
        sonarqube_metric_value = get_sonarqube_metric_value(SONARQUBE_METRIC, SONARQUBE_COMPONENT_KEY)
        print('SQ-metric-value :', sonarqube_metric_value)
        # Push data to influx db

        # Wait for 5 minutes before collecting the metric again
        time.sleep(300)

def push_to_influxdb(data):
    json_body = []
    client = InfluxDBClient(host='localhost', port=8086, username='murali',password='password123', database='test_data')
    for row in data:
        json_body=[{
            "measurement": "code_smells",
            "tags":{"tag1":row[0],"tag2":row[1]},
            "time":row[2],
            "fields":{
                "field1": float(row[3]),
                "field2": float(row[4])
            }
        }]

    client.write_points(json_body)

# Function to get the metric value from SonarQube
def get_sonarqube_metric_value(metric, component_key):
    sonar = SonarCloudClient(sonarcloud_url=SONARCLOUD_URL,token=SONARCLOUD_TOKEN)
    component = sonar.measures.get_component_with_specified_measures(
        component=SONARQUBE_COMPONENT_KEY,
        fields="metrics,periods",
        metricKeys="code_smells")
    measures = component['component']['measures']
    for metric_data in measures:
        print(metric_data['metric'])
        if metric_data['metric'] == 'code_smells':
            metric_value = metric_data['value']
            break
    print('metric_value : ', metric_value)
    return metric_value



if __name__ == '__main__':
    main()