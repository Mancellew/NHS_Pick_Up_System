import requests
from requests import Response


def check_response(response: Response, message):
    """
    Automatically checks if the response within the 2xx-3xx range
    and raises a ValueError with the message provided if that's not the case
    :param response: The Response object returned by a request
    :param message: The message to include in case of an exception
    :return: This function does not return anything
    :raise: ValueError if the response status code is not within the range 2xx-3xx
    """
    if not response.ok:
        raise ValueError(message)


def get_and_check(url, headers=None, timeout=None, error_message="Unhandled error: {}", verify_ssl=True) -> Response:
    """
    Wrapper to make get requests and check their response for potentially unwanted HTTP status codes
    :param url: The url to make the GET request
    :param headers: Headers to be used in the request
    :param timeout: How long to wait until the request is assumed to have had an error
    :param error_message: The error message template, to attach the response text to, in case of an error
    :param verify_ssl: Whether SSL verification (hence use of https) will be enforced or not
    :return: The response returned from the request
    :raise: ValueError if the response status code is not within the range 2xx-3xx
    """
    response = requests.get(url, headers=headers, timeout=timeout, verify=verify_ssl)

    if error_message:
        check_response(response, error_message.format(response.text))

    return response


def post_and_check(url, json=None, data=None, headers=None, timeout=None, error_message="Unhandled error: {}",
                   verify_ssl=True) -> Response:
    """
    Wrapper to make put requests and check their response for potentially unwanted HTTP status codes
    :param url: The url to make the PUT request
    :param json: A python dictionary to be dumped in the request json body
    :param data: Direct data to put in the request body without further dumping or other operations made to it
    :param headers: Headers to be used in the request
    :param timeout: How long to wait until the request is assumed to have had an error
    :param error_message: The error message template, to attach the response text to, in case of an error
    :param verify_ssl: Whether SSL verification (hence use of https) will be enforced or not
    :return:The response returned from the request
    :raise: ValueError if the response status code is not within the range 2xx-3xx
    """

    if json:
        response = requests.post(url, json=json, headers=headers, timeout=timeout, verify=verify_ssl)
    else:
        response = requests.post(url, data=data, headers=headers, timeout=timeout, verify=verify_ssl)

    if error_message:
        check_response(response, error_message.format(response.text))

    return response
