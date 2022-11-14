from typing import (
    Any,
    Dict,
)

import requests
from flask import Request


def parse_request(request: Request) -> str:
    if "ip" in request.args.keys():
        ip = request.args.get("ip")
    elif "ip" in request.json.keys():
        ip = request.json.get("ip")
    else:
        ip = ""

    return ip


def fetch_ip_data(ip: str, ip_stack_key: str) -> Dict[str, Any]:
    """
    Fetches json response from ipstack API about a particular ip address

    :param ip: ip address of interest
    :type ip: str
    :param ip_stack_key: api key necessary to access ipstack API
    :type ip_stack_key: str

    :return: json response from ipstack API
    :rtype: dict
    """
    url = f"http://api.ipstack.com/{ip}?access_key={ip_stack_key}"
    resp = requests.get(url)
    return resp.json()
