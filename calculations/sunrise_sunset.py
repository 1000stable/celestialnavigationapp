from datetime import timedelta
from decimal import Decimal
import math
    
    
class Sunrise_Sunset(object):
    # General Solar position Calculations - NOAA Global Monitoring Division
    def __init__(self, day, time_zone, latitude, longitude):

        def convert_longitude(longitude_str):
            degrees = float(longitude_str[0:3])
            minutes = (float(longitude_str[4:8]))/60
            long_dec = degrees + minutes
            long_hemisphere = longitude_str[8:9]
            if long_hemisphere=="W":
                long_dec = long_dec = long_dec * -1
            return long_dec
        
        def convert_latitude(latitude_str):
            degrees = float(latitude_str[0:2])
            minutes = (float(latitude_str[3:7]))/60
            lat_dec = degrees + minutes
            lat_hemisphere = latitude_str[7:8]
            if lat_hemisphere=="S":
                lat_dec = lat_dec = lat_dec * -1
            return lat_dec

        def is_leap_year(year):
            year_num = int(year)
            if year_num < 1 or year_num > 9999:
                return False
            if year_num % 4 != 0:
                return False
            if year_num % 100 == 0:
                if year_num % 400 == 0:
                    return True
                return False
            return True

        def day_of_year(month, day, is_leap_year):
            # given year, month, day return day of year Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7
            month_num = int(month)
            day_num = int(day)
            if is_leap_year:
                K = 1
            else:
                K = 2
            N = int((275 * month_num) / 9.0) - K * int((month_num + 9) / 12.0) + day_num - 30
            return N
        
        def fraction_of_year(day_of_year, is_leap_year):
            hour = 12
            if is_leap_year:
                fraction = ((2 * math.pi) / 366) * (day_of_year - 1 + ((hour - 12)/ 24))
            else:
                fraction = ((2 * math.pi) / 365) * (day_of_year - 1 + ((hour - 12)/ 24))
            print(fraction)
            return fraction 
        
        def equation_of_time(fractional_year):
            eqn_time = 229.18 * (0.000075 + (0.001868 * math.cos(fractional_year)) -  (0.032077 * math.sin(fractional_year)) -
            (0.014615 * math.cos(2 * fractional_year)) - (0.040849 * math.sin(2 * fractional_year)))
            return eqn_time
        
        def calc_declination(fractional_year):
            dec = (0.006918 
            - (0.399912 * math.cos(fractional_year)) 
            + (0.070257 * math.sin(fractional_year)) 
            - (0.006758 * math.cos(2 * fractional_year)) 
            + (0.000907 * math.sin(2 * fractional_year)) 
            - (0.002697 * math.cos(3 * fractional_year)) 
            + (0.00148 * math.sin(3 * fractional_year)))
            print(dec)
            return dec
        
        def calc_time_offset(eqn_of_time, longitude_dec, time_zone):
            offset = eqn_of_time + (4 * longitude_dec) - (60 * time_zone)
            return offset
        
        def calc_true_solar_time(longitude_dec, time_zone):
            tst = (12 * 60) + (4 * longitude_dec) - time_zone
            return tst
        
        def calc_hour_angle(latitude, declination):
            k = math.pi / 180
            a = math.cos(90.833 * k)
            b = math.cos(latitude * k)
            c = math.cos(declination)
            d = math.tan(latitude * k)
            e = math.tan(declination)
            f = (a /(b * c)) - (d * e)
            ha =  (math.acos(f) / k)
            return ha
    
        def calc_sunrise(hour_angle, time_offset):
            sr = 720 - time_offset - ((hour_angle * 60) / 15)
            return sr
        
        def calc_sunset(hour_angle, time_offset):
            ss = 720 - time_offset + ((hour_angle * 60) / 15)
            return ss
        
        def convert_sun(time):
            time_in_hours = time / 60.0
            time_hours = math.floor((time_in_hours))
            print(time_hours)
            time_minutes = math.floor(((time_in_hours - time_hours) * 60.0))
            time_minutes = round(time_minutes, 0)
            print(time_minutes)
            if time_hours < 10:
                hour_str = f"0{time_hours}"
            else:
                hour_str = f"{time_hours}"
            if time_minutes < 10:
                minute_str = f"0{time_minutes}"
            else:
                minute_str = f"{time_minutes}"
            time_str = hour_str + minute_str
            return time_str
   
        self.day = day
        self.time_zone = time_zone
        self.latitude_str = latitude
        self.latitude_dec = convert_latitude(self.latitude_str)
        self.longitude_str = longitude
        self.longitude_dec = convert_longitude(self.longitude_str)
        self.leap_year = is_leap_year(self.day.year)
        self.month = int(self.day.month)
        self.day_of_year = day_of_year(self.month, self.day.day, self.leap_year)
        self.fraction_of_year = fraction_of_year(self.day_of_year, self.leap_year)
        self.equation_of_time = equation_of_time(self.fraction_of_year)
        self.declination = calc_declination(self.fraction_of_year)
        self.time_offset = calc_time_offset(self.equation_of_time, self.longitude_dec, self.time_zone)
        self.true_solar_time = calc_true_solar_time(self.longitude_dec, self.time_zone)
        self.hour_angle = calc_hour_angle(self.latitude_dec, self.declination)      
        self.sunrise_num = calc_sunrise(self.hour_angle, self.time_offset)
        self.sunrise = convert_sun(self.sunrise_num)
        self.sunset_num = calc_sunset(self.hour_angle, self.time_offset)
        self.sunset = convert_sun(self.sunset_num)
