from math import sqrt, sin, cos, tan, asin, acos, atan2, radians, pi


def get_phi(latitude_deg):
    return radians(latitude_deg)


def mean_anomaly(day_frac):
    return 2 * pi * day_frac


def true_anomaly(m, e):
    e_anom = m + e * sin(m) * (1 + e * cos(m))
    v = 2 * atan2(sqrt(1 + e) * sin(e_anom / 2),
                  sqrt(1 - e) * cos(e_anom / 2))
    return v


def solar_longitude(v):
    return v


def equation_of_time(m, ls, e, obliquity_rad):
    e_term = -2 * e * sin(m)
    obl_term = tan(obliquity_rad / 2) ** 2 * sin(2 * ls)
    return e_term + obl_term


def declination(ls, obliquity_rad):
    return asin(sin(obliquity_rad) * sin(ls))


def solar_altitude(latitude, hour_angle, decl):
    phi = radians(latitude)
    return_value = asin(sin(phi) * sin(decl) + cos(phi) * cos(decl) * cos(hour_angle))
    return return_value


def solar_azimuth(latitude, hour_angle, decl, altitude):
    phi = radians(latitude)
    cos_az = (sin(decl) - sin(phi) * sin(altitude)) / (cos(phi) * cos(altitude))
    cos_az = max(-1, min(1, cos_az))
    az = acos(cos_az)
    if hour_angle > 0:
        az = 2 * pi - az
    return az


def get_solar_xy(latitude, hour_angle, decl):
    alt = solar_altitude(latitude, hour_angle, decl)
    if alt <= 0:
        return None
    az = solar_azimuth(latitude, hour_angle, decl, alt)
    x = cos(alt) * sin(az)
    y = sin(alt)
    return x, y


__all__ = [
    "get_phi",
    "get_solar_xy",
    "mean_anomaly",
    "true_anomaly",
    "solar_longitude",
    "solar_azimuth",
    "solar_altitude",
    "declination",
    "equation_of_time"
]

# def create_path(day, orbital_period, eccentricity, axial_tilt, latitude):
#     path = []
#     day_frac = day / orbital_period
#     m = mean_anomaly(day_frac)
#     v = true_anomaly(m, eccentricity)
#     ls = solar_longitude(v)
#     decl = declination(ls, axial_tilt)
#     eot = equation_of_time(m, ls, eccentricity, axial_tilt)
#
#     hour_angle = -eot
#     result = get_solar_xy(latitude, hour_angle, decl)
#     if result:
#         x, y = result
#         px = center_x + int(x * radius)
#         py = center_y - int(y * radius)
#         path.append((px, py))
#     return path
