##
#     Project: Django Ping Results
# Description: A Django application to collect ping results
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2020 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import argparse
import re
import subprocess

from django.db import models
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from ping_results.models import Host, Result


class Command(BaseCommand):
    help = 'Ping a host'

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        BaseCommand.add_arguments(self, parser)
        parser.add_argument('--host',
                            action='store',
                            type=str,
                            required=True,
                            help=pgettext_lazy(
                                'Ping',
                                'Host to ping'))
        parser.add_argument('--count',
                            action='store',
                            type=int,
                            default=0,
                            help=pgettext_lazy(
                                'Ping',
                                'Max ping count'))

    def handle(self, *args, **options) -> None:
        # Get Host
        try:
            host = Host.objects.get(name=options['host'])
        except models.ObjectDoesNotExist:
            # Not existing host
            print('No host named "{NAME}"'.format(
                NAME=options['host']))
        # Check Host
        if host:
            arguments = ['ping',
                         '-D',
                         '-O',
                         '-i',
                         str(host.delay) if host.delay > 1 else '1',
                         host.hostname]
            process = subprocess.Popen(args=arguments,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            count = 0
            regex_time = re.compile(r'time=(\d)+(\.)(\d)*')
            # Repeat until terminated or count done
            while (process.poll() is None) and (
                    count < options['count'] or options['count'] == 0):
                line = process.stdout.readline()[:-1]
                if line.startswith('['):
                    # Find duration
                    match = regex_time.search(line)
                    duration = (float(match.group().replace('time=', ''))
                                if match
                                else None)
                    Result.objects.create(host=host,
                                          timestamp=timezone.now(),
                                          status=duration is not None,
                                          elapsed=duration)
                    print(line)
                    count += 1
            process.stdout.close()
            process.kill()
