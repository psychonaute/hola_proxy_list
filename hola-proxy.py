#!/usr/bin/env python3

import sys
import argparse
import enum
import logging
import uuid
import urllib.request
import urllib.parse
import codecs
import json
import random
import base64
import csv

USER_AGENT = "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
EXT_VER = "1.164.641"
EXT_BROWSER = "chrome"
PRODUCT = "cws"
CCGI_URL = "https://client.hola.org/client_cgi/"
PORT_TYPE_WHITELIST = {"direct", "peer"}
PROTOCOL_WHITELIST = {"http", "HTTP"}

def setup_logger(name, verbosity):
    logger = logging.getLogger(name)
    logger.setLevel(verbosity)
    handler = logging.StreamHandler()
    handler.setLevel(verbosity)
    handler.setFormatter(logging.Formatter("%(asctime)s "
                                           "%(levelname)-8s "
                                           "%(name)s: %(message)s",
                                           "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    return logger

class LogLevel(enum.IntEnum):
    debug = logging.DEBUG
    info = logging.INFO
    warn = logging.WARN
    error = logging.ERROR
    fatal = logging.FATAL
    crit = logging.CRITICAL

    def __str__(self):
        return self.name

def fetch_url(url, *, data=None, method=None, timeout=10):
    logger = logging.getLogger("FETCH")
    logger.debug("Fetching URL %s with method %s, post data=%s",
                 url, method, repr(data))
    http_req = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": USER_AGENT
        }
    )
    with urllib.request.urlopen(http_req, None, timeout) as resp:
        coding = resp.headers.get_content_charset()
        coding = coding if coding is not None else "utf-8-sig"
        decoder = codecs.getreader(coding)(resp)
        res = decoder.read()
    return res

def encode_params(params, encoding=None):
    return urllib.parse.urlencode(params, encoding=encoding)

def background_init(user_uuid):
    post_data = encode_params({
        "login": "1",
        "ver": EXT_VER,
    }).encode('ascii')
    query_string = encode_params({
        "uuid": user_uuid,
    })
    resp = fetch_url(CCGI_URL + "background_init?" + query_string,
                     data=post_data)
    return json.loads(resp)

def zgettunnels(user_uuid, session_key, country="us", *, limit=3, is_premium=0):
    qs = encode_params({
        "country": country,
        "limit": limit,
        "ping_id": random.random(),
        "ext_ver": EXT_VER,
        "browser": EXT_BROWSER,
        "product": PRODUCT,
        "uuid": user_uuid,
        "session_key": session_key,
        "is_premium": is_premium,
    })
    resp = fetch_url(CCGI_URL + "zgettunnels?" + qs)
    return json.loads(resp)

def vpn_countries():
    qs = encode_params({
        "browser": EXT_BROWSER,
    })
    resp = fetch_url(CCGI_URL + "vpn_countries.json?" + qs)
    return json.loads(resp)

def parse_args():
    def check_loglevel(arg):
        try:
            return LogLevel[arg]
        except (IndexError, KeyError):
            raise argparse.ArgumentTypeError("%s is not valid loglevel" % (repr(arg),))

    def check_positive_int(arg):
        def fail():
            raise argparse.ArgumentTypeError("%s is not valid positive integer" % (repr(arg),))
        try:
            ivalue = int(arg)
        except ValueError:
            fail()
        if ivalue <= 0:
            fail()
        return ivalue

    parser = argparse.ArgumentParser(
        description="Fetches free proxy list via Hola browser extension API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--list-countries",
                        action="store_true",
                        help="list available countries")
    parser.add_argument("-A", "--auth-header",
                        action="store_true",
                        help="produce auth header for each line in output")
    parser.add_argument("-c", "--country",
                        default="us",
                        help="desired proxy location")
    parser.add_argument("-n", "--limit",
                        default=3,
                        type=check_positive_int,
                        help="amount of proxies in retrieved list")
    parser.add_argument("-v", "--verbosity",
                        help="logging verbosity",
                        type=check_loglevel,
                        choices=LogLevel,
                        default=LogLevel.info)
    return parser.parse_args()

def output_csv(tunnels, user_uuid, auth_header=False):
    login = "user-uuid-" + user_uuid
    password = tunnels["agent_key"]
    fields = ["Host", "IP address", "Port", "Port type", "Vendor", "Login", "Password"]
    if auth_header:
        auth_header = "Proxy-Authorization: basic %s" % base64.b64encode(
            (login + ":" + password).encode('ascii')).decode('ascii')
        fields.append("Auth header")
    host_pairs = [(host, ip) for host, ip in tunnels["ip_list"].items()
                  if tunnels["protocol"][host] in PROTOCOL_WHITELIST]
    port_pairs = [(t, p) for t, p in tunnels["port"].items()
                  if t in PORT_TYPE_WHITELIST]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for host, ip in host_pairs:
        for port_type, port in port_pairs:
            row = {
                "Host": host,
                "IP address": ip,
                "Port": port,
                "Port type": port_type,
                "Vendor": tunnels["vendor"][host],
                "Login": login,
                "Password": password,
            }
            if auth_header:
                row["Auth header"] = auth_header
            writer.writerow(row)

def main():
    args = parse_args()
    logger = setup_logger("MAIN", args.verbosity)
    setup_logger("FETCH", args.verbosity)
    try:
        if args.list_countries:
            for cc in vpn_countries():
                print(cc)
            return

        user_uuid = uuid.uuid4().hex
        logger.info("Generated user UUID: %s", user_uuid)
        logger.info("Retrieving session key...")
        session_key = background_init(user_uuid)["key"]
        logger.info("Session key = %s", repr(session_key))
        tunnels = zgettunnels(user_uuid, session_key,
                              country=args.country, limit=args.limit)
        logger.debug("Retrieved tunnels data: %s", tunnels)
        output_csv(tunnels, user_uuid)
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        logger.exception("Got exception: %s", str(exc))

if __name__ == "__main__":
    main()
