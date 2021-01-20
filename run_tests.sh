#!/bin/bash
export RESOURCE_MONITOR_RESOURCES='[{"url": "https://google.com", "expectedCode": 404}]'
export RESOURCE_MONITOR_SLACK_URL=''
python lambda_function.test.py