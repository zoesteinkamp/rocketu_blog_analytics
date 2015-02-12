from django.db import models
from localflavor.us.us_states import US_STATES


class Location(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    class Meta:
        unique_together = [
            'city', 'country', 'region'
        ]

    def __unicode__(self):
        return '{}, {}, {}'.format(
            self.city,
            self.country,
            self.region,
        )


class Page(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return 'From {}'.format(
            self.url
        )


class View(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    location = models.ForeignKey(Location, related_name='views')
    page = models.ForeignKey(Page, related_name='views')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return 'Visited {} from {} with {}'.format(
            self.timestamp,
            self.location,
            self.ip_address,
        )


class Ad(models.Model):
    ad_image = models.ImageField(upload_to='media')
    ad_url = models.URLField()
    state = models.CharField(choices=US_STATES, max_length=30)

    def __unicode__(self):
        return '{}'.format(self.state)

