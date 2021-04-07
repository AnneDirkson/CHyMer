def looseI_toB(self, tgs, tagtype):
    itag = 'I-' + tagtype
    nwtgs = tgs  ##initialize
    change = 0
    for num, t in enumerate(tgs):
        if t.endswith(itag) and tgs[num - 1] == 'O':
            t2 = t.replace('I', 'B')
            nwtgs[num] == t2
    return nwtgs


def extract_entities(self, pred, predlbls):
    #         nwpred = self.remove_punc_ypred(pred)

    #         nwpred2 = []
    #         for i in nwpred:
    #             t= []
    #             t = [j[0] for j in i]
    #             nwpred2.append(t)

    #         nwpredlbls = []
    #         for i in nwpred:
    #             t= []
    #             t = [j[1] for j in i]
    #             nwpredlbls.append(t)

    #         nwpredlbls2 = [link_up_loose_I(r) for r in nwpredlbls]

    #         nwpredlbls2 = [self.looseI_toB(r, tagtype = 'ADR') for r in predlbls]
    all_adr, all_tgs, all_ix, ent_ranges = EntityExtractor().main(pred, predlbls)
    return all_adr, all_tgs, all_ix, ent_ranges


def main(self, words, predlbls, threadix, ix):
    all_adr, all_tgs, all_ix, ent_ranges = self.extract_entities(words, predlbls)

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