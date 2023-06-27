import datetime
from django.db import models

# Create your models here
class Meridian_Passage_Entry(models.Model):
    sight_number = models.IntegerField(default=1, unique=True)

    SUN='Sun'
    MOON='Moon'
    PLANET='Planet'
    STAR='Star'
    CELESTIAL_BODY_CHOICES=[
        ('Sun','Sun'),
        ('Moon','Moon'),
        ('Planet','Planet'),
        ('Star','Star'),
    ]
    celestial_body = models.CharField(
        max_length=6,
        choices=CELESTIAL_BODY_CHOICES,
        default=SUN,
        )
    
    UPPER ='Upper'
    LOWER='Lower'
    NA = 'Not Apllicable'
    LIMB_CHOICES=[
        ('Upper','Upper'),
        ('Lower','Lower'),
        ('Not Applicable','Not Applicable'),
    ]
    limb = models.CharField(
        max_length=14,
        choices=LIMB_CHOICES,
        default=LOWER,
        )

    passage_lmt = models.DateTimeField(blank=False, default="2023-01-01 00:00:00")
    time_zone = models.IntegerField(default=12)
    dr_longitude = models.CharField(max_length=9, null=True, verbose_name = "DR Longitude", default = "000 00.0E")
 
 
class Meridian_Passage_Sight(models.Model):   
    sight_number = models.IntegerField(default=1, unique=True)

    NORTH='North'
    SOUTH='South'
    BEARING_CHOICES=[
        ('North','North'),
        ('South','South'),
    ]
    bearing_of_body = models.CharField(
        max_length=5,
        choices=BEARING_CHOICES,
        default=NORTH,
        )

    eye_height = models.FloatField(default=0.0)
    index_error = models.CharField(max_length=5, default="+00.0", help_text="+MM.M + = off arc, - = on arc")
    temperature = models.CharField(max_length=3, default="+15", help_text="+ or - degrees celsius")
    pressure = models.CharField(max_length=4, default="1013")
    height_sextant = models.CharField(max_length=7, default="00 00.0", help_text="DD MM.M")
    #morning = models.BooleanField(default=True)
    #clock_error = models.IntegerField(default=0)
    dec_0 = models.CharField(max_length=8, default="-00 00.0", help_text="-DD MM.M -South +North")
    dec_1 = models.CharField(max_length=8, default="-00 00.0", help_text="-DD MM.M -South +North")

    semi_diameter = models.CharField(max_length=4, default="00.0", help_text="MM.M")


class SunriseSunsetEntry(models.Model):
    calc_number = models.IntegerField(default=1, unique=True)
    day = models.DateField(blank=False, help_text="YYYY-MM-DD")
    time_zone = models.IntegerField(default=12)
    latitude = models.CharField(max_length=8, null=True, default = "00 00.0S", 
                                    help_text="DD MM.MX where X is either N(orth) or S(outh)")
    longitude = models.CharField(max_length=9, null=True, default = "000 00.0E", 
                                    help_text="DDD MM.MX where X is either W(est) or E(ast)")
    


class SightEntry(models.Model):
    sight_number = models.IntegerField(default=1, unique=True)

    SUN='Sun'
    MOON='Moon'
    PLANET='Planet'
    STAR='Star'
    CELESTIAL_BODY_CHOICES=[
        ('Sun','Sun'),
        ('Moon','Moon'),
        ('Planet','Planet'),
        ('Star','Star'),
    ]
    celestial_body = models.CharField(
        max_length=6,
        choices=CELESTIAL_BODY_CHOICES,
        default=SUN,
        )
    
    UPPER ='Upper'
    LOWER='Lower'
    NA = 'Not Apllicable'
    LIMB_CHOICES=[
        ('Upper','Upper'),
        ('Lower','Lower'),
        ('Not Applicable','Not Applicable'),
    ]
    limb = models.CharField(
        max_length=14,
        choices=LIMB_CHOICES,
        default=LOWER,
        )

    sight_time_lmt = models.DateTimeField(blank=False, help_text="YYYY-MM-DD HH:MM:SS")
    clock_error = models.CharField(max_length=4, default="-000", help_text="-SSS seconds -slow, +fast")
    time_zone = models.IntegerField(default=12)
    dr_latitude = models.CharField(max_length=8, null=True, default="00 00.0S",
                                   help_text="DD MM.MX where X is either S(outh) or N(orth)")
    dr_longitude = models.CharField(max_length=9, null=True, default = "000 00.0E", 
                                    help_text="DDD MM.MX where X is either W(est) or E(ast)")
    eye_height = models.FloatField(default=0.0)
    index_error = models.CharField(max_length=5, default="+00.0", help_text="+MM.M + = off arc, - = on arc")
    temperature = models.CharField(max_length=3, default="+15", help_text="+ or - degrees celsius")
    pressure = models.CharField(max_length=4, default="1013")
    height_sextant = models.CharField(max_length=7, default="00 00.0", help_text="DD MM.M")
    morning = models.BooleanField(default=True)

class SightAlmanacEntry(models.Model):
    sight_number = models.IntegerField(default=1, unique=True)
    dec_0 = models.CharField(max_length=8, default="-00 00.0", help_text="-DD MM.M -South +North")
    dec_1 = models.CharField(max_length=8, default="-00 00.0", help_text="-DD MM.M -South +North")
    gha_0 = models.CharField(max_length=8, default="000 00.0", help_text="DDD MM.M")
    gha_1 = models.CharField(max_length=8, default="000 00.0", help_text="DDD MM.M")
    sha = models.CharField(max_length=8, default="000 00.0", help_text="DDD MM.M")
    semi_diameter = models.CharField(max_length=4, default="00.0", help_text="MM.M")

class StarFinderTime(models.Model):
    calc_number = models.IntegerField(default=1, unique=True)
    sight_time_lmt = models.DateTimeField(blank=False, help_text="YYYY-MM-DD HH:MM:SS")
    time_zone = models.IntegerField(default=12)
    dr_longitude = models.CharField(max_length=9, null=True, default = "000 00.0E", 
                                    help_text="DDD MM.MX where X is either W(est) or E(ast)")
    
class StarFinderGhaAries(models.Model):
    calc_number = models.IntegerField(default=1, unique=True)
    gha_0 = models.CharField(max_length=8, default="000 00.0", help_text="DDD MM.M")
    gha_1 = models.CharField(max_length=8, default="000 00.0", help_text="DDD MM.M")

    