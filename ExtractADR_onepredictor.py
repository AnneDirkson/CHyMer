##This script combines all the steps for ADR extraction


from ExtractEntities import EntityExtractor
from collections import Counter
import pickle
import statistics as stat

import ktrain
# from ktrain import text as txt
# import tensorflow as tf
# import numpy as np
import pandas as pd

class ADRExtractor():

    def __init__(self):
        pass

    def load_obj(self, name):
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding='latin1')

    def save_obj(self, obj, name):
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    ## models running
    def run_data_through_model(self, modeldir, outpath, X2): ## X2 is hte input - just a list of joined sentences
        # modeldir = 'C://Users//dirksonar//Documents//Data/Project12_pipeline/BERTfinal/' ##te
        predictor = ktrain.load_predictor(modeldir)

        out = []
        for num, sent in enumerate(X2):
            # if num % 1000 == 0:
            #     print(num)

            o = predictor.predict(sent, return_proba=False)
            out.append(o)
        # print(out)
        self.save_obj(out, outpath)

        tags = []

        for s in out:
            s2 = []
            for w in s:
                s2.append(w[1])
            tags.append(s2)
        print(tags[0])
        # self.alllbls.append(tmp)
        #
        self.nw_words = []

        for s in out:
            s2 = []
            for w in s:
                s2.append(w[0])
            self.nw_words.append(s2)
        # self.nw_words = tmp

        return tags

    ##extracting ADR phrases from the tags

    def looseI_toB(self, tgs, tagtype):
        itag = 'I-' + tagtype
        nwtgs = tgs  ##initialize
        for num, t in enumerate(tgs):
            if t.endswith(itag) and tgs[num - 1] == 'O':
                t2 = t.replace('I', 'B')
                nwtgs[num] == t2
        return nwtgs

    def extract_from_tags(self, df):
        words = list(df.words)
        # print(df.tag)
        predlbls = list(df.tag)
        threadix = df.thread_id
        ix = df.post_id
        nwtgs = [self.looseI_toB(p, tagtype = 'ADR') for p in predlbls]
        # print(predlbls)
        # print(nwtgs[0])
        # print(self.nw_words[0])

        all_adr, all_tgs, all_ix, ent_ranges = EntityExtractor().main(self.nw_words, nwtgs)
        # print(all_adr)

        adrlst = []
        nwthreadix = []
        nwix = []
        ent_start = []
        ent_end = []

        for a, b, c, d in zip(all_adr, ent_ranges, threadix, ix):
            if a != []:
                for i, j in zip(a, b):
                    adrlst.append(i)
                    nwthreadix.append(c)
                    nwix.append(d)
                    ent_start.append(j[0])
                    ent_end.append(j[-1])
            else:
                pass

        df = pd.concat([pd.Series(adrlst, name='ent'), pd.Series(nwthreadix, name='thread_id'),
                        pd.Series(nwix, name='post_id'), pd.Series(ent_start, name='ent_start'),
                        pd.Series(ent_end, name='ent_end')], axis=1)

        return df


    def main(self, df, modeldir, outpath):
        ##reformat data
        words = df.words
        # X = list(words)
        X2 = [" ".join(w) for w in list(words)]
        print(X2[0])

        ## models running
        tags = self.run_data_through_model(modeldir, outpath, X2)

        #self.load_results(outpath)

        ## majority voting -- not included with single predictor
        #out = self.simple_majority_vote()
        # print(out[0])

        df2 = pd.concat([df, pd.Series(tags, name='tag')], axis=1)
        print(df2.head())

        ##extracting ADR phrases from the tags
        df3 = self.extract_from_tags(df2)

        self.save_obj(df3, outpath + 'Output_NER')
        return df3