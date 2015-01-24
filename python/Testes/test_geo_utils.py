# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import unittest
from test import test_support

import GEOUtils

class TestGeoUtils(unittest.TestCase):
    def test_distance(self):
        # Testa distancia normal
        actual = float(GEOUtils.distance(-7.217149, -35.911706, -7.217276, -35.910807))
        expected = 100
        self.assertAlmostEquals(expected, actual, 0)

        # Testa se trocar a posição de coordenadas
        actual = float(GEOUtils.distance(-7.217149, -35.911706, -7.217276, -35.910807))
        expected = 100
        self.assertAlmostEquals(expected, actual, 0)

        # Testa se a distância for zero
        actual = GEOUtils.distance(-7.217149, -35.911706, -7.217149, -35.911706)
        expected = 0
        self.assertAlmostEquals(expected, actual, 0)

        # Testa se a distância se aproximar de 0
        actual = GEOUtils.distance(-7.217149, -35.911706, -7.217149, -35.911705)
        expected = 0
        self.assertLess(expected, actual, 0)

        #Testa se a latitude não for valida (>90º ou < -90º)
        try:
            actual = GEOUtils.distance(-90.217149, -35.911706, -7.217149, -35.911705)
            self.assertEqual(1,0)
        except ValueError as e:
            pass

        try:
            actual = GEOUtils.distance(-7.217149, -35.911706, 90.217149, -35.911705)
            self.assertEqual(1,0)
        except ValueError as e:
            pass

        #Testa se a longitude não for valida(>180º ou < -180º)
        try:
            actual = GEOUtils.distance(-7.217149, -35.911706, -7.217149, -180.911705)
            self.assertEqual(1,0)
        except ValueError as e:
            pass

        try:
            actual = GEOUtils.distance(7.217149, 180.911705, -7.217149, -35.911706)
            self.assertEqual(1,0)
        except ValueError as e:
            pass

    def test_distance2(self):
        # Testa distancia normal
        actual = GEOUtils.distance2(-7.217149, -35.911706, -7.217276, -35.910807)
        expected = 100
        self.assertAlmostEquals(expected, actual, 0)

        # Testa se trocar a posição de coordenadas
        actual = GEOUtils.distance2(-7.217149, -35.911706, -7.217276, -35.910807)
        expected = 100
        self.assertAlmostEquals(expected, actual, 0)

        # Testa se a distância for zero
        actual = GEOUtils.distance2(-7.217149, -35.911706, -7.217149, -35.911706)
        expected = 0
        self.assertAlmostEquals(expected, actual, 0)

        # Testa se a distância se aproximar de 0
        actual = GEOUtils.distance2(-7.217149, -35.911706, -7.217149, -35.911705)
        expected = 0
        self.assertLess(expected, actual, 0)

    def test_check_direction(self):
        # Testa se quando está a direita da rota, o valor é positivo
        actual1 = GEOUtils.check_direction(-7.217149, -35.911706, -7.217276, -35.910807, -7.217287, -35.911275)
        expected1 = 0
        self.assertGreater(actual1, expected1)

        # Testa se quando está a esquerda da rota, o valor é negativo
        actual2 = GEOUtils.check_direction(-7.217149, -35.911706, -7.217276, -35.910807, -7.217053, -35.911254)
        expected2 = 0
        self.assertLess(actual2, expected2)

        #Testa quando dois pontos da rota são igual, se o terceiro é zero
        actual3 = GEOUtils.check_direction(-7.217149, -35.911706, -7.217149, -35.911706, -7.217053, -35.911254)
        expected3 = 0
        self.assertEqual(actual3, expected3)

        #Testa se quando o valor está em cima da rota o valor é zero
        actual4 = GEOUtils.check_direction(-7.217160545527704, -35.91162427274799, -7.217172091040776, -35.911542545491834, 7.217183636539218, -35.91146081823155)
        expected4 = 0
        self.assertAlmostEqual(actual4, expected4, 0)


