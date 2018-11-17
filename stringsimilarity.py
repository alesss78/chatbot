#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 09:53:34 2018

@author: mrshit
"""
import numpy as np

class stringsimilarity():
 def __init__(self):
    self.distance = 0

 def Damerau_levenshtein_distance(self, s1, s2):
    len_s1 = len(s1)
    len_s2 = len(s2)
    
    d = np.zeros((len_s1, len_s2))
    
    for i in range(-1, len_s1):
        d[i,0] = i + 1
    for j in range(-1, len_s2):
        d[0,j] = j + 1
        
    cost = 0
    for i in range(0, len_s1):
        for j in range(0, len_s2):
            if (s1[i] == s2[j]):
                cost = 0
            else:
                cost = 1
            d[i, j] = min(d[i - 1,j] + 1,          # deletion
                          d[i,j - 1] + 1,          # insertion
                          d[i - 1,j - 1] + cost)   # substitution
            if i > 1 and j > 1 and (s1[i] == s2[j - 1]) and (s1[i - 1] == s2[j]):
                d[i, j] = min(d[i, j],
                              d[i - 2, j - 2] + cost) # transposition
    return d[len_s1 - 1, len_s2 - 1]


 def levenshtein_distance(self, s1, s2):
    len_s1 = len(s1)
    len_s2 = len(s2)
    cost = 0
    d = np.zeros((len_s1, len_s2))
    for i in range (-1, len_s1):
        d[i, 0] = i + 1
        
    for j in range(-1, len_s2):
        d[0, j] = j + 1

    for j in range(0, len_s2):
      for i in range(0, len_s1):
          if (s1[i] == s2[j]):
             cost = 0
          else:
             cost = 1
          d[i, j] = min(d[i-1, j] + 1,                   # deletion
                        d[i, j-1] + 1,                   # insertion
                        d[i-1, j-1] + cost)              # substitution
 
    return d[len_s1 - 1, len_s2 - 1]

