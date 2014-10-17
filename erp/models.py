from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    added_time = models.DateTimeField('added time')
    modified_time = models.DateTimeField('last modified time')
    is_enabled = models.BooleanField(default=True)

    class Meta:
        abstract = True
        app_label = 'erp'


class Space(BaseModel):
    name = models.CharField(max_length=200)  # null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    kind = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    logo = models.URLField(max_length=400, blank=True, null=True)
    latitude = models.DecimalField(default=0, decimal_places=10, max_digits=15,
                                   blank=True, null=True)
    longitude = models.DecimalField(default=0, decimal_places=10,
                                    max_digits=15, blank=True, null=True)
    map_zoom_level = models.IntegerField(default=13)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    no_of_members = models.CharField(max_length=200, null=True, blank=True)
    membership_fee = models.CharField(max_length=200, null=True, blank=True)
    date_of_founding = models.CharField(max_length=200, null=True, blank=True)
    last_updated_external = models.CharField(max_length=200, null=True,
                                             blank=True)
    admins = models.ManyToManyField(User, null=True, blank=True,
                                    related_name='space_admins')
    members = models.ManyToManyField(User, null=True, blank=True,
                                    related_name='space_members')
    inventory = models.ManyToManyField('Part', through='Inventory',
                                       related_name='space_inventory')

    class Meta:
        app_label = 'erp'

    def __unicode__(self):
        return self.name

    def pub_date(self):
        return self.added_time

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super(Space, self).save(*args, **kwargs)


class Part(BaseModel):
    name = models.TextField()
    url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        app_label = 'erp'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if(self.url and self.url[:4] != "http"):
            self.url = "http://" + self.url

        self.modified_time = timezone.now()
        super(Part, self).save(*args, **kwargs)


class Inventory(BaseModel):
    part = models.ForeignKey('Part', related_name='inventory_part')
    space = models.ForeignKey(Space, related_name='inventory_space')
    quantity = models.IntegerField(default=1, null=True, blank=True)
    owner = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'erp'

    def __unicode__(self):
        return '(%s - %s - %s)' % (self.space, self.part, self.quantity)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super(Inventory, self).save(*args, **kwargs)
