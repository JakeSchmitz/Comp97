import csv


entry_list = []
total_key_set = set()


class SSLEntry(object):
  """Represents an SSL entry, with one attribute per field retrieved from Tisch"""
  def __init__(self):
    self.keys = []

  def __str__(self):
    to_return = ''
    for key, value in self.__dict__.iteritems():
      to_return += '%s: %s\n' % (key, value)
    return to_return

  def percent_full(self):
    """Returns percentage of all attributes this entry has"""
    return float(len(self.keys)) / float(len(total_key_set))


try:
  with open('tischdata.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      # First five entries are SSL-related and we don't care about them
      new_entry = SSLEntry()
      for i in xrange(5, len(row)):
        item = eval(row[i])
        key, _ = item
        new_entry.keys.append(key)
        total_key_set.add(key)
      entry_list.append(new_entry)
except:
  pass

percent_list = [e.percent_full() for e in entry_list]

print 'All keys we\'ve found thus far:'
for k in sorted(total_key_set):
  print '    %s' % k
print 'Number of keys: %d' % len(total_key_set)
print 'Min: %f' % min(percent_list)
print 'Max: %f' % max(percent_list)
print 'Average: %f' % (sum(percent_list) / len(percent_list))
