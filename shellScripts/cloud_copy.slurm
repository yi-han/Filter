#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1-00:00:00
#SBATCH --account=punim0636
#SBATCH --partition=cloud
#SBATCH --job-name=copyStuff
# Send yourself an email when the job:
# aborts abnormally (fails)
#SBATCH --mail-type=FAIL
# ends successfully
#SBATCH --mail-type=END

# Use this email address:
#SBATCH --mail-user=jpattison@student.unimelb.edu.au


cp -R ../$1/$2 $3
rm $3/*.csv


# my project file /data/projects/punim0621