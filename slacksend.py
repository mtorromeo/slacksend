#!/usr/bin/env python
# -*- coding:utf-8 -*-

name = 'slacksend'
version = '0.1'
url = 'https://github.com/mtorromeo/slacksend'
description = "Sends messages to slack's incoming webhooks via CLI"

def main():
    import sys
    import os
    import argparse
    import configparser
    import json

    import setproctitle
    import requests

    setproctitle.setproctitle(name)

    # CLI arguments
    parser = argparse.ArgumentParser(prog=name, description=description)

    parser.add_argument('-V', '--version',  action='version', version="%(prog)s " + version)
    parser.add_argument('-C', '--config',   help='Use a different configuration file')
    parser.add_argument('-c', '--channel',  help='Send to this channel')
    parser.add_argument('-U', '--url',      help='Slack webhook URL')
    parser.add_argument('-u', '--username', help='Username')
    parser.add_argument('-i', '--icon',     help='Icon')
    parser.add_argument('message', nargs='?', help='The message to send. If not specified it will be read from STDIN')

    args = parser.parse_args()

    # CONFIG file
    config = configparser.SafeConfigParser()
    try:
        if args.config:
            config.read(args.config)
        else:
            config.read(["/etc/{}.conf".format(name), os.path.expanduser("~/.{}.conf".format(name))])
    except configparser.Error as e:
        sys.exit(e.message)

    # merge config file with cli arguments
    options = {}
    for opt in ('channel', 'url', 'username', 'icon'):
        arg = getattr(args, opt)
        if arg:
            options[opt] = arg
        elif opt in config['DEFAULT']:
            options[opt] = config['DEFAULT'][opt]

    # cleanup
    if 'channel' in options and options['channel'][:1] not in ('@', '#'):
        sys.exit('Invalid channel name. It should start with # or @.')

    if 'url' not in options:
        sys.exit('Missing Slack webhook URL')

    if 'icon' in options:
        ioptname = 'icon_url' if '://' in options['icon'] else 'icon_emoji'
        options[ioptname] = options['icon']
        del options['icon']

    # read message from CLI or stdin
    message = args.message if args.message else sys.stdin.read()

    # build request
    payload = {
        'text': message,
    }

    for opt in ('channel', 'username', 'icon_url', 'icon_emoji'):
        if opt in options:
            payload[opt] = options[opt]

    r = requests.post(options['url'], json.dumps(payload))

    if r.status_code != 200:
        sys.exit("{} ({})".format(r.text, r.status_code))

if __name__ == '__main__':
    main()
