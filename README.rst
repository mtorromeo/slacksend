slacksend
=========

CLI tool to send messages to the Incoming webhook of Slack (https://slack.com).

Help
----

::

	usage: slacksend [-h] [-V] [-C CONFIG] [-c CHANNEL] [-U URL] [-u USERNAME]
	                 [-i ICON]
	                 [message]

	Sends messages to slack's incoming webhooks via CLI

	positional arguments:
	  message               The message to send. If not specified it will be read
	                        from STDIN

	optional arguments:
	  -h, --help            show this help message and exit
	  -V, --version         show program's version number and exit
	  -C CONFIG, --config CONFIG
	                        Use a different configuration file
	  -c CHANNEL, --channel CHANNEL
	                        Send to this channel
	  -U URL, --url URL     Slack webhook URL
	  -u USERNAME, --username USERNAME
	                        Username
	  -i ICON, --icon ICON  Icon

Configuration file
------------------

The only required option to start sending messages to slack is the webhook url.
You can either set this in a configurations file (globally in */etc/slacksend.conf* or locally in *$HOME/.slacksend.conf*) or specify it on the CLI with the --url argument.

This is an example of a configuration file for slacksend::

	[DEFAULT]
	url = https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXX
	icon = :ghost:
	username = This is a bot
	channel = @myself

Example usage
-------------

::

	echo "Hello world!" | slacksend -U https://hooks.slack.com/services/XXX
	slacksend -U https://hooks.slack.com/services/XXX "Hello world!"

LICENSE
-------
Copyright (c) 2014 Massimiliano Torromeo

slacksend is free software released under the terms of the BSD license.

See the LICENSE file provided with the source distribution for full details.

Contacts
--------

* Massimiliano Torromeo <massimiliano.torromeo@gmail.com>
