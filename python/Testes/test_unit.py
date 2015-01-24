# -*- coding: utf-8 -*-

import unittest
from test import test_support
import test_unity_utils, test_geo_utils, test_route_marks_interpolator, test_csv_manager


def test_main():
    test_support.run_unittest(test_unity_utils.TestUnityUtils, test_geo_utils.TestGeoUtils,
                              test_route_marks_interpolator.TestaRouteMarksInterpolator, test_csv_manager.Test_csv_manager)


if __name__ == '__main__':
    test_main()
