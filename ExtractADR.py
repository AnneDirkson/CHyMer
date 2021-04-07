##This script combines all the steps for ADR extraction


from ExtractEntities import EntityExtractor
from collections import Counter

class ADRExtractor():

    def __init__(self):
        pass

    ## models running

    ## majority voting
    def load_results(self, output_dir):
        seeds = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

        alllbls = []

        for s in seeds:
            probas = load_obj(fpath + 'seed' + str(s))
            tmp = []
            for s in probas:
                s2 = []
                for w in s:
                    s2.append(w[1])
                tmp.append(s2)
            alllbls.append(tmp)
        return alllbls

    def simple_majority_vote(self, all_probs):  ##rule if another as likely as O then include - all_probs are just the labls

        out = []

        for s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 in zip(all_probs[0], all_probs[1], all_probs[2], all_probs[3],
                                                           all_probs[4], all_probs[5], all_probs[6], all_probs[7],
                                                           all_probs[8], all_probs[9]):
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
        words = df.words
        predlbls = df.tag
        threadix = df.thread_id
        ix = df.post_id
        nwtgs = self.looseI_toB(predlbls, tagtype = 'ADR')
        all_adr, all_tgs, all_ix, ent_ranges = EntityExtractor().main(words, predlbls)

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


    def main(self):
        ## models running

        ## majority voting
        alllbls = self.load_results(output_dir)
        out = self.simple_majority_vote(alllbls)

        df2 = pd.concat([df, pd.Series(out, name='tag')], axis=1)

        ##extracting ADR phrases from the tags
        df3 = extract_from_tags(self, df2)
        return df3