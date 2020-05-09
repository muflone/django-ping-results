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

from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class Result(BaseModel):
    host = models.ForeignKey('Host',
                             on_delete=models.PROTECT,
                             verbose_name=pgettext_lazy('Result',
                                                        'host'))
    timestamp = models.DateTimeField(verbose_name=pgettext_lazy('Result',
                                                                'timestamp'))
    status = models.BooleanField(verbose_name=pgettext_lazy('Result',
                                                            'status'))
    elapsed = models.FloatField(blank=True,
                                null=True,
                                verbose_name=pgettext_lazy('Result',
                                                           'elapsed time'))

    class Meta:
        # Define the database table
        db_table = 'ping_results_results'
        ordering = ['-timestamp', 'host']
        unique_together = ('host', 'timestamp')
        verbose_name = pgettext_lazy('Result', 'Result')
        verbose_name_plural = pgettext_lazy('Result', 'Results')

    def __str__(self):
        return '{HOST} {DATETIME}'.format(HOST=self.host,
                                          DATETIME=self.timestamp.strftime(
                                              '%Y-%m-%d %H:%M.%S.%f'))


class ResultAdmin(BaseModelAdmin):
    pass
