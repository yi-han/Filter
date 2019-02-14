import sys

import mapsAndSettings



assert(len(sys.argv)>1)
mapsAndSettings.massSummary(sys.argv[1])
print("done")