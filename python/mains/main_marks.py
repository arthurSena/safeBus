#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')

import IOUtils, paths, KML_manager

if __name__ == '__main__':
	marks = KML_manager.extract_routes("../"+paths.ROTAS+"Rotas.kml")
	IOUtils.save_file_lists(marks,"../"+paths.ROTAS+ "shapesRotas/shapes.txt")