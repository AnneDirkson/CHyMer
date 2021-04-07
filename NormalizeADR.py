##This is the script for normalizing ADR which is largely based on the BioSyn method
# by Sung et al. I (A.R. Dirkson) adapted the composite splitting script to allow for
# splitting in unlabelled data + reconfigured the input data and input targets.
# I have switched off the abbreviation expansion in the biosyn module as it has already been
# done during pre-processing. I have also set lower case; remove punc and split composites
# to True.

from biosyn.query_preprocess_inference import QueryPreprocess

class ADRNormalizer():

    def __init__(self):
        pass

    def main(self, modelpath):
        QueryPreprocess().main(input_dir, output_dir)
