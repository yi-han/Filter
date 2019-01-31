# if we need to rerun the attacks we use this. This is a custom file so review before using.

cp ~/runAttacks.py runAttacks.py
cp ~/slurms_gpgpu_v3.sh slurms_gpgpu_v3.sh
./slurms_gpgpu_v3.sh
# for file in runDDQN.py runDDQNAdditional.py runDDQNAdditional.py runDDQNMalialis.py runDDQNNetQuick.py runDDQNHundred.py; do
# 	sed "s/loadAttacks = False/loadAttacks = True/g" $file -i
# done
# sbatch --depend=afterok:7306000:7306003 exp_attacks.slurm