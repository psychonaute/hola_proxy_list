hola-proxy-list
===============

---

This project is superseeded by [hola-proxy](https://github.com/Snawoot/hola-proxy)

---

Fetches free proxy list via Hola browser extension API. Resulting list contains proxies which forward traffic directly from server (`direct` type) and via peers with residental IP addresses in specified country (`peer` type). Proxies support both HTTP and HTTPS protocols (i.e. HTTP proxy via TLS channel between client and proxy server).

Once proxy was accessed with proper credentials, it will whitelist your IP address for a while and will not require authentication for further requests. However, it might be more convenient to enable authorization for all requests unconditionally.

hola-proxy-list outputs resulting list in CSV format into stdout and logs get written to stderr. Those two outputs don't interfere with each other and you may use output of application right away as machine-readable input for other programs.

Note: proxy auth credentials have some expiration time, so you'll have to update it from time to time.

## Requirements

Python 3.4+

## Usage example

Retrieve list of available countries:

```
$ ./hola-proxy-list.py -l
ar - Argentina
at - Austria
au - Australia
be - Belgium
bg - Bulgaria
br - Brazil
ca - Canada
ch - Switzerland
cl - Chile
co - Colombia
cz - Czech Republic
de - Germany
dk - Denmark
es - Spain
fi - Finland
fr - France
gr - Greece
hk - Hong Kong
hu - Hungary
id - Indonesia
ie - Ireland
il - Israel
in - India
it - Italy
jp - Japan
kr - Korea, Republic of
mx - Mexico
nl - Netherlands
no - Norway
nz - New Zealand
pl - Poland
ro - Romania
ru - Russian Federation
se - Sweden
sg - Singapore
sk - Slovakia
tr - Turkey
uk - United Kingdom
us - United States of America
```

Get proxies in Sweden:

```
$ ./hola-proxy-list.py -c se
2020-02-29 14:23:23 INFO     MAIN: Generated user UUID: ed8087e8681c4ac9bdad03f17b623a75
2020-02-29 14:23:23 INFO     MAIN: Retrieving session key...
2020-02-29 14:23:23 INFO     MAIN: Session key = 2332190283
Host,IP address,Port,Port type,Vendor,Login,Password
zagent1977.hola.org,178.73.210.145,22222,direct,edis,user-uuid-ed8087e8681c4ac9bdad03f17b623a75,16e73f43fc5d
zagent1977.hola.org,178.73.210.145,22223,peer,edis,user-uuid-ed8087e8681c4ac9bdad03f17b623a75,16e73f43fc5d
zagent267.hola.org,46.246.126.114,22222,direct,edis,user-uuid-ed8087e8681c4ac9bdad03f17b623a75,16e73f43fc5d
zagent267.hola.org,46.246.126.114,22223,peer,edis,user-uuid-ed8087e8681c4ac9bdad03f17b623a75,16e73f43fc5d
zagent1932.hola.org,46.246.93.226,22222,direct,edis,user-uuid-ed8087e8681c4ac9bdad03f17b623a75,16e73f43fc5d
zagent1932.hola.org,46.246.93.226,22223,peer,edis,user-uuid-ed8087e8681c4ac9bdad03f17b623a75,16e73f43fc5d
```

Use proxy. Here is an example of usage of direct HTTPS proxy with curl:

```
$ curl --proxy https://user-uuid-ed8087e8681c4ac9bdad03f17b623a75:16e73f43fc5d@zagent1977.hola.org:22222 https://ifconfig.me ; echo
178.73.210.145
```

For more options see Synopsis below.

## Using with middlewares

If your client doesn't support proxy authorization or doesn't support HTTPS proxies, you may need to use some middleware like haproxy which is capable to connect to a TLS proxy upstream and inject `Proxy-Authorization` header. In this case it might be useful to have `Proxy-Authorization` header exported along with other proxy data in list. `hola-proxy-list` can do it for you:

```
$ ./hola-proxy-list.py -c se -A
2020-02-29 14:34:42 INFO     MAIN: Generated user UUID: b0ada121f24945259857731a661324ab
2020-02-29 14:34:42 INFO     MAIN: Retrieving session key...
2020-02-29 14:34:42 INFO     MAIN: Session key = 336269028
Host,IP address,Port,Port type,Vendor,Login,Password,Auth header
zagent994.hola.org,178.73.210.76,22222,direct,edis,user-uuid-b0ada121f24945259857731a661324ab,da36c03f59e8,Proxy-Authorization: basic dXNlci11dWlkLWIwYWRhMTIxZjI0OTQ1MjU5ODU3NzMxYTY2MTMyNGFiOmRhMzZjMDNmNTllOA==
zagent994.hola.org,178.73.210.76,22223,peer,edis,user-uuid-b0ada121f24945259857731a661324ab,da36c03f59e8,Proxy-Authorization: basic dXNlci11dWlkLWIwYWRhMTIxZjI0OTQ1MjU5ODU3NzMxYTY2MTMyNGFiOmRhMzZjMDNmNTllOA==
zagent404.hola.org,46.246.126.21,22222,direct,edis,user-uuid-b0ada121f24945259857731a661324ab,da36c03f59e8,Proxy-Authorization: basic dXNlci11dWlkLWIwYWRhMTIxZjI0OTQ1MjU5ODU3NzMxYTY2MTMyNGFiOmRhMzZjMDNmNTllOA==
zagent404.hola.org,46.246.126.21,22223,peer,edis,user-uuid-b0ada121f24945259857731a661324ab,da36c03f59e8,Proxy-Authorization: basic dXNlci11dWlkLWIwYWRhMTIxZjI0OTQ1MjU5ODU3NzMxYTY2MTMyNGFiOmRhMzZjMDNmNTllOA==
zagent1982.hola.org,46.246.93.155,22222,direct,edis,user-uuid-b0ada121f24945259857731a661324ab,da36c03f59e8,Proxy-Authorization: basic dXNlci11dWlkLWIwYWRhMTIxZjI0OTQ1MjU5ODU3NzMxYTY2MTMyNGFiOmRhMzZjMDNmNTllOA==
zagent1982.hola.org,46.246.93.155,22223,peer,edis,user-uuid-b0ada121f24945259857731a661324ab,da36c03f59e8,Proxy-Authorization: basic dXNlci11dWlkLWIwYWRhMTIxZjI0OTQ1MjU5ODU3NzMxYTY2MTMyNGFiOmRhMzZjMDNmNTllOA==
```

hola-proxy-list utility has special support for haproxy and capable to output haproxy config. See Output Formats section below.

## Output Formats

### CSV output

Default output format. All examples above illustrate it.

### URI output
This format outputs URI. easy to use in bash scripts..

```
$ curl -x $(./hola-proxy-list.py  -O uri -n 1) 'https://httpbin.org/get'
2020-07-07 22:12:41 INFO     MAIN: Generated user UUID: f0211175927740b4bd2a7fe2d57b1fa2
2020-07-07 22:12:41 INFO     MAIN: Retrieving session key...
2020-07-07 22:12:41 INFO     MAIN: Session key = 3293743567
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.58.0",
    "X-Amzn-Trace-Id": "Root=1-5f04d73b-4e0af4244e4c739adc2696dc"
  },
  "origin": "192.241.230.96",
  "url": "https://httpbin.org/get"
}
```

### JSON output

This format outputs JSON which has structure almost identical to API response. Example:

```
$ ./hola-proxy-list.py -O json -c us
2020-03-01 16:12:02 INFO     MAIN: Generated user UUID: f0211175927740b4bd2a7fe2d57b1fa2
2020-03-01 16:12:02 INFO     MAIN: Retrieving session key...
2020-03-01 16:12:03 INFO     MAIN: Session key = 3293743567
{
    "agent_key": "253627386895",
    "agent_types": {
        "us": "hola"
    },
    "ip_list": {
        "zagent2051.hola.org": "159.89.183.208",
        "zagent520.hola.org": "184.164.146.10",
        "zagent775.hola.org": "104.131.243.162"
    },
    "port": {
        "direct": 22222,
        "hola": 22224,
        "peer": 22223,
        "trial": 22225,
        "trial_peer": 22226
    },
    "protocol": {
        "zagent2051.hola.org": "http",
        "zagent520.hola.org": "http",
        "zagent775.hola.org": "http"
    },
    "uuid": "f0211175927740b4bd2a7fe2d57b1fa2",
    "vendor": {
        "zagent2051.hola.org": "digitalocean",
        "zagent520.hola.org": "nqhost",
        "zagent775.hola.org": "digitalocean"
    },
    "ztun": {
        "us": [
            "HTTP zagent520.hola.org:22222",
            "HTTP zagent2051.hola.org:22222",
            "HTTP zagent775.hola.org:22222"
        ]
    }
```

### HAProxy config output

This format uses default template `haproxy.cfg.tmpl` in script directory (or one specified with `-T` option) and outputs HAProxy configuration which for retrieved proxies. Configuration template has substitution syntax of [built-in Python templates](https://docs.python.org/3/library/string.html#template-strings).

List of available template variables:

* `$first_host` - first host in list
* `$first_ip` - IP address of first host in list
* `$auth_header` - proxy basic authorization header
* `$direct_port` - direct proxy port number
* `$peer_port` - peer proxy port number
* `$host` - hostname of proxy in list. If this variable met in template line, given line yielded for each proxy in list
* `$ip` - IP address of proxy in list. If this variable met in template line, given line yielded for each proxy in list
* `$counter` - counter, which starts from 0. Useful for producing names of servers in haproxy backend section. If this variable met in template line, given line yielded for each proxy in list

Default template produces configuration providing plain HTTP proxy without authentication on local port 8080. Proxy connections forwarded via verified TLS connections to first alive upstream proxy. Alive proxies determined by periodic health checks with an authenticated CONNECT request.

Example of produced config with [default template](https://github.com/Snawoot/hola-proxy-list/blob/master/haproxy.cfg.tmpl):

```
$ ./hola-proxy-list.py -O haproxy -c us
2020-03-01 16:28:32 INFO     MAIN: Generated user UUID: e480985e8d474d4c989429f394f68f9b
2020-03-01 16:28:32 INFO     MAIN: Retrieving session key...
2020-03-01 16:28:33 INFO     MAIN: Session key = 4278986874
global
    maxconn 1000
    max-spread-checks 10000

defaults
    mode    http
    timeout connect 5000
    timeout client  600000
    timeout server  600000
    timeout tunnel  0
    timeout check   5000

frontend http-proxy
    bind 127.0.0.1:8080
    mode http
    # These five lines is a fix for torrent
    acl local_retracker url -i -m beg http://retracker.local/
    acl bt_announce urlp(info_hash) -m found
    acl port0 urlp(port) 0
    http-request reject if local_retracker
    http-request set-query %[query,regsub(^port=0,port=1),regsub(&port=0,&port=1)] if bt_announce port0
    http-request add-header Proxy-Authorization "basic dXNlci11dWlkLWU0ODA5ODVlOGQ0NzRkNGM5ODk0MjlmMzk0ZjY4ZjliOmZkODdhNDU4NGYwMQ=="
    default_backend proxy-be

backend proxy-be
    balance first
    default-server inter 60s fall 2 rise 3
    option httpchk CONNECT www.google.com:443 "HTTP/1.1\r\nProxy-Authorization: basic dXNlci11dWlkLWU0ODA5ODVlOGQ0NzRkNGM5ODk0MjlmMzk0ZjY4ZjliOmZkODdhNDU4NGYwMQ=="
    server proxy0 zagent777.hola.org:22222 ssl sni str(zagent777.hola.org) verify required verifyhost zagent777.hola.org ca-file /etc/ssl/certs/ca-bundle.crt check
    server proxy1 zagent874.hola.org:22222 ssl sni str(zagent874.hola.org) verify required verifyhost zagent874.hola.org ca-file /etc/ssl/certs/ca-bundle.crt check
    server proxy2 zagent1254.hola.org:22222 ssl sni str(zagent1254.hola.org) verify required verifyhost zagent1254.hola.org ca-file /etc/ssl/certs/ca-bundle.crt check
```

You can keep your haproxy config updated with cron job like one presented below:

```sh
python3 ~/src/hola-proxy-list/hola-proxy-list.py -v error -O haproxy -c us > /etc/haproxy/haproxy.cfg.new && \
    mv /etc/haproxy/haproxy.cfg.new /etc/haproxy/haproxy.cfg && \
    systemctl reload haproxy
```

## Synopsis

```
$ ./hola-proxy-list.py --help
usage: hola-proxy-list.py [-h] [-v {debug,info,warn,error,fatal}] [-l]
                          [-c COUNTRY] [-n LIMIT] [-t TIMEOUT]
                          [-O {csv,json,haproxy}] [-A] [-T TEMPLATE]

Fetches free proxy list via Hola browser extension API

optional arguments:
  -h, --help            show this help message and exit
  -v {debug,info,warn,error,fatal}, --verbosity {debug,info,warn,error,fatal}
                        logging verbosity (default: info)

request options:
  -l, --list-countries  list available countries (default: False)
  -c COUNTRY, --country COUNTRY
                        desired proxy location (default: us)
  -n LIMIT, --limit LIMIT
                        amount of proxies in retrieved list (default: 3)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout for network operations (default: 10.0)

output options:
  -O {csv,json,haproxy}, --output-format {csv,json,haproxy}
                        output format (default: csv)
  -A, --auth-header     (CSV format only) produce auth header for each line in
                        output (default: False)
  -T TEMPLATE, --template TEMPLATE
                        (haproxy format only) haproxy config template file
                        (default: /home/user/src/hola-proxy-list/haproxy.cfg.tmpl)
```
