from datetime import timedelta
from decimal import Decimal
import math
    
    
class Meridian_Passage(object):
    def __init__(self, celestial_body, limb, passage_lmt, time_zone, dr_longitude):
        
        def calc_utc(local_datetime, time_zone):
            calc_utc = local_datetime - timedelta(hours=time_zone)
            return calc_utc
        
        def convert_longitude(longitude_str):
            degrees = Decimal(longitude_str[0:3])
            minutes = (Decimal(longitude_str[4:8]))/60
            long_dec = degrees + minutes
            long_hemisphere = longitude_str[8:9]
            if long_hemisphere=="W":
                long_dec = long_dec = long_dec * -1
            return long_dec
        
        def calc_arc_to_time(longitude): 
            arc = (longitude / 15)
            return  arc

        def calc_time_of_pass(passage_lmt, time_zone, arc_to_time):
            arc_to_time = float(arc_to_time)
            time_of_pass = (passage_lmt - timedelta(hours=arc_to_time)) + timedelta(hours=time_zone)
            return time_of_pass
        
        def calc_interpolation_factor(minute, second):
            if second == 0:
                return minute / 60.0
            else:
                return minute / 60.0 + second / 3600.0

        self.celestial_body = celestial_body
        self.limb = limb
        self.passage_lmt = passage_lmt
        self.time_zone = time_zone
        self.dr_longitude_str = dr_longitude
        self.dr_longitude_dec = convert_longitude(self.dr_longitude_str)
        self.arc_to_time = calc_arc_to_time(self.dr_longitude_dec)
        self.passage_local = calc_time_of_pass(self.passage_lmt, self.time_zone, self.arc_to_time)
        self.passage_utc = calc_utc(self.passage_local, self.time_zone)
        self.interpolation_factor = calc_interpolation_factor(self.passage_utc.minute, self.passage_utc.second)
        
             
class Meridian_Sight(object):
    
    def __init__(self, bearing, eye_height, celestial_body, limb, index_error, temperature, pressure, semi_diameter, 
                 height_sextant, dec_0, dec_1, interpolation_factor):

        def convert_error(minute_str):
            minutes = float(minute_str[1:5])/60
            minutes_sign = minute_str[0:1]
            if minutes_sign=="-":
                minutes = minutes * -1
            return minutes
        
        def convert_temperature(temperature_str):
            temperature = float(temperature_str[1:3])
            temperature_sign = temperature_str[0:1]
            if temperature_sign=="-":
                temperature = temperature * -1
            return temperature
        
        def convert_pressure(pressure_str):
            pressure = float(pressure_str[0:4])
            return pressure
        
        def convert_semi_diameter(sd_str):
            sd = float((sd_str[0:4]))/60
            if self.limb == "Upper":
                sd = sd * -1
            return sd
        
        def convert_height_sextant(hs_str):
            hs_degrees = float(hs_str[0:2])
            hs_minutes = float(hs_str[3:7])/60
            hs = hs_degrees + hs_minutes
            return hs
        
        def calculate_declination(dec_0, dec_1, interpolation_factor):

            def convert_dec(dec):
                dec_sign = dec[0:1]
                dec_degrees = float(dec[1:3])
                dec_minutes = float(dec[4:8])/60
                declination = dec_degrees + dec_minutes
                if dec_sign == "-":
                    declination = declination * -1
                return declination
            
            dec_a = convert_dec(dec_0)
            dec_b = convert_dec(dec_1)
            declination = dec_a + interpolation_factor * (dec_b - dec_a)
            return declination

        self.bearing_of_body = bearing
        self.eye_height = eye_height
        self.celestial_body = celestial_body
        self.limb = limb
        self.index_error = index_error
        self.error = convert_error(self.index_error)
        self.temperature = temperature
        self.temp = convert_temperature(self.temperature)
        self.pressure = pressure
        self.press = convert_pressure(self.pressure)
        self.semi_diameter = semi_diameter
        self.sd = convert_semi_diameter(self.semi_diameter)
        self.height_sextant = height_sextant
        self.hs = convert_height_sextant(self.height_sextant)
        self.declination = calculate_declination(dec_0, dec_1, interpolation_factor)     
        self.height_observed = 0.0
        self.latitude = "Not Calculated"    

    def calc_height_observed(self):
        k = math.pi/180
        dip = 0.0293 * math.sqrt(self.eye_height)
        apparent_altitude = self.hs + self.error - dip
        r = 0.0167 / (math.tan((apparent_altitude + 7.32 / (apparent_altitude + 4.32)) * k))
        f = (0.23 * self.press) / (self.temp + 273)
        refraction = r * f
        if self.celestial_body == "Sun":
            pa = 0.0024 * math.cos(apparent_altitude * k)
            self.height_observed = apparent_altitude - refraction + pa + self.sd

    def calc_latitude(self):
        def convert_latitude(latitude):
            lat_deg = math.floor(latitude)
            lat_min = (latitude - lat_deg) * 60.0
            lat_min = round(lat_min,1)
            latitude = f"{lat_deg} {lat_min}"
            return latitude 

        meridian_zenith_distance = 90.0 - self.height_observed
        if self.bearing_of_body == "North":
            meridian_Zenith_name = "South"
        else:
            meridian_Zenith_name = "North"
        if self.declination <= 0:
            dec_name = "South"
        else:
            dec_name = "North"
        if dec_name == meridian_Zenith_name:
            latitude = meridian_zenith_distance + abs(self.declination)
        else:
            latitude = meridian_zenith_distance - abs(self.declination)
        self.latitude = convert_latitude(latitude)