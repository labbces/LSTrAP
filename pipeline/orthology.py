import os
import subprocess
from shutil import copyfile

from cluster import wait_for_job

from .base import PipelineBase


class OrthologyPipeline(PipelineBase):

    def run_orthofinder(self):
        """
        Runs orthofinder for all genomes
        """
        orthofinder_dir = self.dp['GLOBAL']['orthofinder_output']
        orthofinder_cores = int(self.dp['GLOBAL']['orthofinder_cores'])

        os.makedirs(os.path.dirname(orthofinder_dir), exist_ok=True)

        filename, jobname = self.write_submission_script("orthofinder_%d",
                                                         self.python_module + ' ' +
                                                         self.blast_module + ' ' +
                                                         self.mcl_module,
                                                         self.orthofinder_cmd,
                                                         "orthofinder_%d.sh")

        for g in self.genomes:
            copyfile(self.dp[g]['protein_fasta'], orthofinder_dir)

        subprocess.call(["qsub", "-v", "fasta_dir=" + orthofinder_dir + ",num_cores=" + orthofinder_cores, filename])

         # wait for all jobs to complete
        wait_for_job(jobname)

        # remove the submission script
        os.remove(filename)

        # remove OUT_ files
        PipelineBase.clean_out_files(jobname)

        print("Done\n\n")