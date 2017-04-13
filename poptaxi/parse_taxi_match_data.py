#!/usr/bin/python

import sys
import re

if __name__ == '__main__':
  print("[main] invoked.")

  if len(sys.argv) != 3:
    print("[ERROR] input/output file names not given.")
    sys.exit(1)

  IdDayTime = {}
  white_space = re.compile('\s+')
  valid_record = re.compile("^(T_\d+),([1-7]),([\d]{2}),(1|2|3|-1),(\d+)?,(\d+)?,(\d+)?,(\d+)?,$")
  clear_pattern = re.compile("[\(\)\[\]\'\"\s]")

  with open(sys.argv[1], "r") as inf:
    num_lines = 0
    for line in inf:
      num_lines += 1
      line2 = white_space.sub('', line)
      matches = valid_record.match(line2)
      if None == matches:
        print("[Warning] not matched: [" + str(num_lines) + "] " + line)
        continue
      key = matches.group(1, 2, 3)
      if None in key:
        print("[ERROR] T_Link_ID/Day/Time fields must be valid.")
        continue
      val = [elem != None and int(elem) or 0 for elem in matches.group(6, 7, 8)]
      # print("[val] (" + str(num_lines) + ") " + str(val))
      if key in IdDayTime:
        IdDayTime[key][0] += 1
        IdDayTime[key][1] += val[0]
        IdDayTime[key][2] += val[1]
        IdDayTime[key][3] += val[2]
      else:
        IdDayTime[key] = [1, val[0], val[1], val[2]]
    print("total lines: " + str(num_lines))

  print("[IdDayTime] total pairs: " + str(len(IdDayTime)))
  with open(sys.argv[2], "w") as outf:
    outf.write("T_Link_ID,Day,Time,TotalInstance,TotalCntOn,TotalCntOff,TotalCntEmp\n")
    for key in sorted(IdDayTime.keys()):
      outf.write(clear_pattern.sub('', str(key) + ',' + str(IdDayTime[key])) + "\n")

