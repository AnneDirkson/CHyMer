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
    def run_data_through_models(self, modeldir, outpath, X2): ## X2 is hte input - just a list of joined sentences
        # modeldir = 'C://Users//dirksonar//Documents//Data/Project12_pipeline/BERTfinal/' ##te
        lst_models = ['predictor_seed1', 'predictor_seed2', 'predictor_seed4', 'predictor_seed8', 'predictor_seed16',
                       'predictor_seed32', 'predictor_seed64', 'predictor_seed128', 'predictor_seed256', 'predictor_seed512']
        seednums = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        self.alllbls = []


        for a,b in zip(lst_models, seednums):
            model = modeldir + '\\' + a
            predictor = ktrain.load_predictor(model)



            out = []
            for num, sent in enumerate(X2):
                # if num % 1000 == 0:
                #     print(num)

                o = predictor.predict(sent, return_proba=False)
                out.append(o)
            # print(out)
            outpath1 = outpath + 'lbls_seed' + str(b)
            self.save_obj(out, outpath1)

            tmp = []
            for s in out:
                s2 = []
                for w in s:
                    s2.append(w[1])
                tmp.append(s2)
            self.alllbls.append(tmp)

            if b == 1:  ##grab words only for hte first one
                self.nw_words = []
                tmp = []
                for s in out:
                    s2 = []
                    for w in s:
                        s2.append(w[0])
                    tmp.append(s2)
                self.nw_words = tmp
                # outpath1 = outpath + 'words_BERT'
                # self.save_obj(nw_w, outpath1)

    # majority voting
    def load_results(self, fpath):
        seeds = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

        self.alllbls = []
        self.nw_words = []

        for s in seeds:
            probas = self.load_obj(fpath + 'lbls_seed' + str(s))
            tmp = []
            for p in probas:
                s2 = []
                for w in p:
                    s2.append(w[1])
                tmp.append(s2)
            self.alllbls.append(tmp)

            if s == 1:
                tmp = []
                for p in probas:
                    s2 = []
                    for w in p:
                        s2.append(w[0])
                    tmp.append(s2)
                self.nw_words = tmp


    def simple_majority_vote(self):  ##rule if another as likely as O then include - all_probs are just the labls

        out = []

        for s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 in zip(self.alllbls[0], self.alllbls[1], self.alllbls[2], self.alllbls[3],
                                                           self.alllbls[4], self.alllbls[5], self.alllbls[6], self.alllbls[7],
                                                           self.alllbls[8], self.alllbls[9]):
            nw_sent = []
            for w1, w2, w3, w4, w5, w6, w7, w8, w9, w10 in zip(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10):

                try:
                    m = stat.mode([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10])


                except:
                    c = Counter([w1, w2, w3, w4, w5, w6, w7, w8, w9, w10])
                    g = c.most_common(2)
                    u = [i[0] for i in g]
                    #                 print(g)
                    if 'B-ADR' in u:
                        m = 'B-ADR'
                    elif 'I-ADR' in u:
                        m = 'I-ADR'


                nw_sent.append(m)
            out.append(nw_sent)
        return out

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
        # self.run_data_through_models(modeldir, outpath, X2)

        self.load_results(outpath)

        ## majority voting
        out = self.simple_majority_vote()
        # print(out[0])

        df2 = pd.concat([df, pd.Series(out, name='tag')], axis=1)
        # print(df2.head())

        ##extracting ADR phrases from the tags
        df3 = self.extract_from_tags(df2)
        return df3