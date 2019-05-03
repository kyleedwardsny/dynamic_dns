#!/usr/bin/env python3

import io
import json
import os.path
import urllib.request as ur


with open(os.path.join(os.path.dirname(__file__), "settings.json")) as f:
    settings = json.load(f)

with ur.urlopen("https://ipinfo.io/json") as response:
    obj = json.load(io.TextIOWrapper(response))
    current_ip = obj["ip"]

request = ur.Request("https://api.godaddy.com/v1/domains/%s/records/A/%s" % (settings["domain"], settings["subdomain"]), headers={"Authorization": "sso-key %s:%s" % (settings["key"], settings["secret_key"])}, method="GET")
with ur.urlopen(request) as response:
    obj = json.load(io.TextIOWrapper(response))

update = False
if len(obj) != 1:
    update = True
else:
    domain_ip = obj[0]["data"]
    if domain_ip != current_ip:
        update = True

if update:
    obj = [
        {
            "data": current_ip,
            "name": settings["subdomain"],
            "ttl": 3600,
            "type": "A",
        },
    ]
    data = json.dumps(obj).encode()
    request = ur.Request("https://api.godaddy.com/v1/domains/%s/records/A/%s" % (settings["domain"], settings["subdomain"]), headers={"Authorization": "sso-key %s:%s" % (settings["key"], settings["secret_key"]), "Content-Type": "application/json"}, method="PUT", data=data)
    with ur.urlopen(request) as response:
        pass
