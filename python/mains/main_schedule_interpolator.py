#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pstats
import cProfile
import sys
sys.path.insert(0, '../')

import IOUtils, paths,routes_manager,stops_from_route,KML_manager,schedule_interpolator
def format_to_googletransit(schedule,trip_id):
    schedule_formatted = []
    for i in range(0,len(schedule)):
        time = schedule[i]
        schedule_formatted.append(trip_id+","+time[0]+","+time[0]+","+time[1]+","+str(i+1)+",,,")
    return schedule_formatted

def calculate():
    list_stop_times = IOUtils.read_file_to_dictlist('../' + paths.PARADAS + "initial_stop_times.txt")
    list_shapes = IOUtils.read_file_to_dictlist('../' + paths.GOOGLE_TRANSIT + "shapes.txt")
    list_stops = IOUtils.read_file_to_dictlist('../' + paths.GOOGLE_TRANSIT + "stops.txt")
    trips = IOUtils.read_file_to_dictlist('../' + paths.GOOGLE_TRANSIT + "trips.txt")
    stops_routes = IOUtils.read_file_to_dictlist('../'+paths.PARADAS +"Paradas das rotas.txt")

    trip_ids = [trip["trip_id"] for trip in trips]
    schedules = {}




    schedule_formatted = []
    schedule_formatted.append("trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,shape_dist_traveled")
    index = 0
    for trip_id in trip_ids:
        #if (index == 3):
        #    break

        index = index + 1
        route_id = routes_manager.routeid_from_tripid(trip_id)
        service_id = routes_manager.serviceid_from_tripid(trip_id)
        print("=============================================== " + trip_id)

        # if (schedules.has_key(route_id)):
        #     schedules_route = schedules[route_id]
        #     if (schedules_route.has_key(service_id)):
        #         schedule_formatted.extend(format_to_googletransit(schedules_route[service_id],trip_id))
        #         print "============================================================================================="
        #         #print (schedule_formatted)
        #
        #         continue
        #     else:
        #         schedules[route_id][service_id] = []
        # else:
        #     schedules[route_id] = {}

        marks_filtered = routes_manager.marks_from_route(list_shapes,route_id)
        stop_times_filtered = [stop_time for stop_time in list_stop_times if stop_time["trip_id"] == trip_id]
        stops_ids = [stop_route["stop_id"] for stop_route in stops_routes if stop_route["route"] == route_id]
        resp = schedule_interpolator.schedule_interpolator(stops_ids, int(route_id), stop_times_filtered, marks_filtered, list_stops)

#        schedules[route_id][service_id] = resp
        schedule_formatted.extend(format_to_googletransit(resp,trip_id))
        #print(oi)
        #print("=============================================== " + route_id + " " + service_id)
        # print(resp)

        #print (schedule_formatted)


    #IOUtils.save_file(schedule_formatted,'../' + paths.GOOGLE_TRANSIT + "stop_times1.txt")

cProfile.run("calculate()")

