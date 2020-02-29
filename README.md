hola-proxy-list
===============

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

If your client doesn't support proxy authorization or doesn't support HTTPS proxies, you may need to use some middleware like haproxy which is capable to TLS proxy upstream and inject `Proxy-Authorization` header. In this case it might be useful to have `Proxy-Authorization` header exported along with other proxy data in list. `hola-proxy-list` can do it for you:

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

## Synopsis

```
$ ./hola-proxy-list.py --help
usage: hola-proxy-list.py [-h] [-l] [-A] [-c COUNTRY] [-n LIMIT]
                          [-v {debug,info,warn,error,fatal}]

Fetches free proxy list via Hola browser extension API

optional arguments:
  -h, --help            show this help message and exit
  -l, --list-countries  list available countries (default: False)
  -A, --auth-header     produce auth header for each line in output (default:
                        False)
  -c COUNTRY, --country COUNTRY
                        desired proxy location (default: us)
  -n LIMIT, --limit LIMIT
                        amount of proxies in retrieved list (default: 3)
  -v {debug,info,warn,error,fatal}, --verbosity {debug,info,warn,error,fatal}
                        logging verbosity (default: info)
```
