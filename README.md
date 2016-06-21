# fbfeed2rss
Facebook feed to RSS gateway

## Installing
Put files into some directory and run `fbfeed2rss.py` with python. Program has no external dependencies.

## Running
`fbfeed2rss` runs as web-server and requires Facebook API access token for operation. Key should be specified in a text file which contains only one line with key. Path to token file can be specified with `-k` option, but defaults to `fbtoken.txt`.
