from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import Meridian_Passage_SightForm, Meridian_Passage_EntryForm, SightEntryForm, SightAlmanacEntryForm, SunriseSunsetEntryForm, StarFinderTimeEntryForm, StarFinderGhaAriesEntryForm
from .models import Meridian_Passage_Entry, Meridian_Passage_Sight, SunriseSunsetEntry, SightEntry, SightAlmanacEntry, StarFinderTime, StarFinderGhaAries
from calculations import meridian_altitude, sunrise_sunset, sight, starfinder
from django.http import HttpResponse
from django.template import loader


def check_longitude_format(longitude):
    if len(longitude) == 9:
        if  (longitude[0] in ["0","1"] and
            longitude[1] in ["0","1","2","3","4","5","6","7","8","9"] and
            longitude[2] in ["0","1","2","3","4","5","6","7","8","9"] and
            longitude[3] == " " and
            longitude[4] in ["0","1","2","3","4","5"] and
            longitude[5] in ["0","1","2","3","4","5","6","7","8","9"] and
            longitude[6] == "." and
            longitude[7] in ["0","1","2","3","4","5","6","7","8","9"] and
            longitude[8] in ["E", "W"]):
            return True
    return False
        

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
            if check_longitude_format(form.cleaned_data['dr_longitude']):
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
            return redirect('sight_almanac_entry')

        return redirect('sight_entry')

    
class SightAlmanacEntryView(TemplateView):
    template_name = 'sight_almanac_entry.html'

    def get(self, request):
        form = SightAlmanacEntryForm()
        if SightEntry.objects.all().first():
            this_sight = sight.SightEntry(
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
                SightEntry.objects.all()[0].morning
                ) 
        sight_utc = this_sight.sight_time_utc    

        args={'form':form,'sight_utc':sight_utc}

        return render(request, self.template_name, args)
    
    def post(self, request):
        form = SightAlmanacEntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sight_result')
        
        return redirect('sight_almanac_entry')


class SightResultView(TemplateView):
    template_name = 'sight_result.html'

    def get(self, request):
        this_sight = sight.SightEntry(
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
            SightEntry.objects.all()[0].morning
            )
        this_almanac = sight.SightAlmanacEntry(
            this_sight.interpolation_factor,
            this_sight.limb,
            SightAlmanacEntry.objects.all()[0].dec_0,
            SightAlmanacEntry.objects.all()[0].dec_1,
            SightAlmanacEntry.objects.all()[0].gha_0,
            SightAlmanacEntry.objects.all()[0].gha_1,
            SightAlmanacEntry.objects.all()[0].sha,
            SightAlmanacEntry.objects.all()[0].semi_diameter
            )
        
        #TODO: Output UTC time of sight so Almanac can be accessed
        #return HttpResponse("UTC")
    
        #delete record filtered on calc_number which is unique.
        calc_number_to_delete = 1
        SightEntry.objects.filter(sight_number=calc_number_to_delete).delete()
        SightAlmanacEntry.objects.filter(sight_number=calc_number_to_delete).delete()
        
        this_calc = sight.SightCalculation(
            this_sight.dr_latitude_float,
            this_sight.dr_longitude_float,
            this_sight.eye_height,
            this_sight.height_sextant_float,
            this_sight.index_error_float,
            this_sight.pressure_float,
            this_sight.temperature_float,
            this_sight.celestial_body,
            this_almanac.dec,
            this_almanac.gha,
            this_almanac.semi_diameter_float
        )
        sight_utc = this_sight.sight_time_utc
        sight_drlatitude = this_sight.dr_latitude_str
        sight_drlongitude = this_sight.dr_longitude_str
        sight_plot = this_calc.plot

        args = {'sight_utc':sight_utc,
                'sight_drlatitude':sight_drlatitude,
                'sight_drlongitude':sight_drlongitude,
                'sight_plot':sight_plot}

        return render(request, self.template_name, args)
    

class StarFinderTimeEntryView(TemplateView):
    template_name = 'star_finder_time_entry.html'

    def get(self, request):
        form = StarFinderTimeEntryForm
        args={'form':form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = StarFinderTimeEntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('star_finder_gha_aries_entry')

        return redirect('star_finder_time_entry')
    

class StarFinderGhaAriesEntryView(TemplateView):
    template_name = 'star_finder_gha_aries_entry.html'

    def get(self, request):
        form = StarFinderGhaAriesEntryForm()
        if StarFinderTime.objects.all().first():
            this_starfinder_time = starfinder.TimeEntry(
                StarFinderTime.objects.all()[0].sight_time_lmt,
                StarFinderTime.objects.all()[0].time_zone,
                StarFinderTime.objects.all()[0].dr_longitude
                ) 
        sight_utc = this_starfinder_time.sight_time_utc    

        args={'form':form,'sight_utc':sight_utc}

        return render(request, self.template_name, args)
    
    def post(self, request):
        form = StarFinderGhaAriesEntryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('star_finder_lha_aries_result')
        
        return redirect('star_finder_gha_aries_entry')

class StarFinderLhaAriesResultView(TemplateView):
    template_name = 'star_finder_lha_aries_result.html'

    def get(self, request):
        this_starfinder_time = starfinder.TimeEntry(
                StarFinderTime.objects.all()[0].sight_time_lmt,
                StarFinderTime.objects.all()[0].time_zone,
                StarFinderTime.objects.all()[0].dr_longitude
                ) 
        this_starfinder_gha = starfinder.GhaEntry(
            this_starfinder_time.interpolation_factor,
            this_starfinder_time.dr_longitude_float,
            StarFinderGhaAries.objects.all()[0].gha_0,
            StarFinderGhaAries.objects.all()[0].gha_1
            )
        star_finder_utc = this_starfinder_time.sight_time_utc
        star_finder_drlongitude = this_starfinder_time.dr_longitude_str
    
        #delete record filtered on calc_number which is unique.
        calc_number_to_delete = 1
        StarFinderTime.objects.filter(calc_number=calc_number_to_delete).delete()
        StarFinderGhaAries.objects.filter(calc_number=calc_number_to_delete).delete()
        
        this_lha = starfinder.LhaCalculation(
            this_starfinder_gha.gha,
            this_starfinder_time.dr_longitude_float
        )

        star_finder_lha_aries = this_lha.lha

        args = {'star_finder_utc':star_finder_utc,
                'star_finder_drlongitude':star_finder_drlongitude,
                'star_finder_lha_aries':star_finder_lha_aries
                }

        return render(request, self.template_name, args)
    