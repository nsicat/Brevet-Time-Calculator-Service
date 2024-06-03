"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#
#original

# Define control times and brevet distances

brevet_distances = [200, 300, 400, 600, 1000]

min_speeds = [
    (200, 15),
    (200, 15),
    (200, 15),
    (400, 11.428),
    (300, 13.333)
]
max_speeds = [
    (200, 34),
    (200, 32),
    (200, 30),
    (400, 28),
    (300, 26)
]



def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Calculate the open time for a control.

    Args:
        control_dist_km: number, the control distance in kilometers
        brevet_dist_km: number, the nominal distance of the brevet
        brevet_start_time: An arrow object representing the start time of the brevet
    
    Returns:
        An ISO 8601 format date string indicating the control open time.
        This will be in the same time zone as the brevet start time.
    """

    if brevet_dist_km not in brevet_distances:
        raise ValueError("Brevet Distance Invalid")
    
    # ensures no non-negative values, assumes negative is zero
    if control_dist_km < 0:
        control_dist_km = 0

    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km
   
    if control_dist_km == 0:
        return brevet_start_time.isoformat()
        

    # 0.5 rounds up to the nearest whole number
    control_dist_km = int(control_dist_km + 0.5)

    total_time = 0
    remaining_dist = control_dist_km

    for dist, max_speed in max_speeds:
        if remaining_dist > dist:
            total_time += dist / max_speed
            remaining_dist -= dist
        else:
            total_time += remaining_dist / max_speed
            break

    hours = int(total_time)
    minutes = round((total_time - hours) * 60)

    return brevet_start_time.shift(hours=hours, minutes=minutes).isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Calculate the close time for a control.

    Args:
        control_dist_km: number, the control distance in kilometers
        brevet_dist_km: number, the nominal distance of the brevet
        brevet_start_time: An arrow object representing the start time of the brevet
    
    Returns:
        An ISO 8601 format date string indicating the control close time.
        This will be in the same time zone as the brevet start time.
    """
    #ensure proper distance is inputted
    if brevet_dist_km not in brevet_distances:
        raise ValueError("Brevet Distance Invalid")
    
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km
   
    if control_dist_km < 0:
        control_dist_km = 0
    if control_dist_km == 0:
        return brevet_start_time.shift(hours=1).isoformat()

    # adding 0.5 rounds up to the nearest whole number
    control_dist_km = int(control_dist_km + 0.5)

    total_time = 0
    remaining_dist = control_dist_km

    for dist, min_speed in min_speeds:
        if remaining_dist > dist:
            total_time += dist / min_speed
            remaining_dist -= dist
        else:
            total_time += remaining_dist / min_speed
            break

    hours = int(total_time)
    minutes = round((total_time - hours) * 60)

    return brevet_start_time.shift(hours=hours, minutes=minutes).isoformat()
