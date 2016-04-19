import os
import configparser

from utils.parser.fasta import Fasta
from math import ceil
from pipeline.base import PipelineBase


class InterProPipeline(PipelineBase):

    def run_interproscan(self):
        filename, jobname = self.write_submission_script("interproscan_%d", self.interproscan_module, self.interproscan_cmd, "%interproscan_%d.sh")




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


def run_interpro(config):
    print("Running InterProScan using", config)

    cp = configparser.ConfigParser()
    cp.read(config)

    interpro_module = cp['DEFAULT']['interpro_module']
    interpro_cmd = cp['DEFAULT']['interpro_cmd']
    genomes = cp['DEFAULT']['genomes'].split(';')
    email = None if cp['DEFAULT']['email'] == 'None' else cp['DEFAULT']['email']
    jobs = int(cp['DEFAULT']['jobs'])

    for g in genomes:
        input = cp[g]['input']
        output = cp[g]['output']
        split_filenames = cp[g]['split_filenames']
        out_filenames = cp[g]['out_filenames']

        script = 'run_interpro_'+g+'.sh'
        job_name = 'interproscan_' + g

        split_fasta(input, jobs, output, filenames=split_filenames)
        generate_script(script, job_name, jobs,
                        os.path.join(output, split_filenames),
                        os.path.join(output, out_filenames),
                        interpro_module=interpro_module,
                        interpro_cmd=interpro_cmd,
                        email=email)

    print("Done !")
