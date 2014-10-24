#!/usr/bin/env python
# -*- coding:utf-8 -*-

import configparser
import json

name = 'slacksend'
version = '0.1'
url = 'https://github.com/mtorromeo/slacksend'
description = "Sends messages to slack's incoming webhooks via CLI and provides a simple API"


class MissingParamError(ValueError): pass


def send(message, channel=None, url=None, username=None, icon=None, attachments=None, config=None):
    import os
    import requests

    # CONFIG file
    cfg = configparser.SafeConfigParser()
    if config:
        cfg.read(config)
    else:
        cfg.read(["/etc/{}.conf".format(name), os.path.expanduser("~/.{}.conf".format(name))])

    # merge config file with cli arguments
    options = {'attachments': attachments}
    for opt in ('channel', 'url', 'username', 'icon'):
        arg = locals()[opt]
        if arg:
            options[opt] = arg
        elif opt in cfg['DEFAULT']:
            options[opt] = cfg['DEFAULT'][opt]

    # cleanup
    if 'channel' in options and options['channel'][:1] not in ('@', '#'):
        options['channel'] = '#' + options['channel']

    if 'url' not in options:
        raise MissingParamError('Missing Slack webhook URL')

    if 'icon' in options:
        ioptname = 'icon_url' if '://' in options['icon'] else 'icon_emoji'
        options[ioptname] = options['icon']
        del options['icon']

    # build request
    payload = {
        'text': message,
    }

    for opt in ('channel', 'username', 'icon_url', 'icon_emoji', 'attachments'):
        if opt in options:
            payload[opt] = options[opt]

    return requests.post(options['url'], json.dumps(payload))


def main():
    import sys
    import argparse
    import setproctitle

    setproctitle.setproctitle(name)

    # CLI arguments
    parser = argparse.ArgumentParser(prog=name, description=description)

    parser.add_argument('-V', '--version',    action='version', version="%(prog)s " + version)
    parser.add_argument('-C', '--config',     help='Use a different configuration file')
    parser.add_argument('-c', '--channel',    help='Send to this channel')
    parser.add_argument('-U', '--url',        help='Slack webhook URL')
    parser.add_argument('-u', '--username',   help='Username')
    parser.add_argument('-i', '--icon',       help='Icon')
    parser.add_argument('-a', '--attachment', nargs='*', help='Attachment (JSON formatted)')
    parser.add_argument('message', nargs='?', help='The message to send. If not specified it will be read from STDIN')

    args = parser.parse_args()
    argsd = args.__dict__

    # rename cli arguments to function parameters
    if argsd['attachment']:
        argsd['attachments'] = []
        for attachment in argsd['attachment']:
            try:
                argsd['attachments'].append(json.loads(attachment))
            except ValueError as e:
                sys.exit("Could not decode JSON attachment: {}".format(e))

    del argsd['attachment']

    # read message from CLI or stdin
    argsd['message'] = args.message if args.message else sys.stdin.read()

    try:
        r = send(**argsd)
    except configparser.Error as e:
        sys.exit(e.message)

    if r.status_code != 200:
        sys.exit("{} ({})".format(r.text, r.status_code))

if __name__ == '__main__':
    main()
