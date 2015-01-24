#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import IOUtils, paths, route_marks_interpolator

if __name__ == '__main__':
    # write_new_points_on_file("500", IOUtils.read_file_to_dictlist(paths.GOOGLE_TRANSIT+"shapes.txt"))
    routes_marks = IOUtils.read_file_to_dictlist("../"+paths.ROTAS+"shapesRotas/shapes.txt")
    list_answer = route_marks_interpolator.format_transit_points(10,routes_marks)
    print list_answer
    IOUtils.save_file_lists(list_answer,"../"+paths.GOOGLE_TRANSIT+"shapes.txt")
