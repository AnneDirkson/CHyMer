import argparse
import logging
import os
import json
from tqdm import tqdm
from .utils import (
    evaluate
)
from .data_loader import DictionaryDataset
from .data_loader import QueryDataset
from .biosyn import BioSyn
LOGGER = logging.getLogger()

class RunNormalizer():

    def __init__(self):
        pass

    def parse_args(self):
        """
        Parse input arguments
        """
        parser = argparse.ArgumentParser(description='BioSyn evaluation')

        # Required
        parser.add_argument('--model_name_or_path', required=True, help='Directory for model')
        parser.add_argument('--dictionary_path', type=str, required=True, help='dictionary path')
        parser.add_argument('--data_dir', type=str, required=True, help='data set to evaluate')

        # Run settings
        parser.add_argument('--use_cuda', action="store_true")
        parser.add_argument('--topk', type=int, default=20)
        parser.add_argument('--score_mode', type=str, default='hybrid', help='hybrid/dense/sparse')
        parser.add_argument('--output_dir', type=str, default='./output/', help='Directory for output')
        parser.add_argument('--filter_composite', action="store_true", help="filter out composite mention queries")
        parser.add_argument('--filter_duplicate', action="store_true", help="filter out duplicate queries")
        parser.add_argument('--save_predictions', action="store_true", help="whether to save predictions")

        # Tokenizer settings
        parser.add_argument('--max_length', default=25, type=int)

        args = parser.parse_args()
        return args
    
    def init_logging(self):
        LOGGER.setLevel(logging.INFO)
        fmt = logging.Formatter('%(asctime)s: [ %(message)s ]',
                                '%m/%d/%Y %I:%M:%S %p')
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        LOGGER.addHandler(console)

    def load_dictionary(self, dictionary_path):
        dictionary = DictionaryDataset(
            dictionary_path = dictionary_path
        )
        return dictionary.data

    def load_queries(self, data_dir, filter_composite, filter_duplicate):
        dataset = QueryDataset(
            data_dir=data_dir,
            filter_composite=filter_composite,
            filter_duplicate=filter_duplicate
        )
        return dataset.data
                
    def main(self, model_dir, dictionary_path, data_dir, use_cuda, topk=10):
        self.init_logging()
        #print(args)

        # load dictionary and data
        eval_dictionary = self.load_dictionary(dictionary_path=dictionary_path)
        eval_queries = self.load_queries(
            data_dir=data_dir,
            filter_composite=False,
            filter_duplicate=True
        )

        biosyn = BioSyn(
            max_length=25,
            use_cuda=use_cuda
        )
        biosyn.load_model(
            model_name_or_path=model_dir,
        )

        result_evalset = evaluate(
            biosyn=biosyn,
            eval_dictionary=eval_dictionary,
            eval_queries=eval_queries,
            topk=topk,
        )

        # print(result_evalset)
        # LOGGER.info("acc@1={}".format(result_evalset['acc1']))
        # LOGGER.info("acc@5={}".format(result_evalset['acc5']))

        output_dir = './output/Normalized/'
        output_file = os.path.join(output_dir,"predictions_eval.json")
        with open(output_file, 'w') as f:
            json.dump(result_evalset, f, indent=2)

        return result_evalset

if __name__ == '__main__':
    args = RunNormalizer().parse_args()
    RunNormalizer().main(args)
