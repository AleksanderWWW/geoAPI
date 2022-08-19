from typing import Dict, Any

import requests


def fetch_ip_data(ip: str, ip_stack_key:str) -> Dict[str, Any]:
    """
    Fetches json response from ipstack API about a particular ip address

    :param ip: ip address of interest
    :type ip: str
    :param ip_stack_key: api key neccessary to access ipstack API
    :type ip_stack key: str

    :return: json response from ipstack API
    :rtype: dict
    """
    url = f"http://api.ipstack.com/{ip}?access_key={ip_stack_key}"
    resp = requests.get(url)
    return resp.json()
