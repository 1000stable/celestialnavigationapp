from datetime import timedelta
from decimal import Decimal
import math
    
    
class TimeEntry(object):
    # General Solar position Calculations - NOAA Global Monitoring Division
    def __init__(self, sight_time_lmt, time_zone, dr_longitude): 
        
        def calc_utc(local_datetime, time_zone):
            utc = local_datetime - timedelta(hours=time_zone) 
            return utc
        
        def calc_interpolation_factor(minute, second):
            if second == 0:
                return minute / 60.0
            else:
                return minute / 60.0 + second / 3600.0

        def convert_longitude(longitude_str):
            #takes a longitude string and converts it to a float value so that it may be used
            #in calculations.  Used also in sunrise_set.py.  TODO put this in another class?
            degrees = float(longitude_str[0:3])
            minutes = (float(longitude_str[4:8]))/60
            long_float = degrees + minutes
            long_hemisphere = longitude_str[8:9]
            if long_hemisphere=="W":
                long_float = long_float = long_float * -1
            return long_float
   
        self.sight_time_lmt = sight_time_lmt
        self.time_zone = time_zone
        self.sight_time_utc = calc_utc(self.sight_time_lmt, self.time_zone)
        self.interpolation_factor = calc_interpolation_factor(self.sight_time_utc.minute, self.sight_time_utc.second)
        self.dr_longitude_str = dr_longitude
        self.dr_longitude_float = convert_longitude(self.dr_longitude_str)
        
    
    
class GhaEntry(object):

    def __init__(self, interpolation_factor, longitude, gha_0, gha_1):
        
        def convert_gha(gha_str):
            #takes a gha string formatted DDD MM.M and converts to float
            degrees = float(gha_str[0:4])
            minutes = float((gha_str[4:8]))/60.0
            gha_float = degrees + minutes
            return gha_float
        
        def interpolate_gha(gha_0, gha_1, interpolation_factor):
            #If GHA passes through 360 between Almanac tabulated values add 360 to the second tabulated value - gha_1
            if gha_1 < gha_0:
                gha_0 = gha_0 + 360.0

            interpolated_gha = gha_0 + interpolation_factor * (gha_1 - gha_0)

            #If interpolated gha exceeds 360 subtract 360 from interpolate_gha
            if interpolated_gha > 360:
                interpolated_gha = interpolated_gha - 360.0

            return interpolated_gha
        
        self.interpolation_factor = interpolation_factor
        self.longitude = longitude
        self.gha_0_str = gha_0
        self.gha_0_float = convert_gha(self.gha_0_str)
        self.gha_1_str = gha_1
        self.gha_1_float = convert_gha(self.gha_1_str)
        self.gha = interpolate_gha(self.gha_0_float, self.gha_1_float, self.interpolation_factor)
       

class LhaCalculation(object):

    def __init__(self, gha, longitude):
        
        def calculate_lha(gha, longitude):
            lha = gha + longitude
            if lha < 0:
                lha = lha + 360
            if lha > 360:
                lha = lha - 360         
            return lha

        self.lha = calculate_lha(gha, longitude)

