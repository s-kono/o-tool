#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/post-statuses-update

import argparse
import configparser
import sys

from urllib.parse import urlencode

# pip3 install oauth2
from oauth2 import Client, Consumer, Token

"""
$ cat <configfile>
[general]
consumer_key = AAAAAAAAAAAAAAAAAAAAAA
consumer_secret = BBBBBBBBBBBBBBBBBBBBBB
user_key = CCCCCCCCCCCCCCCCCCCCCCCCCCC
user_secret = DDDDDDDDDDDDDDDDDDDDDDD
"""


def parser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
      '-c', '--configfile',
      help='config file path',
      required=True,
    )
    parser.add_argument(
      '-r', '--replyid',
      help='reply id',
      required=False,
    )
    parser.add_argument(
      '-m', '--message',
      help='tweet message',
      required=True,
    )
    return parser.parse_args()


def main(args):
    conf = configparser.SafeConfigParser()
    try:
        conf.read(args.configfile)
        consumer_key = conf.get('general', 'consumer_key')
        consumer_secret = conf.get('general', 'consumer_secret')
        user_key = conf.get('general', 'user_key')
        user_secret = conf.get('general', 'user_secret')
    except Exception as e:
        print('err: (', args.configfile, ')', e, file=sys.stderr)
        sys.exit(1)

    twclient = Client(
      Consumer(consumer_key, consumer_secret),
      Token(user_key, user_secret),
    )
    if args.replyid is None:
        ret = twclient.request(
          'https://api.twitter.com/1.1/statuses/update.json',
          'POST',
          urlencode({'status': args.message})
        )
    else:
        ret = twclient.request(
          'https://api.twitter.com/1.1/statuses/update.json',
          'POST',
          urlencode(
            {'status': args.message, 'in_reply_to_status_id': args.replyid}
          )
        )

    if int(ret[0]['status']) == 200:
        print(ret[1].decode('utf-8'))
    else:
        print('err:', ret[0]['status'], file=sys.stderr)
        print(ret[1].decode('utf-8'))
        sys.exit(2)


if __name__ == '__main__':
    main(parser())
