import collections
import csv


total_key_set = collections.Counter()


class SSLEntry(object):
  """Represents an SSL entry, with one attribute per field retrieved from Tisch"""
  def __init__(self):
    self.keys = []

def process_entries():
  try:
    entry_list = []
    with open('tischdata.csv', 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
        new_entry = SSLEntry()
        # First five entries are SSL-related and we don't care about them
        for i in xrange(5, len(row)):
          key, _ = eval(row[i])
          if key in new_entry.keys:
            continue
          new_entry.keys.append(key)
        entry_list.append(new_entry)
        for key in new_entry.keys:
          total_key_set[key] += 1
  except:
    pass
  return entry_list


def write_stats(entry_list):
  num_keys_list = [len(e.keys) for e in entry_list]
  print 'Number of keys:\t%d' % len(total_key_set)
  print 'Number of publications:\t%d' % len(num_keys_list)
  print ''
  print 'Frequency of each key among articles:'
  for k, v in total_key_set.most_common():
    print '    %s\t%d\t%f' % (k, v, v / float(len(num_keys_list)))
  print ''
  print 'Min keys present: %d' % min(num_keys_list)
  print 'Max keys present: %d' % max(num_keys_list)
  print 'Average keys present: %.2f' % (sum(num_keys_list) / float(len(num_keys_list)))


if __name__ == '__main__':
  write_stats(process_entries())
