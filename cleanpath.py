"""cleanPath - Edit PATH and similar environment variables.Takes one
argument: which variable to edit (defaults to PATH).Try it on
PYTHONPATH, PERL5LIB, CLASSPATH, etc.Written in IronPython by
Catherine Devlin (catherinedevlin.blogspot.com)"""


from Microsoft.Win32 import Registry
import System, sys, cleanPath


class PathItem:

    def __init__(self, raw, parent):
        self.raw = raw
        self.cleaned = self.raw.lower().rstrip('\\')
        self.keep = True
        self.parent = parent

    def isJar(self):
        return self.parent.pathType == 'classpath' and \
               self.cleaned[-4:] == '.jar'

    def exists(self):
        if self.isJar():
            info = System.IO.FileInfo
        else:
            info = System.IO.DirectoryInfo
        try:
            return info(self.raw).Exists
        except:
            return False

    def findDupOf(self, lst):
        for i in range(len(lst)):
            if self.cleaned == lst[i].cleaned:
                return i
            return None

    def flagStr(self):
        badStr, dupStr = '   ','         '
        if not self.exists():
            badStr = 'BAD'
            if self.dupOf:
                dupStr = 'DUP of %2s' % (self.dupOf)
                return ('%s %s' % (badStr, dupStr)).ljust(13)

    def __str__(self):
        return '%s %s. %s' % (self.flagStr(), str(self.idx).rjust(2),
        self.raw)


class Path:
    def __init__(self, pathType):
        self.pathType = pathType.lower()
        self.envLoc = \
        'HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\' + \
        'Control\\Session Manager\\Environment'
        self.find()

    def find(self):
        self.oldPath = Registry.GetValue(self.envLoc, self.pathType,
                                         None)
        self.items = []
        if not self.oldPath:
            return
        for element in self.oldPath.split(';'):
            pathItem = PathItem(element, self)
            pathItem.dupOf = pathItem.findDupOf(self.items)
            pathItem.idx = len(self.items)
            self.items.append(pathItem)

    def __str__(self):
        return '\n'.join([str(i) for i in self.items])

    def recc(self):
        return [p for p in self.items if p.exists() and not p.dupOf]

    def strRecc(self):
        return ' '.join([str(p.idx) for p in self.recc()])

    def isGood(self):
        return self.recc() == self.items

    def record(self):
        fname = '%s_%s.txt' % (self.pathType,
                               str(System.DateTime.Now.GetHashCode()))
        f = open(fname, 'w')
        f.write(self.oldPath)
        f.close()

    def set(self, chosen):
        self.record()
        newPathStr = ';'.join([p.raw for p in chosen])
        Registry.SetValue(self.envLoc, self.pathType, newPathStr)
        print 'Path has been set to %s\n' % (newPathStr)

    def question(self):
        result = ''
        if self.isGood():
            result += 'No bad or duplicate items found in your' + \
                      'path.\n'
        else:
            result += 'Your reccommended path is %s\na: accept, ' % \
                      (self.strRecc())
            result += 'q: quit, or enter your own path' + \
                      '(like "0 1 4 5 3")' + \
                      '\nd: delete (followed by numbers to' + \
                      ' delete, like "d3 5")'
        return result

    def ask(self):
        print self.question()
        inp = raw_input('> ') or 'h'
        inp = inp.lower().strip()
        return inp

    def askLoop(self):
        inp = self.ask()
        while inp != 'q':
            if inp == 'a':
                self.set(self.recc())
                return
            elif inp.replace(' ','').isdigit():
                chosenNumbers = [int(i) for i in inp.split()]
                self.set([i for i in self.items if i.idx in
                          chosenNumbers])
                return
            elif inp[0] == 'd':
                try:
                    chosenNumbers = [int(i) for i in inp[1:].split()]
                    self.set([i for i in self.items if i.idx not in
                              chosenNumbers])
                    self.find()
                    print(self)
                except:
                    None
                    inp = self.ask()


def main(whichPath):
    path = Path(whichPath or 'Path')
    if path.items:
        print path
        path.askLoop()
    else:
        print "Could not find a pathlike environment" + \
        " variable '%s'.\n%s" % \
        (whichPath, cleanPath.__doc__)


if __name__ == '__main__':
    whichPath = None
    if len(sys.argv) > 1:
        whichPath = sys.argv[1]
        main(whichPath)
