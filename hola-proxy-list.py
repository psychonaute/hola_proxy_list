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
ISO3166 = {
	'AD': 'Andorra',
	'AE': 'United Arab Emirates',
	'AF': 'Afghanistan',
	'AG': 'Antigua & Barbuda',
	'AI': 'Anguilla',
	'AL': 'Albania',
	'AM': 'Armenia',
	'AN': 'Netherlands Antilles',
	'AO': 'Angola',
	'AQ': 'Antarctica',
	'AR': 'Argentina',
	'AS': 'American Samoa',
	'AT': 'Austria',
	'AU': 'Australia',
	'AW': 'Aruba',
	'AZ': 'Azerbaijan',
	'BA': 'Bosnia and Herzegovina',
	'BB': 'Barbados',
	'BD': 'Bangladesh',
	'BE': 'Belgium',
	'BF': 'Burkina Faso',
	'BG': 'Bulgaria',
	'BH': 'Bahrain',
	'BI': 'Burundi',
	'BJ': 'Benin',
	'BM': 'Bermuda',
	'BN': 'Brunei Darussalam',
	'BO': 'Bolivia',
	'BR': 'Brazil',
	'BS': 'Bahama',
	'BT': 'Bhutan',
	'BU': 'Burma (no longer exists)',
	'BV': 'Bouvet Island',
	'BW': 'Botswana',
	'BY': 'Belarus',
	'BZ': 'Belize',
	'CA': 'Canada',
	'CC': 'Cocos (Keeling) Islands',
	'CF': 'Central African Republic',
	'CG': 'Congo',
	'CH': 'Switzerland',
	'CI': 'Cote D\'ivoire (Ivory Coast)',
	'CK': 'Cook Iislands',
	'CL': 'Chile',
	'CM': 'Cameroon',
	'CN': 'China',
	'CO': 'Colombia',
	'CR': 'Costa Rica',
	'CS': 'Czechoslovakia (no longer exists)',
	'CU': 'Cuba',
	'CV': 'Cape Verde',
	'CX': 'Christmas Island',
	'CY': 'Cyprus',
	'CZ': 'Czech Republic',
	'DD': 'German Democratic Republic (no longer exists)',
	'DE': 'Germany',
	'DJ': 'Djibouti',
	'DK': 'Denmark',
	'DM': 'Dominica',
	'DO': 'Dominican Republic',
	'DZ': 'Algeria',
	'EC': 'Ecuador',
	'EE': 'Estonia',
	'EG': 'Egypt',
	'EH': 'Western Sahara',
	'ER': 'Eritrea',
	'ES': 'Spain',
	'ET': 'Ethiopia',
	'FI': 'Finland',
	'FJ': 'Fiji',
	'FK': 'Falkland Islands (Malvinas)',
	'FM': 'Micronesia',
	'FO': 'Faroe Islands',
	'FR': 'France',
	'FX': 'France, Metropolitan',
	'GA': 'Gabon',
	'GB': 'United Kingdom (Great Britain)',
	'GD': 'Grenada',
	'GE': 'Georgia',
	'GF': 'French Guiana',
	'GH': 'Ghana',
	'GI': 'Gibraltar',
	'GL': 'Greenland',
	'GM': 'Gambia',
	'GN': 'Guinea',
	'GP': 'Guadeloupe',
	'GQ': 'Equatorial Guinea',
	'GR': 'Greece',
	'GS': 'South Georgia and the South Sandwich Islands',
	'GT': 'Guatemala',
	'GU': 'Guam',
	'GW': 'Guinea-Bissau',
	'GY': 'Guyana',
	'HK': 'Hong Kong',
	'HM': 'Heard & McDonald Islands',
	'HN': 'Honduras',
	'HR': 'Croatia',
	'HT': 'Haiti',
	'HU': 'Hungary',
	'ID': 'Indonesia',
	'IE': 'Ireland',
	'IL': 'Israel',
	'IN': 'India',
	'IO': 'British Indian Ocean Territory',
	'IQ': 'Iraq',
	'IR': 'Islamic Republic of Iran',
	'IS': 'Iceland',
	'IT': 'Italy',
	'JM': 'Jamaica',
	'JO': 'Jordan',
	'JP': 'Japan',
	'KE': 'Kenya',
	'KG': 'Kyrgyzstan',
	'KH': 'Cambodia',
	'KI': 'Kiribati',
	'KM': 'Comoros',
	'KN': 'St. Kitts and Nevis',
	'KP': 'Korea, Democratic People\'s Republic of',
	'KR': 'Korea, Republic of',
	'KW': 'Kuwait',
	'KY': 'Cayman Islands',
	'KZ': 'Kazakhstan',
	'LA': 'Lao People\'s Democratic Republic',
	'LB': 'Lebanon',
	'LC': 'Saint Lucia',
	'LI': 'Liechtenstein',
	'LK': 'Sri Lanka',
	'LR': 'Liberia',
	'LS': 'Lesotho',
	'LT': 'Lithuania',
	'LU': 'Luxembourg',
	'LV': 'Latvia',
	'LY': 'Libyan Arab Jamahiriya',
	'MA': 'Morocco',
	'MC': 'Monaco',
	'MD': 'Moldova, Republic of',
	'MG': 'Madagascar',
	'MH': 'Marshall Islands',
	'ML': 'Mali',
	'MN': 'Mongolia',
	'MM': 'Myanmar',
	'MO': 'Macau',
	'MP': 'Northern Mariana Islands',
	'MQ': 'Martinique',
	'MR': 'Mauritania',
	'MS': 'Monserrat',
	'MT': 'Malta',
	'MU': 'Mauritius',
	'MV': 'Maldives',
	'MW': 'Malawi',
	'MX': 'Mexico',
	'MY': 'Malaysia',
	'MZ': 'Mozambique',
	'NA': 'Namibia',
	'NC': 'New Caledonia',
	'NE': 'Niger',
	'NF': 'Norfolk Island',
	'NG': 'Nigeria',
	'NI': 'Nicaragua',
	'NL': 'Netherlands',
	'NO': 'Norway',
	'NP': 'Nepal',
	'NR': 'Nauru',
	'NT': 'Neutral Zone (no longer exists)',
	'NU': 'Niue',
	'NZ': 'New Zealand',
	'OM': 'Oman',
	'PA': 'Panama',
	'PE': 'Peru',
	'PF': 'French Polynesia',
	'PG': 'Papua New Guinea',
	'PH': 'Philippines',
	'PK': 'Pakistan',
	'PL': 'Poland',
	'PM': 'St. Pierre & Miquelon',
	'PN': 'Pitcairn',
	'PR': 'Puerto Rico',
	'PT': 'Portugal',
	'PW': 'Palau',
	'PY': 'Paraguay',
	'QA': 'Qatar',
	'RE': 'Reunion',
	'RO': 'Romania',
	'RU': 'Russian Federation',
	'RW': 'Rwanda',
	'SA': 'Saudi Arabia',
	'SB': 'Solomon Islands',
	'SC': 'Seychelles',
	'SD': 'Sudan',
	'SE': 'Sweden',
	'SG': 'Singapore',
	'SH': 'St. Helena',
	'SI': 'Slovenia',
	'SJ': 'Svalbard & Jan Mayen Islands',
	'SK': 'Slovakia',
	'SL': 'Sierra Leone',
	'SM': 'San Marino',
	'SN': 'Senegal',
	'SO': 'Somalia',
	'SR': 'Suriname',
	'ST': 'Sao Tome & Principe',
	'SU': 'Union of Soviet Socialist Republics (no longer exists)',
	'SV': 'El Salvador',
	'SY': 'Syrian Arab Republic',
	'SZ': 'Swaziland',
	'TC': 'Turks & Caicos Islands',
	'TD': 'Chad',
	'TF': 'French Southern Territories',
	'TG': 'Togo',
	'TH': 'Thailand',
	'TJ': 'Tajikistan',
	'TK': 'Tokelau',
	'TM': 'Turkmenistan',
	'TN': 'Tunisia',
	'TO': 'Tonga',
	'TP': 'East Timor',
	'TR': 'Turkey',
	'TT': 'Trinidad & Tobago',
	'TV': 'Tuvalu',
	'TW': 'Taiwan, Province of China',
	'TZ': 'Tanzania, United Republic of',
	'UA': 'Ukraine',
	'UG': 'Uganda',
	'UK': 'United Kingdom',
	'UM': 'United States Minor Outlying Islands',
	'US': 'United States of America',
	'UY': 'Uruguay',
	'UZ': 'Uzbekistan',
	'VA': 'Vatican City State (Holy See)',
	'VC': 'St. Vincent & the Grenadines',
	'VE': 'Venezuela',
	'VG': 'British Virgin Islands',
	'VI': 'United States Virgin Islands',
	'VN': 'Viet Nam',
	'VU': 'Vanuatu',
	'WF': 'Wallis & Futuna Islands',
	'WS': 'Samoa',
	'YD': 'Democratic Yemen (no longer exists)',
	'YE': 'Yemen',
	'YT': 'Mayotte',
	'YU': 'Yugoslavia',
	'ZA': 'South Africa',
	'ZM': 'Zambia',
	'ZR': 'Zaire',
	'ZW': 'Zimbabwe',
	'ZZ': 'Unknown or unspecified country',
}

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

def background_init(user_uuid, *, timeout=10.0):
    post_data = encode_params({
        "login": "1",
        "ver": EXT_VER,
    }).encode('ascii')
    query_string = encode_params({
        "uuid": user_uuid,
    })
    resp = fetch_url(CCGI_URL + "background_init?" + query_string,
                     data=post_data,
                     timeout=timeout)
    return json.loads(resp)

def zgettunnels(user_uuid, session_key, country="us", *, limit=3, is_premium=0,
                timeout=10.0):
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
    resp = fetch_url(CCGI_URL + "zgettunnels?" + qs, timeout=timeout)
    return json.loads(resp)

def vpn_countries(*, timeout=10.0):
    qs = encode_params({
        "browser": EXT_BROWSER,
    })
    resp = fetch_url(CCGI_URL + "vpn_countries.json?" + qs, timeout=timeout)
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

    def check_positive_float(arg):
        def fail():
            raise argparse.ArgumentTypeError("%s is not valid positive float" % (repr(arg),))
        try:
            fvalue = float(arg)
        except ValueError:
            fail()
        if fvalue <= 0:
            fail()
        return fvalue

    parser = argparse.ArgumentParser(
        description="Fetches free proxy list via Hola browser extension API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbosity",
                        help="logging verbosity",
                        type=check_loglevel,
                        choices=LogLevel,
                        default=LogLevel.info)
    req_group = parser.add_argument_group("request options")
    req_group.add_argument("-l", "--list-countries",
                           action="store_true",
                           help="list available countries")
    req_group.add_argument("-c", "--country",
                           default="us",
                           help="desired proxy location")
    req_group.add_argument("-n", "--limit",
                           default=3,
                           type=check_positive_int,
                           help="amount of proxies in retrieved list")
    req_group.add_argument("-t", "--timeout",
                           default=10.0,
                           type=check_positive_float,
                           help="timeout for network operations")
    output_group = parser.add_argument_group("output options")
    output_group.add_argument("-A", "--auth-header",
                              action="store_true",
                              help="produce auth header for each line in output")
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
            for cc in vpn_countries(timeout=args.timeout):
                print("%s - %s" % (cc, ISO3166.get(cc.upper(), "???")))
            return

        user_uuid = uuid.uuid4().hex
        logger.info("Generated user UUID: %s", user_uuid)
        logger.info("Retrieving session key...")
        session_key = background_init(user_uuid, timeout=args.timeout)["key"]
        logger.info("Session key = %s", repr(session_key))
        tunnels = zgettunnels(user_uuid, session_key,
                              country=args.country, limit=args.limit,
                              timeout=args.timeout)
        logger.debug("Retrieved tunnels data: %s", tunnels)
        output_csv(tunnels, user_uuid, args.auth_header)
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        logger.exception("Got exception: %s", str(exc))

if __name__ == "__main__":
    main()
