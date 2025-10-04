# filepath: clancalc-ui/src/clancalc.py
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 14:44:37 2025

@author: Gako
"""
import numpy as np
import json


class Member:
    def __init__(self, name, level, role):
        self.name = name
        self.level = int(level)
        self.role = int(role)
        dmgmod = np.ones(3)
        if (self.role != 0):
            dmgmod[int(role) - 1] = 1.25
        self.dmgmod = dmgmod


    def getdmg(self):
        return 10. * 3**(self.level - 1) * self.dmgmod


class Guild:
    def __init__(self, name, members):
        self.name = name
        self.members = members
        dmg = np.zeros(3)
        for member in members:
            dmg += member.getdmg()
        self.damage = dmg * 30 * 15

    def getdmg(self):
        return self.damage

    def getmaxlevel(self):
        return self.maxlevel(self.damage)

    def p(self, level):
        if (level < 4):
            return (2 * level - 1) / 10
        if (level < 7):
            return (level - 3) / 10
        return (2 * ((level - 1) % 3) + 3) / 10

    def immohp(self, level):
        return 10 * 3**(np.ceil(level / 3) - 1) * 15 * 35 * 10 * self.p(level)

    def maxlevel(self, dmg):
        level = np.floor(3 * np.log(self.damage / 1750) / np.log(3) + 2)
        for i in range(0, 3):
            while (self.immohp(level[i]) > self.getdmg()[i]):
                level[i] -= 1
        return level
