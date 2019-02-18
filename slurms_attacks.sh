# if we need to rerun the attacks we use this. This is a custom file so review before using.

# cp ~/runAttacks.py runAttacks.py
# cp ~/slurms_gpgpu_v3.sh slurms_gpgpu_v3.sh
# ./slurms_gpgpu_v3.sh


 
for file in runDDQN.py runDDQNAdditional.py runDDQNHundred.py runDDQNMalialis.py runDDQNNetQuick.py runSarsaDDQNCopy.py runSarsaAdditional.py runSarsaNoOverdrive.py; do
	sed -i.bak "s/loadAttacks = False/loadAttacks = True/g" $file
	sed "s/runDDQN.py/$file/g" exp_physical_ddqn.slurm > output.slurm
	rm $file.bak
	sed -i.bak "s/0 2/0 10/g" output.slurm
	sed -i.bak "s/samplePath/$1/g" output.slurm
	sed -i.bak 's/sampleDDQNText/longTest/g' output.slurm
	sbatch output.slurm
	rm output.slurm.bak
done
