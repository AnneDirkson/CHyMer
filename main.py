##This is the main script of CHyMER
#
# Author: Anne Dirkson
# Date: 6 April 2021
#
# This script imports the methods to extract and normalize ADR; as well as those to link them to the most likely medication.
# Here data is reformatted for each step and additional attributes are added

from NormalizeADR import ADRNormalizer
from ExtractADR import ADRExtractor
from DrugLinker import DrugLinker
import pandas as pd
import argparse
import pickle
import os

class RunPipeline():

    def __init__(self):
        pass

    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


    def get_messages_of_ADR(self, df, orig_data):
        # data.post_id = data.nw_ix.apply(lambda x: change_postid(x))
        times = []
        sents = []
        for ix in df3.post_id:
            sent = orig_data[orig_data.post_id == ix].word.iloc[0]
            time = orig_data[orig_data.post_id == ix].time.iloc[0][0]
            sents.append(" ".join(sent))
            times.append(time)

        df2 = pd.concat([df, pd.Series(sents, name='message'), pd.Series(times, name='time')], axis=1)

        return df2

    # def adjust_col (row):
    #     return row[0]

    def main(self, args):
        # orig_data = pd.read_csv(args.datapath, sep= '\t')
        #
        # def adapt_strings(row):
        #     row2 = row.replace('[', ' ')
        #     row3 = row2.split(',')
        #
        #     return row3
        #
        # orig_data.words = orig_data.words.apply(lambda x: adapt_strings(x))
        # orig_data.tag = orig_data.tag.apply(lambda x: adapt_strings(x))
        #
        # print(orig_data.words.iloc[0])

        orig_data = self.load_obj(args.datapath)
        print(orig_data.head())
        # print(orig_data.tag.iloc[0][7])
        norm_model_dir = args.norm_model_dir
        ner_model_dir = args.ner_model_dir

        ##preprocess?

        ### run extraction
        ner_outpath = './output/NER/'

        # df = ADRExtractor().main(orig_data, ner_model_dir, ner_outpath)
        # print(df.head())
        ##run normalization

        if args.use_cuda:
            u = True
        else:
            u = False

        # NormalizedResults = ADRNormalizer().main(df, output_dir1 = 'output/Unprocessed/', output_dir2 = 'output/Processed/', model_dir= norm_model_dir, dictionary_path= './data/ConceptDictionary.txt', use_cuda=u)
        #
        # df2 = self.get_messages_of_ADR(self, NormalizedResults, orig_data)
        #
        # if args.restricted_druglst:
        #     restricted_list = pd.read_csv('./data/restricted_druglist.txt', header = None)
        #
        #     df3 = DrugLinker().main(df2, restricted = True, possible_drugs = restricted_list)
        # else:
        #     df3 = DrugLinker().main(df2, restricted=False, possible_drugs=None)
        #
        # df3.to_csv('./output/DrugLinkedADR.tsv', sep = '\t', index = False)


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Extraction and normalization ADR')

    # Required
    parser.add_argument('--ner_model_dir', required=True, help='Directory for NER predictors')
    parser.add_argument('--norm_model_dir', required=True, help='Directory for normalization model')
    # parser.add_argument('--dictionary_path', type=str, required=True, help='dictionary path')
    parser.add_argument('--datapath', type=str, required=True, help='data set to evaluate')


    # Run settings
    parser.add_argument('--restricted_drugs', action="store_true")
    parser.add_argument('--use_cuda',  action="store_true")
    parser.add_argument('--output_dir', type=str, default='./output/', help='Directory for output')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    RunPipeline().main(args)

##syn_cui_text is the original synonym the term was linked to
##cannot share files below due to SNOMED CT license
# DefaultName = []
# LvlUpCUI = []
# LvlUpName = []
#
# for a in NormalizedResults.cui:
#      DefaultName.append(self.default_names[a])
#      LvlUpCUI.append(self.lvl_up_dict[a])
# for b in LvlUpCUI:
#     LvlUpName.append(self.default_names[b])

# df3['thread_id'] = df3.thread_id.apply(lambda x: adjust_col(x))
# drugdf['thread_id'] = drugdf.thread_id.apply(lambda x: adjust_col(x))
# NormalizedResults2 = pd.concat([NormalizedResults, pd.Series(DefaultName, name='cui_txt'), pd.Series(LvlUpCUI, name = 'lvl_up_cui'), pd.Series(LvlUpName, name= 'lvl_up_name')], axis=1)





