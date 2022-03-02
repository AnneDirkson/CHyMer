import argparse
import os
import pdb
import pickle
from data_loader import DictionaryDataset
from data_loader import QueryDataset
from biosyn import (
    BioSyn)

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='BioSyn Inference')

    # Required
    parser.add_argument('--mention', type=str, required=True, help='mention to normalize')
    parser.add_argument('--model_name_or_path', required=True, help='Directory for model')

    # Settings
    parser.add_argument('--show_embeddings',  action="store_true")
    parser.add_argument('--show_predictions',  action="store_true")
    parser.add_argument('--dictionary_path', type=str, default=None, help='dictionary path')
    parser.add_argument('--use_cuda',  action="store_true")
    
    args = parser.parse_args()
    return args
    
def cache_or_load_dictionary(biosyn, model_name_or_path, dictionary_path):
    dictionary_name = os.path.splitext(os.path.basename(args.dictionary_path))[0]
    
    cached_dictionary_path = os.path.join(
        './tmp',
        f"cached_{model_name_or_path.split('/')[-1]}_{dictionary_name}.pk"
    )

    # If exist, load the cached dictionary
    if os.path.exists(cached_dictionary_path):
        with open(cached_dictionary_path, 'rb') as fin:
            cached_dictionary = pickle.load(fin)
        print("Loaded dictionary from cached file {}".format(cached_dictionary_path))

        dictionary, dict_sparse_embeds, dict_dense_embeds = (
            cached_dictionary['dictionary'],
            cached_dictionary['dict_sparse_embeds'],
            cached_dictionary['dict_dense_embeds'],
        )

    else:
        dictionary = DictionaryDataset(dictionary_path = dictionary_path).data
        dictionary_names = dictionary[:,0]
        dict_sparse_embeds = biosyn.embed_sparse(names=dictionary_names, show_progress=True)
        dict_dense_embeds = biosyn.embed_dense(names=dictionary_names, show_progress=True)
        cached_dictionary = {
            'dictionary': dictionary,
            'dict_sparse_embeds' : dict_sparse_embeds,
            'dict_dense_embeds' : dict_dense_embeds
        }

        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        with open(cached_dictionary_path, 'wb') as fin:
            pickle.dump(cached_dictionary, fin)
        print("Saving dictionary into cached file {}".format(cached_dictionary_path))

    return dictionary, dict_sparse_embeds, dict_dense_embeds

def main(args):
    # load biosyn model
    biosyn = BioSyn(
        use_cuda=False,
        max_length=25
    )
    
    biosyn.load_model(model_name_or_path=args.model_name_or_path)
    # preprocess mention
    #mention = TextPreprocess().run(args.mention)
    mention = args.mention
    
    # embed mention
    mention_sparse_embeds = biosyn.embed_sparse(names=[mention])
    mention_dense_embeds = biosyn.embed_dense(names=[mention])
    
    output = {
        'mention': args.mention,
    }

    if args.show_embeddings:
        output = {
            'mention': args.mention,
            'mention_sparse_embeds': mention_sparse_embeds.squeeze(0),
            'mention_dense_embeds': mention_dense_embeds.squeeze(0)
        }

    if args.show_predictions:
        if args.dictionary_path == None:
            print('insert the dictionary path')
            return

        # cache or load dictionary
        dictionary, dict_sparse_embeds, dict_dense_embeds = cache_or_load_dictionary(biosyn, args.model_name_or_path, args.dictionary_path)

        # calcuate score matrix and get top 5
        sparse_score_matrix = biosyn.get_score_matrix(
            query_embeds=mention_sparse_embeds,
            dict_embeds=dict_sparse_embeds
        )
        dense_score_matrix = biosyn.get_score_matrix(
            query_embeds=mention_dense_embeds,
            dict_embeds=dict_dense_embeds
        )
        sparse_weight = biosyn.get_sparse_weight().item()
        hybrid_score_matrix = sparse_weight * sparse_score_matrix + dense_score_matrix
        hybrid_candidate_idxs = biosyn.retrieve_candidate(
            score_matrix = hybrid_score_matrix, 
            topk = 5
        )

        # get predictions from dictionary
        predictions = dictionary[hybrid_candidate_idxs].squeeze(0)
        output['predictions'] = []

        for prediction in predictions:
            predicted_name = prediction[0]
            predicted_id = prediction[1]
            output['predictions'].append({
                'name': predicted_name,
                'id': predicted_id
            })

    print(output)

if __name__ == '__main__':
    args = parse_args()
    main(args)