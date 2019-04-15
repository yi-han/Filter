#!/bin/bash

# We assume $1 is the name of the folder we are copying from

# sarsaOrig
EV_MODE="Over_"

DEFENDER="sarOrig"
echo ../$1/$DEFENDER "dd$EV_MODE$DEFENDER"

cp -R ../$1/$DEFENDER "dd$EV_MODE$DEFENDER"
rm "dd$EV_MODE$DEFENDER"/*.csv

# sliding
TEMP_DEF="sliding"
cp -R "dd$EV_MODE$DEFENDER" "dd$EV_MODE$TEMP_DEF"

DEFENDER="sarSinDD"
cp -R ../$1/$DEFENDER "dd$EV_MODE$DEFENDER"

# DEFENDER="sarHier"
# cp -R ../$1/$DEFENDER "dd$EV_MODE$DEFENDER"
# # cp -R ../expTwo64ConOverflow/sarHier ddOver_sarHier

# DEFENDER="ddSin"
# cp -R ../$1/$DEFENDER "dd$EV_MODE$DEFENDER"

# DEFENDER="ddHier"
# cp -R ../$1/$DEFENDER "dd$EV_MODE$DEFENDER"


rm */*.csv