from datetime import timedelta
from decimal import Decimal
import math
    
    
class Sight(object):
    # General Solar position Calculations - NOAA Global Monitoring Division
    def __init__(self, celestial_body, limb, sight_time_lmt, clock_error, time_zone, dr_latitude, dr_longitude,
                 eye_height, index_error, temperature, pressure, height_sextant, morning, dec_0, dec_1, 
                 gha_0, gha_1, sha, semi_diameter):
        
        def convert_clock_error(clock_error_str):
            #takes clock error string ()"-SSS seconds -slow, +fast") and converts to an integer
            sign = clock_error_str[0:1]
            seconds = int(clock_error_str[1:4])
            if sign == "+":
                seconds = seconds * -1
            return seconds
        
        def calc_corrected_utc(local_datetime, clock_error, time_zone):
            corrected_utc = local_datetime + timedelta(seconds=clock_error) - timedelta(hours=time_zone) 
            return corrected_utc
        
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
        
        def convert_latitude(latitude_str):
            #takes a latitude string and converts it to a float value so that it may be used
            #in calculations. Used also in sunrise_set.py.  TODO put this in another class?
            degrees = float(latitude_str[0:2])
            minutes = (float(latitude_str[3:7]))/60
            lat_dec = degrees + minutes
            lat_hemisphere = latitude_str[7:8]
            if lat_hemisphere=="S":
                lat_dec = lat_dec = lat_dec * -1
            return lat_dec
        
        def convert_error(minute_str):
            #takes the index error string in the format "+MM.M + = off arc, - = on arc" and
            #converts it to a float value.
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
        
        def convert_height_sextant(hs_str):
            hs_degrees = float(hs_str[0:2])
            hs_minutes = float(hs_str[3:7])/60
            hs = hs_degrees + hs_minutes
            return hs
        
        def convert_semi_diameter(sd_str):
            sd = float((sd_str[0:4]))/60
            if self.limb == "Upper":
                sd = sd * -1
            return sd
        
        def convert_gha(gha_str):
            #takes a gha string formatted DDD MM.M and converts to float
            degrees = float(gha_str[0:4])
            minutes = float((gha_str[4:8]))/60.0
            gha_float = degrees + minutes
            return gha_float
        
        def convert_dec(dec_str):
            #takes a dec string formatted -DD MM.M and converts to float
            sign = dec_str[0:1]
            degrees = float(dec_str[1:3])
            minutes = float((dec_str[4:8]))/60.0
            dec_float = degrees + minutes
            if sign == "-":
                dec_float = dec_float * -1
            return dec_float
        
        def convert_sha(sha_str):
            #takes a gha string formatted DDD MM.M and converts to float
            degrees = float(sha_str[0:4])
            minutes = float((sha_str[4:8]))/60.0
            sha_float = degrees + minutes
            return sha_float

        def interpolate_dec(dec_0, dec_1, interpolation_factor):
            interpolated_dec = dec_0 + interpolation_factor * (dec_1 - dec_0)
            return interpolated_dec
        
        def interpolate_gha(gha_0, gha_1, interpolation_factor):
            #If GHA passes through 360 between Almanac tabulated values add 360 to the second tabulated value - gha_1
            if gha_1 < gha_0:
                gha_0 = gha_0 + 360.0

            interpolated_gha = gha_0 + interpolation_factor * (gha_1 - gha_0)

            #If interpolated gha exceeds 360 subtract 360 from interpolate_gha
            if interpolated_gha > 360:
                interpolated_gha = interpolated_gha - 360.0

            return interpolated_gha
        
        def calculate_lha(gha, longitude):
            lha = gha + longitude
            return lha

        def calculate_height_calculated(dec, lha, lat):
            k = math.pi / 180
            if lha < 360:
                lha = lha + 360
            else:
                lha = lha - 360
            s = math.sin(dec * k)
            c = (math.cos(dec * k)) * (math.cos(lha * k))
            hc = math.asin((s * math.sin(lat * k)) + (c * math.cos(lat * k))) / k
            return hc
        
        def calculate_azimuth_z(dec, lat, hc, lha):
            k = math.pi /180
            s = math.sin(dec * k)
            c = (math.cos(dec * k)) * (math.cos(lha * k))
            x = ((s * math.cos(lat * k)) - (c * math.sin(lat * k))) / math.cos(hc * k)
            if x > 1:
                x = 1
            if x <-1:
                x = -1
            a = math.acos(x)
            if lha > 180:
                z = a /k
            else:
                z = 360 - (a / k)
            return z
        
        def calculate_height_observed(eye_height, hs, error, press, temp, celestial_body, sd):
            k = math.pi/180
            dip = 0.0293 * math.sqrt(eye_height)
            apparent_altitude = hs + error - dip
            r = 0.0167 / (math.tan((apparent_altitude + 7.32 / (apparent_altitude + 4.32)) * k))
            f = (0.23 * press) / (temp + 273)
            refraction = r * f
            if celestial_body == "Sun":
                pa = 0.0024 * math.cos(apparent_altitude * k)
            else:
                #TODO: cater for moon venus and mars
                pa = 0
            height_observed = apparent_altitude - refraction + pa + sd
            return height_observed
        
        def create_plot_str(ho, hc, azimuth_z):
            p = ho - hc
            direction = ""
            if p > 0:
                direction = "towards"
            if p <= 0:
                direction = "away"
            nautical_miles = p * -60.0
            nm_str = f"{nautical_miles}"
            azimuth_str = f"{azimuth_z}"
            if azimuth_z < 100:
                plot_str = "0" + azimuth_str + "T / " + nm_str + "nm / " + direction
            if azimuth_z >= 100:
                plot_str = azimuth_str + "T / " + nm_str + "nm / " + direction
            return plot_str

        
        #just acode example of converting a number to a string
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
   
        self.celestial_body = celestial_body
        self.limb = limb
        self.sight_time_lmt = sight_time_lmt
        self.clock_error = clock_error
        self.clock_error_int = convert_clock_error(self.clock_error)
        self.time_zone = time_zone
        self.sight_time_utc = calc_corrected_utc(self.sight_time_lmt, self.clock_error_int, self.time_zone)
        self.interpolation_factor = calc_interpolation_factor(self.sight_time_utc.minute, self.sight_time_utc.second)
        self.dr_latitude_str = dr_latitude
        self.dr_latitude_float = convert_latitude(self.dr_latitude_str)
        self.dr_longitude_str = dr_longitude
        self.dr_longitude_float = convert_longitude(self.dr_longitude_str)
        self.eye_height = eye_height
        self.index_error = index_error
        self.index_error_float = convert_error(self.index_error)
        self.temperature_str = temperature
        self.temperature_float = convert_temperature(self.temperature_str)
        self.pressure_str = pressure
        self.pressure_float = convert_pressure(self.temperature_str)
        self.height_sextant_str = height_sextant
        self.height_sextant_float = convert_height_sextant(self.height_sextant_str)
        self.morning = morning
        self.dec_0_str = dec_0
        self.dec_0_float = convert_dec(self.dec_0_str)
        self.dec_1_str = dec_1
        self.dec_1_float = convert_dec(self.dec_1_str)
        self.dec = interpolate_dec(self.dec_0_float, self.dec_1_float, self.interpolation_factor)
        self.gha_0_str = gha_0
        self.gha_0_float = convert_gha(self.gha_0_str)
        self.gha_1_str = gha_1
        self.gha_1_float = convert_gha(self.gha_1_str)
        self.gha = interpolate_gha(self.gha_0_float, self.gha_1_float, self.interpolation_factor)
        self.sha_str = sha
        self.sha_float = convert_sha(self.sha_str)
        self.semi_diameter_str = semi_diameter
        self.semi_diameter_float = convert_semi_diameter(self.semi_diameter_str)
        self.lha = calculate_lha(self.gha, self.dr_longitude_float)
        self.height_calculated_float = calculate_height_calculated(self.dec, self.lha, self.dr_latitude_float)
        self.azimuth_z = calculate_azimuth_z(self.dec, self.dr_latitude_float, self.height_calculated_float, self.lha)
        self.height_observed_float = calculate_height_observed(self.eye_height, self.height_sextant_float,self.index_error_float,
                                                               self.pressure_float, self.temperature_float, self.celestial_body,
                                                               self.semi_diameter_float)
        self.plot = create_plot_str(self.height_observed_float, self.height_calculated_float, self.azimuth_z)
    