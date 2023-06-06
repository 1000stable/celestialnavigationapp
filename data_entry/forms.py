# import form class from django
from django import forms

#import models from sight/models.py
from .models import Meridian_Passage_Sight, Meridian_Passage_Entry, SunriseSunsetEntry, SightEntry, SightAlmanacEntry, StarFinderTime, StarFinderGhaAries

#Create a Meriidan_Passage_EntryForm
class Meridian_Passage_EntryForm(forms.ModelForm):
    # specify the name of the model to use
    class Meta:
        model = Meridian_Passage_Entry
        fields = "__all__"    


#Create a Meridian_Passage_Sight_Form
class Meridian_Passage_SightForm(forms.ModelForm):
    #specifiy the name of the model to use
    class Meta:
        model = Meridian_Passage_Sight
        fields = "__all__"   


#Create a SunriseSunsetForm
class SunriseSunsetEntryForm(forms.ModelForm):
    #specifiy the name of the model to use
    class Meta:
        model = SunriseSunsetEntry
        fields = "__all__"  

#Create a SightEntryForm
class SightEntryForm(forms.ModelForm):
    #specify the name of model to use
    class Meta:
        model = SightEntry
        fields = "__all__"

#Create a SightAlmanacEntryForm
class SightAlmanacEntryForm(forms.ModelForm):
    #specify the name of model to use
    class Meta:
        model = SightAlmanacEntry
        fields = "__all__"

#Create a StarFinderTimeForm
class StarFinderTimeEntryForm(forms.ModelForm):
    #specify the name of model to use
    class Meta:
        model = StarFinderTime
        fields = "__all__"

#Create a StarFinderGhaAriesForm
class StarFinderGhaAriesEntryForm(forms.ModelForm):
    #specify the name of model to use
    class Meta:
        model = StarFinderGhaAries
        fields = "__all__"