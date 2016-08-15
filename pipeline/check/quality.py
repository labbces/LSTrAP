import sys
import re

__bad_fields = ['no_feature', 'ambiguous', 'too_low_aQual', 'not_aligned', 'alignment_not_unique']


def htseq_count_quality(filename, cutoff=1, log=None):
    """
    UNUSED: Thes generated a N50 like metric (how many genes are responsable for 50 % of the transcripts). This doesn't
    work for e.g. pollen

    :param filename: htseq file to check
    :param cutoff: cutoff value
    :param log: file to print warnings to
    :return: Boolean True is check is OK, False if not
    """
    print("checking quality of htseq-count")
    values = []
    total_count = 0

    with open(filename, "r") as fin:
        for l in fin:
            gene, count = l.strip().split('\t')
            if all([bf not in gene for bf in __bad_fields]):
                values.append(int(count))
                total_count += int(count)

    if total_count == 0:
        print("N50 check for", filename, "failed. No reads found")
        return False

    values.sort(reverse=True)

    # write lengths to log file !
    if log is not None:
        current_count = 0
        for e, v in enumerate(values, start=1):
            current_count += v
            if current_count > total_count / 2:
                print('N50 for', filename, ':', e, file=log)
                break

    current_count = 0
    for e, v in enumerate(values, start=1):
        current_count += v
        if current_count > total_count/2:
            if e >= cutoff:
                print(filename, e, cutoff, current_count, total_count, len(values))
                return True

            break

    print("N50 check for", filename, "failed.", e, cutoff)
    return False


def check_tophat(filename, cutoff=65, log=None):
    """
    Checks the alignment summary of TopHat's output, if it passes it returns true, else false
    Optionally information can be written to a log file

    :param filename: align_summary.txt to check
    :param cutoff: If the percentage of mapped reads is below this the sample won't pass
    :return: True if the sample passed, false otherwise
    """

    re_mapped = re.compile('Mapped   :.*\(\s*(.*)% of input\)')

    with open(filename, 'r') as f:
        lines = '\t'.join(f.readlines())
        hits = re_mapped.search(lines)
        if hits:
            value = float(hits.group(1))
            if value >= cutoff:
                return True
            else:
                if log is not None:
                    print('WARNING:', filename, 'didn\'t pass TopHat Quality check!', value, 'reads mapped. Cutoff,',
                          cutoff, file=log)

    return False


def check_htseq(filename):
    """
    Checks the mapping statistics in htseq files how many reads map into coding sequences

    :param filename: htseq file to check
    :return: percentage of reads that map inside a genome
    """

    return 0
