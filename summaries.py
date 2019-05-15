# goes through every folder and tried to make a summary.
# then creates a summary of the summary

import sys
import os
import mapsAndSettings



assert(len(sys.argv)>1)

root = sys.argv[1]+"/"
print("\n\nscanning {0}\n\n".format(root))
assert(os.path.isdir(root))

snippets = []
for sub in os.listdir(root):
    directory = root+"/"+sub
    if os.path.isdir(directory):

        print(directory)
        snippet = (mapsAndSettings.extensiveSummary(directory))
        if snippet:
            snippets.extend(snippet)
        mapsAndSettings.merge_summaries(directory)
        print("done")


if snippets:
    # if we were successful
    overallSummary = open("{0}/overallSummary.csv".format(root), "w")
    overallSummary.write("AttackType,Repeats,Agent,MeanofMean,MeanSd,MeanRange,CombinedMean,CombinedSd,CombinedRange,Tau,Pretraining,Annealing,TotalEpisodes,start_e,overload,adv_tau,adv_discount,adv_pretrain,adv_annealing_episodes,adv_episodes,adv_start_e\n")
    for snippet in snippets:
        overallSummary.write(snippet)
    overallSummary.close()
