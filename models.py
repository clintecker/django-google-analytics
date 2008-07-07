from django.db import models
from django.contrib.sites.models import Site

class Analytics(models.Model):
    site = models.ForeignKey(Site, edit_inline=models.TABULAR, max_num_in_admin=1, min_num_in_admin=1)
    analytics_code = models.CharField(blank=True, max_length=100, core=True)

    def __unicode__(self):
        return u"%s" % (self.analytics_code)
