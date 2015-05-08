#!/usr/bin/env python
# -*- coding:utf-8 -*-

name = 'slacksend'
version = '0.1'
url = 'https://github.com/mtorromeo/slacksend'
description = "Sends messages to slack's incoming webhooks via CLI"


def build(options, args, message):
    payload = {}

    if args.attachment is not None:
        attachment = message
        message = args.attachment_message if args.attachment_message else None

    # build request
    if message:
        payload['text'] = message

    if attachment:
        attachment = {
            'fallback': 'Content attached',
            'text': attachment
        }
        if args.attachment:
            attachment['title'] = args.attachment
        if args.color:
            if args.color not in ('good', 'warning', 'danger') and args.color[0] != '#':
                args.color = '#' + args.color
            attachment['color'] = args.color
        if args.fields:
            attachment['fields'] = []
            for field in args.fields:
                title, value = field.split(':', 1)
                attachment['fields'].append({
                    'title': title,
                    'value': value,
                    'short': True,
                })
        payload['attachments'] = [attachment]

    for opt in ('channel', 'username', 'icon_url', 'icon_emoji'):
        if opt in options:
            payload[opt] = options[opt]

    return payload


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

    parser.add_argument('-V', '--version',    action='version', version="%(prog)s " + version)
    parser.add_argument('-C', '--config',     help='Use a different configuration file')
    parser.add_argument('-c', '--channel',    help='Send to this channel')
    parser.add_argument('-U', '--url',        help='Slack webhook URL')
    parser.add_argument('-u', '--username',   help='Username')
    parser.add_argument('-i', '--icon',       help='Icon')
    parser.add_argument('-a', '--attachment', help='Send as attachment', nargs='?', default=None, const='', metavar='TITLE')
    parser.add_argument('-f', '--field',      help='Add a field to the attachment', nargs='*', dest='fields', metavar='TITLE:VALUE')
    parser.add_argument('--color',            help='Color for the attachment')
    parser.add_argument('-m', '--message',    help='Use this as message and send everything else as attachment', dest='attachment_message', metavar='MESSAGE')
    parser.add_argument('message', nargs='?', help='The message to send or the attachment content if the -a argument is specified. If not specified it will be read from STDIN')

    args = parser.parse_args()

    if args.attachment_message and args.attachment is None:
        args.attachment = ''

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
    payload = build(options, args, message)
    r = requests.post(options['url'], json.dumps(payload))

    if r.status_code != 200:
        sys.exit("{} ({})".format(r.text, r.status_code))

if __name__ == '__main__':
    main()
