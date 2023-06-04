from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import Meridian_Passage_SightForm, Meridian_Passage_EntryForm, SightEntryForm, SunriseSunsetEntryForm
from .models import Meridian_Passage_Entry, Meridian_Passage_Sight, SunriseSunsetEntry, SightEntry
from calculations import meridian_altitude, sunrise_sunset, sight
from django.http import HttpResponse
from django.template import loader



# Create your views here.
class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request):
            args = {}
            return render(request, self.template_name, args)

    def post(self, request):        
        args = {}
        return redirect(request, self.template_name, args)
    

class Meridian_Passage_EntryView(TemplateView):
    template_name = 'meridian_passage_entry.html'

    def get(self, request):
        form = Meridian_Passage_EntryForm()
        args={'form':form}
        return render(request, self.template_name, args)


    def post(self, request):
        form = Meridian_Passage_EntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('latitude_entry')

        return redirect('meridian_passage_entry')
    

class LatitudeView(TemplateView):
    template_name = 'latitude_entry.html'

    def get(self, request):
        form = Meridian_Passage_SightForm()
        if Meridian_Passage_Entry.objects.all().first():
            this_passage = meridian_altitude.Meridian_Passage(
                Meridian_Passage_Entry.objects.all()[0].celestial_body,
                Meridian_Passage_Entry.objects.all()[0].limb,
                Meridian_Passage_Entry.objects.all()[0].passage_lmt,
                Meridian_Passage_Entry.objects.all()[0].time_zone,
                Meridian_Passage_Entry.objects.all()[0].dr_longitude
            )

            time_of_passage_local = this_passage.passage_local
            time_of_passage_utc = this_passage.passage_utc
            celestial_body = this_passage.celestial_body
            limb = this_passage.limb

            args = {'form':form, 'time_of_passage_local':time_of_passage_local, 'time_of_passage_utc':time_of_passage_utc,
                    'celestial_body':celestial_body, 'limb':limb}

            return render(request, self.template_name, args)
        
   
    def post(self, request):
        form = Meridian_Passage_SightForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('latitude_result')

        return redirect('latitude_result')
    
   
class Latitude_ResultView(TemplateView):
    template_name = 'latitude_result.html'

    def get(self, request):
        this_passage = meridian_altitude.Meridian_Passage(
            Meridian_Passage_Entry.objects.all()[0].celestial_body,
            Meridian_Passage_Entry.objects.all()[0].limb,
            Meridian_Passage_Entry.objects.all()[0].passage_lmt,
            Meridian_Passage_Entry.objects.all()[0].time_zone,
            Meridian_Passage_Entry.objects.all()[0].dr_longitude
            )
        this_sight = meridian_altitude.Meridian_Sight(
            Meridian_Passage_Sight.objects.all()[0].bearing_of_body,
            Meridian_Passage_Sight.objects.all()[0].eye_height,
            Meridian_Passage_Entry.objects.all()[0].celestial_body,
            Meridian_Passage_Entry.objects.all()[0].limb,
            Meridian_Passage_Sight.objects.all()[0].index_error,
            Meridian_Passage_Sight.objects.all()[0].temperature,
            Meridian_Passage_Sight.objects.all()[0].pressure,
            Meridian_Passage_Sight.objects.all()[0].semi_diameter,
            Meridian_Passage_Sight.objects.all()[0].height_sextant,
            Meridian_Passage_Sight.objects.all()[0].dec_0,
            Meridian_Passage_Sight.objects.all()[0].dec_1,
            this_passage.interpolation_factor
            )
        
        #delete record filtered on sight_number which is unique.
        sight_number_to_delete = 1
        Meridian_Passage_Entry.objects.filter(sight_number=sight_number_to_delete).delete()
        Meridian_Passage_Sight.objects.filter(sight_number=sight_number_to_delete).delete()

        this_sight.calc_height_observed()
        this_sight.calc_latitude()
        latitude = this_sight.latitude

        args = {'latitude':latitude}

        return render(request, self.template_name, args)


class SunriseSunsetEntryView(TemplateView):
    template_name = 'sunrise_sunset_entry.html'

    def get(self, request):
        form = SunriseSunsetEntryForm()
        args={'form':form}
        return render(request, self.template_name, args)


    def post(self, request):
        form = SunriseSunsetEntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sunrise_sunset_result')

        return redirect('sunrise_sunset_entry')
    
   
class SunriseSunsetResultView(TemplateView):
    template_name = 'sunrise_sunset_result.html'

    def get(self, request):
        this_calc = sunrise_sunset.Sunrise_Sunset(
            SunriseSunsetEntry.objects.all()[0].day,
            SunriseSunsetEntry.objects.all()[0].time_zone,
            SunriseSunsetEntry.objects.all()[0].latitude,
            SunriseSunsetEntry.objects.all()[0].longitude
            )
        
        #delete record filtered on calcl_number which is unique.
        calc_number_to_delete = 1
        SunriseSunsetEntry.objects.filter(calc_number=calc_number_to_delete).delete()
        
        sunrise = this_calc.sunrise
        sunset = this_calc.sunset

        args = {'sunrise':sunrise, 'sunset':sunset}

        return render(request, self.template_name, args)


class SightEntryView(TemplateView):
    template_name = 'sight_entry.html'

    def get(self, request):
        form = SightEntryForm()
        args={'form':form}
        return render(request, self.template_name, args)


    def post(self, request):
        form = SightEntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sight_result')

        return redirect('sight_entry')
    
class SightResultView(TemplateView):
    template_name = 'sight_result.html'

    def get(self, request):
        this_calc = sight.Sight(
            SightEntry.objects.all()[0].celestial_body,
            SightEntry.objects.all()[0].limb,
            SightEntry.objects.all()[0].sight_time_lmt,
            SightEntry.objects.all()[0].clock_error,
            SightEntry.objects.all()[0].time_zone,
            SightEntry.objects.all()[0].dr_latitude,
            SightEntry.objects.all()[0].dr_longitude,
            SightEntry.objects.all()[0].eye_height,
            SightEntry.objects.all()[0].index_error,
            SightEntry.objects.all()[0].temperature,
            SightEntry.objects.all()[0].pressure,
            SightEntry.objects.all()[0].height_sextant,
            SightEntry.objects.all()[0].morning,
            SightEntry.objects.all()[0].dec_0,
            SightEntry.objects.all()[0].dec_1,
            SightEntry.objects.all()[0].gha_0,
            SightEntry.objects.all()[0].gha_1,
            SightEntry.objects.all()[0].sha,
            SightEntry.objects.all()[0].semi_diameter
            )
        
        #TODO: Output UTC time of sight so Almanac can be accessed
        #return HttpResponse("UTC")
    
        #delete record filtered on calc_number which is unique.
        calc_number_to_delete = 1
        SightEntry.objects.filter(sight_number=calc_number_to_delete).delete()
        
        sight_utc = this_calc.sight_time_utc
        sight_drlatitude = this_calc.dr_latitude_str
        sight_drlongitude = this_calc.dr_longitude_str
        sight_plot = this_calc.plot

        args = {'sight_utc':sight_utc,
                'sight_drlatitude':sight_drlatitude,
                'sight_drlongitude':sight_drlongitude,
                'sight_plot':sight_plot}

        return render(request, self.template_name, args)