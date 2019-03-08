# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 22:52:30 2015
Automatic grading of assignments using google survey
Assumptions:
A google form has been created with name and email as fields both of which are set to SOLUTION for the true solution
Usage:
    grade.py ifname [ofname]
ifname: Input CSV file name of survey responses
ofname: Optional 
@author: Afsar
"""
from __future__ import print_function
import csv
import os, sys
import numpy as np

def getFileParts(fname):
    """
    Returns the parts of a file (path,name,ext)
    """
    (path, name) = os.path.split(fname)
    n = os.path.splitext(name)[0]
    ext = os.path.splitext(name)[1]
    return (path, n, ext)    


nargs = len(sys.argv)

if nargs == 2:
    fname = sys.argv[1]
    p,f,e = getFileParts(fname)
    f = f+'_graded'
    ofname = os.path.join(p,f+e)
elif nargs == 3:
    ofname = sys.argv[2]
else:    
    raise ValueError("Arguments Error. Usage: grade inputcsv [outputcsv]")
solution_key = 'SOLUTION'
Submissions = {}
with open(fname, 'rb') as csvfile:
    reader  = csv.reader(csvfile)
    for row in reader:
        if row[0] == 'Timestamp':
            continue
        #print ', '.join(row)
        if row[2] not in Submissions:
            Submissions[row[2]]=row
if solution_key not in Submissions:
    raise ValueError("Solution not found")
Solution = Submissions[solution_key]
N = len(Solution)
Scores = {}
sList = []
for key in Submissions:
    csub = Submissions[key]
    Scores[key]=(csub[1],key,csub[0],100.0*np.mean([csub[i]==Solution[i] for i in range(3,N) if Solution[i]]))
    sList.append((csub[1].lower(),key))
sList = sorted(sList)

with open(ofname, 'wb') as csvfile:    
    writer = csv.writer(csvfile)
    writer.writerow(['Name','Email','Submission Time','Percentage Score'])
    for name,key in sList:
        if name != solution_key.lower():
            writer.writerow(Scores[key])

print("File created:",ofname)
