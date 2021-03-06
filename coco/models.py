import datetime
from django.db import models
from log.utils import delete_log, save_log

class Village(models.Model):
    name = models.CharField(max_length=100)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

TYPE = (
    ('Pr', 'Pregnant'),
    ('La', 'Lactating'),
    ('Mil', 'Mother-in-law'),
    ('Sil', 'Sister-in-law'),
    ('Pra', 'Pradhan'),
    ('Anm', 'ANM'),
    ('Asha', 'ASHA'),
)

class Person(models.Model):
    name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    type = models.CharField(max_length=5, choices=TYPE)
    delivery_date = models.DateField(null=True, blank=True)
    village = models.ForeignKey(Village)
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.other_name)
models.signals.post_save.connect(save_log, sender = Person)
models.signals.pre_delete.connect(delete_log, sender = Person)

class Mediator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    villages = models.ManyToManyField(Village)
models.signals.post_save.connect(save_log, sender = Mediator)
models.signals.pre_delete.connect(delete_log, sender = Mediator)

class Video(models.Model):
    title = models.CharField(max_length=100, unique=True)
models.signals.post_save.connect(save_log, sender = Video)
models.signals.pre_delete.connect(delete_log, sender = Video)

class Dissemination(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    village = models.ForeignKey(Village)
    video = models.ForeignKey(Video)
    
    mediator = models.ForeignKey(Mediator)
    song = models.BooleanField()
    game = models.BooleanField()
    
    total_households = models.PositiveIntegerField(null=True, blank=True)
    total_new_households = models.PositiveIntegerField(null=True, blank=True)
    total_pregnant_women = models.PositiveIntegerField(null=True, blank=True)
    total_lactating_women = models.PositiveIntegerField(null=True, blank=True)
    
    attendance_records = models.ManyToManyField(Person, through='Attendance')
    class Meta:
        unique_together = ('date', "start_time", "end_time", "mediator", "village")
models.signals.post_save.connect(save_log, sender = Dissemination)
models.signals.pre_delete.connect(delete_log, sender = Dissemination)

class Attendance(models.Model):
    person = models.ForeignKey(Person)
    dissemination = models.ForeignKey(Dissemination)
    question_asked = models.CharField(max_length=200, blank=True)
    liked = models.BooleanField(default=False)

class Adoption(models.Model):
    person = models.ForeignKey(Person)
    mediator = models.ForeignKey(Mediator)
    delivery_date = models.DateField()
    date_of_visit = models.DateField()
    checked_by = models.CharField(null=True, blank=True, max_length=100)
    place_of_birth = models.CharField(null=True, blank=True, max_length=100)
    preparation_of_last_delivery = models.CharField(null=True, blank=True, max_length=100)
    cord_care = models.CharField(null=True, blank=True, max_length=100)
    cord_cut = models.CharField(null=True, blank=True, max_length=100)
    baby_bathe = models.CharField(null=True, blank=True, max_length=100)
    wiped = models.CharField(null=True, blank=True, max_length=100)
    baby_wrap = models.CharField(null=True, blank=True, max_length=100)
    baby_hold = models.CharField(null=True, blank=True, max_length=100)
    baby_colostrums = models.CharField(null=True, blank=True, max_length=100)
    breastfeed = models.CharField(null=True, blank=True, max_length=100)
    feed = models.CharField(null=True, blank=True, max_length=100)
    other_food = models.CharField(null=True, blank=True, max_length=100)
    liquids = models.CharField(null=True, blank=True, max_length=100)
    family_planning = models.CharField(null=True, blank=True, max_length=100)
    fp_method = models.CharField(null=True, blank=True, max_length=100)
    fp_awareness = models.CharField(null=True, blank=True, max_length=100)
    fp_service_providers = models.CharField(null=True, blank=True, max_length=100)
    fp_family_discussion = models.CharField(null=True, blank=True, max_length=100)
    fp_family_member = models.CharField(null=True, blank=True, max_length=100)
    fp_use = models.CharField(null=True, blank=True, max_length=100)

