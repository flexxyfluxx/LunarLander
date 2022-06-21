# entrydialog.py
# AP
# Version 1.03, April 6, 2015

from ch.aplu.util import Monitor
from ch.aplu.util import CheckEntry, EntryItem, RadioEntry, SliderEntry
from ch.aplu.util import TextEntry, ButtonEntry, EntryListener 
import ch.aplu.util.EntryDialog as JavaEntryDialog
import ch.aplu.util.EntryPane as JavaEntryPane
import ch.aplu.util.IntEntry as JavaIntEntry
import ch.aplu.util.LongEntry as JavaLongEntry
import ch.aplu.util.DoubleEntry as JavaDoubleEntry
import ch.aplu.util.StringEntry as JavaStringEntry

# redefine EntryDialog
class EntryDialog(JavaEntryDialog):
   def __init__(self, *args, **kwargs):
       # full ctor
       if len(args) > 2 and type(args[0]) == int and type(args[1]) == int:
           JavaEntryDialog.__init__(self, args[0], args[1], args[2:], **kwargs)

       # short ctor 
       else:
           JavaEntryDialog.__init__(self, args, **kwargs)


# redefine EntryPane
class EntryPane(JavaEntryPane):
   def __init__(self, *args):
       if len(args) > 1 and type(args[0]) == str:
           JavaEntryPane.__init__(self, args[0], args[1:])
       else:
           JavaEntryPane.__init__(self, args)

# redefine IntEntry
class IntEntry(JavaIntEntry):
   def __init__(self, *args):
       if len(args) == 2:
           JavaIntEntry.__init__(self, args[0], args[1])
       elif len(args) == 1:
           JavaIntEntry.__init__(self, args[0])

# redefine LongEntry
class LongEntry(JavaLongEntry):
   def __init__(self, *args):
       if len(args) == 2:
           JavaLongEntry.__init__(self, args[0], args[1])
       elif len(args) == 1:
           JavaLongEntry.__init__(self, args[0])


# define FloatEntry
class FloatEntry(JavaDoubleEntry):
   def __init__(self, *args):
       if len(args) == 2:
           JavaDoubleEntry.__init__(self, args[0], args[1])
       elif len(args) == 1:
           JavaDoubleEntry.__init__(self, args[0])

# redefine StringEntry
class StringEntry(JavaStringEntry):
   def __init__(self, *args):
       if len(args) == 2:
           JavaStringEntry.__init__(self, args[0], args[1])
       elif len(args) == 1:
           JavaStringEntry.__init__(self, args[0])


def putSleep():
   Monitor.putSleep()

def wakeUp():
   Monitor.wakeUp()
