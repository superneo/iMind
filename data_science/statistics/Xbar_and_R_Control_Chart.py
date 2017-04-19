#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import numpy as np
import matplotlib.pyplot as plt

my_range = lambda tmp_list: np.max(tmp_list) - np.min(tmp_list)
my_items_title = lambda tmp_list: "\t".join(['x' + str(elem) for elem in tmp_list])

# sample size: [A2, D4, D3]
coeffs = {
  2: [1.880, 3.267, 0.0],
  3: [1.023, 2.575, 0.0],
  4: [0.729, 2.282, 0.0],
  5: [0.577, 2.114, 0.0],
  6: [0.483, 2.004, 0.0],
  7: [0.419, 1.924, 0.076],
  8: [0.373, 1.864, 0.136],
  9: [0.337, 1.816, 0.184],
  10: [0.308, 1.777, 0.223]
}

if __name__ == '__main__':
  print("[" + sys.argv[0] + "] invoked.")

  if len(sys.argv) != 4:
    print("[USAGE] " + sys.argv[0] + " num_sample_sets size_sample_set x_bar")
    sys.exit(1)

  num_sample_sets = int(sys.argv[1])  # number of total sample sets
  size_sample_set = int(sys.argv[2])  # number of items in each sample set
  x_bar = float(sys.argv[3])  # the origin for means of samples

  if size_sample_set not in coeffs:
    print("[ERROR] invalid number of items in each sample set!!!")
    sys.exit(1)

  sample_dict = {}
  sample_set_idx = 0

  for row in range(num_sample_sets):
    sample_set_idx += 1
    sample_dict[sample_set_idx] = []
    for col in range(size_sample_set):
      cur_item = x_bar - 0.5 + float('%.2f' % random.random())
      # print "%.2f" % (x_bar - 0.5 + random.random()),
      sample_dict[sample_set_idx].append(cur_item)

  total_x_bar = []
  total_r = []

  with open("table.txt", "w") as outf:
    title = "표본번호		개별치%s평균		범위\n" % ('\t' * (size_sample_set + 1))
    subtitle = '\t\t' + my_items_title(range(1, size_sample_set + 1)) + '\t\t(X_bar)\t\t(R)\n'
    outf.write(title)
    outf.write(subtitle)

    for key in sorted(sample_dict.keys()):
      cur_x_bar = np.mean(sample_dict[key])
      cur_range = my_range(sample_dict[key])
      total_x_bar.append(cur_x_bar)
      total_r.append(cur_range)
      line = "%d\t\t%s\t\t%.3f\t\t%.2f\n" % (key, "\t".join([str(elem) for elem in sample_dict[key]]), cur_x_bar, cur_range)
      outf.write(line)
    outf.write("합계:\t\t%s%.3f\t\t%.2f\n\n\n" % ('\t' * (size_sample_set + 1), np.sum(total_x_bar), np.sum(total_r)))

    UCL_X_bar = np.mean(total_x_bar) + coeffs[size_sample_set][0] * np.mean(total_r)
    LCL_X_bar = np.mean(total_x_bar) - coeffs[size_sample_set][0] * np.mean(total_r)
    UCL_R = coeffs[size_sample_set][1] * np.mean(total_r)
    LCL_R = coeffs[size_sample_set][2] * np.mean(total_r)

    outf.write("UCL_X_bar\tLCL_X_bar\tItems (X_bar)\n")
    outf.write("%s\t\t%s\t\t%s\n" % ('%.3f' % UCL_X_bar, '%.3f' % LCL_X_bar, ", ".join([str(elem) for elem in total_x_bar])))
    np_total_x_bar = np.array(total_x_bar)
    if (LCL_X_bar < np_total_x_bar).all() and (np_total_x_bar < UCL_X_bar).all():
      outf.write("[X_bar] well managed within the control limit range.\n\n")
    else:
      outf.write("[X_bar] some outliers exist in the sample!!!\n\n")

    outf.write("UCL_R\tLCL_R\tItems (R)\n")
    outf.write("%s\t%s\t%s\n" % ('%.3f' % UCL_R, '%.3f' % LCL_R, ", ".join([str(elem) for elem in total_r])))
    np_total_r = np.array(total_r)
    if (LCL_R < np_total_r).all() and (np_total_r < UCL_R).all():
      outf.write("[R] well managed within the control limit range.\n\n")
    else:
      outf.write("[R] some outliers exist in the sample!!!\n\n")

  plt.figure(1)
  ax = plt.subplot(211)
  num_cases = len(total_x_bar)
  val_range = UCL_X_bar - LCL_X_bar
  ax.set_title(r'$<\bar X-Control\ Chart>$')
  plt.axis([-0.15 * num_cases, 1.25 * num_cases, LCL_X_bar - 0.2 * val_range, UCL_X_bar + 0.2 * val_range])
  plt.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelbottom='off', labelleft='off')
  plt.plot(np.arange(num_cases), num_cases * [UCL_X_bar], 'k')
  plt.text(-1.0, UCL_X_bar, r'UCL', horizontalalignment='right', verticalalignment='center')
  plt.text(num_cases + 1.0, UCL_X_bar, '%.3f' % UCL_X_bar, horizontalalignment='left', verticalalignment='center')
  plt.plot(np.arange(num_cases), num_cases * [np.mean(total_x_bar)], 'k')
  plt.text(-1.0, np.mean(total_x_bar), r'CL', horizontalalignment='right', verticalalignment='center')
  plt.text(num_cases + 1.0, np.mean(total_x_bar), r'$\bar \bar X=%.3f$' % np.mean(total_x_bar),
    horizontalalignment='left', verticalalignment='center')
  plt.plot(np.arange(num_cases), num_cases * [LCL_X_bar], 'k')
  plt.text(-1.0, LCL_X_bar, r'LCL', horizontalalignment='right', verticalalignment='center')
  plt.text(num_cases + 1.0, LCL_X_bar, '%.3f' % LCL_X_bar, horizontalalignment='left', verticalalignment='center')
  plt.plot(np.arange(num_cases), total_x_bar, 'bo')

  ax = plt.subplot(212)
  num_cases = len(total_r)
  val_range = UCL_R - LCL_R
  ax.set_title(r'$<R-Control\ Chart>$')
  plt.axis([-0.15 * num_cases, 1.25 * num_cases, LCL_R - 0.2 * val_range, UCL_R + 0.2 * val_range])
  plt.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelbottom='off', labelleft='off')
  plt.plot(np.arange(num_cases), num_cases * [UCL_R], 'k')
  plt.text(-1.0, UCL_R, r'UCL', horizontalalignment='right', verticalalignment='center')
  plt.text(num_cases + 1.0, UCL_R, '%.3f' % UCL_R, horizontalalignment='left', verticalalignment='center')
  plt.plot(np.arange(num_cases), num_cases * [np.mean(total_r)], 'k')
  plt.text(-1.0, np.mean(total_r), r'CL', horizontalalignment='right', verticalalignment='center')
  plt.text(num_cases + 1.0, np.mean(total_r), r'$\bar R=%.3f$' % np.mean(total_r),
    horizontalalignment='left', verticalalignment='center')
  plt.plot(np.arange(num_cases), num_cases * [LCL_R], 'k')
  plt.text(-1.0, LCL_R, r'LCL', horizontalalignment='right', verticalalignment='center')
  plt.text(num_cases + 1.0, LCL_R, '%.3f' % LCL_R, horizontalalignment='left', verticalalignment='center')
  plt.plot(np.arange(num_cases), total_r, 'bo')
  plt.show()

