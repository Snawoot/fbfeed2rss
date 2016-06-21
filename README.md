# fbfeed2rss
Facebook feed to RSS gateway

## Requirements
* One of following operating system:
  * Linux
  * Windows
  * \*BSD
* Python 2.6/2.7

Program depends only on Python system libraries

## Installing
Put files into some directory and run `fbfeed2rss.py` with python. 

## Running
`fbfeed2rss` runs as web-server and requires Facebook API access token for operation. Key should be specified in a text file which contains only one line with key. Path to token file can be specified with `-k` option, but defaults to `fbtoken.txt`.

### Obtaining an access token
Just register facebook developer account and create any application. [Step-by-step guide for registering an facebook app](https://developers.facebook.com/docs/apps/register)
After that you can supply your application token in text file for this program.

### Usage
Feel free to run `fbfeed2rss.py` with `-h` or `--help` option to get help on command line options.

```
$ ./fbfeed2rss.py -h
usage: fbfeed2rss.py [-h] [-H ADDRESS] [-p PORT] [-k KEYFILE]

Facebook feed API to RSS gate

optional arguments:
  -h, --help            show this help message and exit
  -H ADDRESS, --host ADDRESS
                        listen address (default: '0.0.0.0')
  -p PORT, --port PORT  listen port (default: 1716)
  -k KEYFILE, --token-file KEYFILE
                        path to application access token (text file containing
                        facebook API access token, default: 'fbtoken.txt')
```

When server is up and running RSS feed is available at address:
`http://server_address:server_port/rss/v1.0/feed?id=<page_numeric_id>`
