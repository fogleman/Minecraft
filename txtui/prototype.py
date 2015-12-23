#!/usr/bin/env python3
# coding: utf-8

""" Prototype text interface with random map """

import random

for y in range(20):
    line = ''
    for x in range(40):
        line = line + random.choice([' ', '#'])
    print(line)
