#!/bin/bash

# We assume $1 is the name of the folder we are copying from

# sarsaOrig

DEFENDER="sarOrig"


echo ../$1/$DEFENDER "adv_$DEFENDER"
rsync -avz --exclude="*.csv" --include="*" ../$1/$DEFENDER/ "adv_$DEFENDER"

#cp -R ../$1/$DEFENDER "adv_$DEFENDER"
#rm "adv_$DEFENDER"/*.csv

DEFENDER="sarOrigLengthened"
rsync -avz --exclude="*.csv" --include="*" ../$1/$DEFENDER/ "adv_$DEFENDER"
#rsync -avz --exclude="*.csv" --include="*" ../$1/$DEFENDER/ "adv_Sliding_$DEFENDER"




DEFENDER="sarSinPackets"
rsync -avz --exclude="*.csv" --include="*" ../$1/$DEFENDER/ "adv_$DEFENDER"
rsync -avz --exclude="*.csv" --include="*" ../$1/$DEFENDER/ "adv_Sliding_$DEFENDER"


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



