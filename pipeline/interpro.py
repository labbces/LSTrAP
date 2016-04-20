import os
import configparser

from utils.parser.fasta import Fasta
from math import ceil
from pipeline.base import PipelineBase


class InterProPipeline(PipelineBase):

    def run_interproscan(self):

        def split_fasta(file, chunks, output_directory, filenames="proteins_%d.fasta"):
            fasta = Fasta()
            fasta.readfile(file)

            for k in fasta.sequences.keys():
                fasta.sequences[k] = fasta.sequences[k].replace('*', '')

            seq_per_chunk = ceil(len(fasta.sequences.keys())/chunks)

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            for i in range(1, chunks+1):
                subset = fasta.remove_subset(seq_per_chunk)
                filename = filenames % i
                filename = os.path.join(output_directory, filename)

                subset.writefile(filename)

        filename, jobname = self.write_batch_submission_script("interproscan_%d", self.interproscan_module, self.interproscan_cmd, "%interproscan_%d.sh")


        os.remove(filename)
        PipelineBase.clean_out_files(jobname)
