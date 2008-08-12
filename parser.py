class Key(object):
  token = 'WASTE_PUBLIC_KEY'

  def __init__(self, io):
    line = io.readline().strip()
    while not line.startswith(Key.token):
      line = io.readline().strip()
    elements = line.split(None, 3)
    self.number = long(elements[1])
    self.length = long(elements[2])
    self.name = elements[3]
    public = []
    line = io.readline().strip()
    while not line.startswith(Key.token):
      public.append(line)
      line = io.readline().strip()
    self.public = public

  def __str__(self):
    return """%s %s %s %s
%s
%s""" % (Key.token, self.number, self.length, self.name,
         "\n".join(self.public),
         Key.token)

def main():
  print Key(open("keys.txt"))

if __name__=="__main__":
  main()