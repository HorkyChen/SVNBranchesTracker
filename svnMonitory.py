#!/usr/bin/env python
#coding=utf8
import sys
import os
import argparse
from getSvnLog import *
from datetime import datetime, timedelta

CSI="\x1B["
CSI_RESET=CSI+"m"

def printInRed(string):
    print CSI+"31;40m",string,CSI_RESET;

def printInGreen(string):
    print CSI+"32;40m",string,CSI_RESET;

def compareTwoLogItemList(leftSideList, rightSideList, leftBranchName, rightBranchName, printMatched):
  print 'Compare',leftBranchName,'with',rightBranchName,':';
  found = False
  for i in range(len(leftSideList)):
    matched = False
    for j in range(len(rightSideList)):
      if leftSideList[i].matched(rightSideList[j]):
        matched = True
        if printMatched:
          printInGreen("Matched!");
          leftSideList[i].printOut();
        break;
    if not matched: #Not found matched item
      found = True
      printInRed("Unmatched!");
      leftSideList[i].printOut();

  if not found:
    printInGreen('Done! These two branches are matched!');

  return found

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-f','--file', type=str, default='monitored_branches.txt', help='The text file contains target branches folder.Default:monitored_branches.txt')
  parser.add_argument('-d','--days', type=int, default=5, help='How many days try to compare. Default:5days')
  parser.add_argument('-s','--skipNonCode', action='store_true', default=False, help='Skip NONCODE commits. Default:False')
  parser.add_argument('-m','--matched', action='store_true', default=False, help='Print matched commits. Default:False')

  args = parser.parse_args()

  list_file = open(args.file, 'r')

  LogItems = []
  Branches = []

  end = datetime.now()
  begin = end - timedelta(days=args.days)

  index = 0
  for line in list_file:
    LogItems.append(getSvnLog(line.strip(), begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), args.skipNonCode))
    head, tail = os.path.split(line.strip())
    Branches.append(tail)
    print tail,"has",len(LogItems[index]), "commits!";
    index = index + 1

  list_file.close()

  found_unmatched = False
  # Compare log items
  for i in range(len(LogItems)):
    for j in range(len(LogItems)):
      if (i == j):
        continue
      if compareTwoLogItemList(LogItems[i], LogItems[j], Branches[i], Branches[j], args.matched):
        found_unmatched = True

  if found_unmatched:
    printInRed('\nSummary:\n  ATTENTION: Found unmatched commits, please double confirm with above list!')
  else:
    printInGreen('\nSummary:\n  Everything goes well!')
