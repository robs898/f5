import requests
import json
import os
from pprint import pprint
from urllib3.exceptions import InsecureRequestWarning


def delete(url, token=""):
    if token:
        headers = {"X-F5-Auth-Token": token}
        r = requests.delete(url, headers=headers, verify=False)
    else:
        raise ("missing token")
    return check(r)


def get(url, token=""):
    if token:
        headers = {"X-F5-Auth-Token": token}
        r = requests.get(url, headers=headers, verify=False)
    else:
        r = requests.get(url, verify=False)
    return check(r)


def post(url, json, token=""):
    if token:
        headers = {"X-F5-Auth-Token": token}
        r = requests.post(url, headers=headers, json=json, verify=False)
    else:
        r = requests.post(url, json=json, verify=False)
    return check(r)


def check(resp):
    if resp.status_code == 200:
        return resp.json()
    else:
        raise ("request failed")


def get_vars():
    user = os.environ.get("USER")
    passwd = os.environ.get("PASSWD")
    return user, passwd


def get_token(user, passwd):
    json = {"username": user, "password": passwd, "loginProviderName": "tmos"}
    r = post("https://18.130.90.35/mgmt/shared/authn/login", json)
    return r["token"]["token"]


def get_info(token):
    r = get("https://18.130.90.35/mgmt/shared/appsvcs/info", token=token)
    return r


def delete_tenant(token):
    r = delete("https://18.130.90.35/mgmt/shared/appsvcs/declare/robbie", token=token)
    return r


def declare(token, json):
    r = post("https://18.130.90.35/mgmt/shared/appsvcs/declare", json, token=token)
    return r


def main():
    user, passwd = get_vars()
    token = get_token(user, passwd)
    info = get_info(token)
    #d = delete_tenant(token)
    #pprint(d)
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        declaration = declare(token, data)
        pprint(declaration)


if __name__ == "__main__":
    main()
