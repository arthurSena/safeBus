
def marks_from_route(routes_marks,routeid):
    return [mark for mark in routes_marks if mark["shape_id"] == str(routeid)]

def routeid_from_tripid(tripid):
    return tripid.split("_")[0]

def serviceid_from_tripid(tripid):
    return tripid.split("_")[1]