#!/usr/bin/env python
#coding=utf8
import sys
import argparse
import commands
import re

class LogItem:
  """Each LogItem indicates one change log"""
  revision = ""
  author = ""
  date = ""
  logs = ""
  bug_id = ""
  feature_id = ""
  is_non_code = False

  def updateFromSvnLog(self, logItem):
    self.logs = ""
    lines = logItem.splitlines()
    index = 0
    while index < len(lines):
      if (len(lines[index]) == 0):
        index = index + 1
        continue;
      elif (index == 0):
        values = lines[index].split(" | ");
        self.revision = values[0]
        self.author = values[1]
        self.date = values[2]
      else:
        self.logs = self.logs + lines[index] + "\n"
        if (lines[index].startswith("BUGFIX")):
          self.bug_id = lines[index].split(":")[1].strip();
        elif (lines[index].startswith("FEATURE")):
          self.feature_id = lines[index].split(":")[1].strip();
        elif (lines[index].startswith("NONCODE")):
          self.is_non_code = True
      index = index + 1

  def matched(self, item):
    return (self.bug_id == item.bug_id
      and self.feature_id == item.feature_id
      and self.logs == item.logs)

  def isNonCodeCommits(self):
    return self.is_non_code;

  def printOut(self):
    print "Rev:",self.revision, "|", "Author:",self.author, "|", "Date:",self.date;
    print "BUG:", self.bug_id, "|", "FEATURE:", self.feature_id;
    print "Log:",self.logs;


  def __init__(self, log):
    self.updateFromSvnLog(log)

def performCommandAndGetResult(command_line):
  return commands.getstatusoutput(command_line)

def processResult(output, skipNonCode):
  logItems = ""
  change_logs = []

  for line in output.splitlines():
    if line.startswith("---"):
      if (len(logItems) > 0):
        item = LogItem(logItems)
        if (not skipNonCode or not item.isNonCodeCommits()):
          change_logs.append(item)
        logItems = ""
      continue
    logItems = logItems + line + "\n"

  return change_logs

def getSvnLog(path, beginDate, endDate, skipNonCode):
  command = "svn log "+path+" -r {"+endDate+"}:{"+beginDate+"}"

  result = performCommandAndGetResult(command)
  change_logs = processResult(result[1], skipNonCode)

  return change_logs


if __name__=="__main__":
  path = "/media/horky/Data/Project/U3/cn/cn-10.9.0-patch1/core"
  getSvnLog(path, "2015-12-01", "2015-12-02", False)
