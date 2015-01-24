# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import UnityUtils, math

class TestUnityUtils(unittest.TestCase):
    def test_deg2rad(self):
        error = "Didn't convert from degrees to radian!"
        self.assertEquals(UnityUtils.deg2rad(180), math.pi, error)
        self.assertEquals(UnityUtils.deg2rad(90), math.pi/2, error)
        self.assertEquals(UnityUtils.deg2rad(60), math.pi/3, error)

    def test_change_schedule_second(self):
        error = "The hour wasn't converted correctly!"
        self.assertEquals(UnityUtils.change_schedule_second("01:30:30"), 5430, error)
        self.assertEquals(UnityUtils.change_schedule_second("11:38:27"),41907, error)