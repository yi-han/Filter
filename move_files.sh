#!/bin/bash

# We assume $1 is the name of the folder we are copying from

# sarsaOrig

DEFENDER="sarOrig"


echo ../$1/$DEFENDER "adv_$DEFENDER"
cp -R ../$1/$DEFENDER "adv_$DEFENDER"
rm "adv_$DEFENDER"/*.csv
cp -R "adv_$DEFENDER" "adv_Sliding_$DEFENDER" # sliding

# DEFENDER="sarOrigLengthened"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"
# rm "adv_$DEFENDER"/*.csv


# DEFENDER="sarSinPackets"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"
# rm "adv_$DEFENDER"/*.csv
# cp -R "adv_$DEFENDER" "adv_Sliding_$DEFENDER" # sliding
# rm "adv_Sliding_$DEFENDER"/*.csv

# do the rest later

# DEFENDER="sarHierNorm"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"

# DEFENDER="sarHierPackets"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"

# DEFENDER="ddSinNorm"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"


# DEFENDER="ddSinPackets"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"

# DEFENDER="ddHierNorm"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"

# Do this later.
# DEFENDER="ddHierPackets"
# cp -R ../$1/$DEFENDER "adv_$DEFENDER"



