import sys


class Fasta:
    def __init__(self):
        self.sequences = {}

    def remove_subset(self, length):
        """
        Removes a set of sequences and returns those as a subset

        :param length: number of sequences to remove
        :return: Fasta object with the sequences removed from the current one
        """
        output = Fasta()
        keys = list(self.sequences.keys())
        output.sequences = {k: self.sequences[k] for k in keys[:length]}

        self.sequences = {k: self.sequences[k] for k in keys[length:]}

        return output

    def readfile(self, filename):
        """
        Reads a fasta file to the dictionary

        :param filename: file to read
        """
        print("Reading FASTA file:" + filename + "...", file=sys.stderr)

        # Initialize variables
        name = ''
        sequence = []
        count = 1

        # open file
        f = open(filename, 'r')

        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                # ignore if first
                if not name == '':
                    self.sequences[name] = ''.join(sequence)
                    count += 1
                name = line.lstrip('>')
                sequence = []
            else:
                sequence.append(line)

        # add last gene
        self.sequences[name] = ''.join(sequence)

        f.close()
        print("Done! (found ", count, " sequences)", file=sys.stderr)

    def writefile(self, filename):
        """
        writes the sequences back to a fasta file

        :param filename: file to write to
        """
        with open(filename, 'w') as f:
            for k, v in self.sequences.items():
                print(">" + k, file=f)
                print(v, file=f)
