import sys

import mapsAndSettings



assert(len(sys.argv)>1)
mapsAndSettings.extensiveSummary(sys.argv[1])
mapsAndSettings.merge_summaries(sys.argv[1])
print("done")