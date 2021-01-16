# WEB-resource monitor written as the Lambda function. It can be run on AWS using its Lambda service.
# Resources must be supplied as a JSON encoded string in the following format:
# [{"url": "http://example.com", "expectedCode": 200}]
# Where url can start with http or https
# GET parameters are also supported
# You can supply the string through the environment variable  RESOURCE_MONITOR_RESOURCES
# For AWS Lambda functions it is the easiest way to go

from json import JSONDecodeError, loads
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def get_error_message(url, status_code, expected_code):
    """ Constract a message based on supplied parameters and return it"""
    return '{0} returned status code {1}. {2} was expected'.format(url, status_code, expected_code)

def check_resorce(url, expected_code):
    """ Make an HTTP request to a givern resource, if the return status code is not equal to the expected code, raise an exception with a explanation """
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36') # To prevent retreaving pages
    try:
        response = urlopen(request)
    except HTTPError as e:
        raise Exception(get_error_message(url, e.code, expected_code))
    except Exception as e:
        raise e
    else:
        if response.getcode() != expected_code:
            raise Exception(get_error_message(url, response.getcode(), expected_code))


def lambda_handler(event, context):
    # This function will be called by AWS Lambda service internally
    resources_str = os.getenv('RESOURCE_MONITOR_RESOURCES')
    if resources_str == None:
        print('ConfigurationError: no resources were supplied')
        exit(1)

    resources = []
    try:
        resources = loads(resources_str)
    except JSONDecodeError as e:
        print('JSONDecodeError: ', str(e))
        exit(1)

    for resource in resources:
        try:
            check_resorce(resource['url'], resource['expectedCode'])
        except Exception as e:
            print('HTTPError: ', str(e))
        else:
            print(resource['url'], ' is working properly')

