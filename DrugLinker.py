##In this script drugs are extracted from conversational messages and the extracted ADR are linked to the most likely
##medication

import pandas as pd
import re

class DrugLinker():

    def __init__(self):
        self.druglist = pd.read_csv('./data/fdadrugslist.txt', header = None)
        self.WORD = '[A-Za-z0-9]+'
        self.WORD2 = '[A-Za-z]+'
        self.ONLYHYPHEN = '[-]+'
        self.punclst = ["_", "%", '+', "&", "<", ">", ")", "(", "[", "]", ".", ",", "/", ";", ":", "!", "?", '"',
                            "$", "'", '#', '-', "|", "~", "=", "`", "*"]


    def extract_drug_data(self, df):  ##input needs to be same as entity linker
        fdalst = self.druglist
        fdalst.columns=['drugs']
        # print(fdalst[:10])
        nwfdalst = []
        for i in fdalst.drugs:

            if len(i) > 2:
                nwfdalst.append(i)

        # print(len(nwfdalst))

        # nwfdalst = [i for i in fdalst if len(i) > 2]

        nwfdalst.extend(['avapritinib', 'ripretinib'])

        #print(nwfdalst[:10])

        drugsnames = []
        threadixs = []
        ixs = []
        start = []
        end = []

        for a, b, c in zip(df.message, df.thread_id, df.post_id):
            drugs = []
            s = []
            e = []
            # print(a)

            try:
                for num, j in enumerate(a):
                # print(j)
                    if re.fullmatch(self.WORD2, j) != None:
                        # print(j.lower())
                        if j.lower() in nwfdalst:
                            # print(j.lower())
                            drugs.append(j.lower())
                            s.append(num)
                            e.append(num)
            except:
                pass



            if drugs != []:
                drugsnames.append(drugs)
                start.append(s)
                end.append(e)
                threadixs.append(b)
                ixs.append(c)

        df = pd.concat([pd.Series(ixs, name='post_id'), pd.Series(threadixs, name='thread_id'),
                        pd.Series(drugsnames, name='found_drugs'), pd.Series(start, name='ent_start'),
                        pd.Series(end, name='ent_end')], axis=1)

        return df



    def nearest_drug_samepost(self, data, drugdf, possible_drugs=None, restricted=False, only_before=False):

        out = []
        dist = []

        for i, j, m in zip(data.ent_start, data.post_id, data.ent_end):
            chosen_drug = None

            ##find nearest before
            start_ent = i
            y = drugdf[drugdf.post_id == j]
            if len(y.found_drugs) == 0:
                out.append(None)
                dist.append(None)

            elif len(y.found_drugs.iloc[0]) == 1:

                if restricted == True:
                    if y.found_drugs.iloc[0][0] in possible_drugs:
                        out.append(y.found_drugs.iloc[0][0])
                        ##calculate distance
                        e = y.ent_end.iloc[0][0]
                        s = y.ent_start.iloc[0][0]
                        if s > m:
                            dist.append(s - m)
                        elif s < m and e < i:  ##in between
                            dist.append(0)
                        else:
                            dist.append(i - e)
                    else:
                        dist.append(None)
                        out.append(None)

                else:
                    out.append(y.found_drugs.iloc[0][0])
                    ##calculate distance
                    e = y.ent_end.iloc[0][0]
                    s = y.ent_start.iloc[0][0]
                    if s > m:
                        dist.append(s - m)
                    elif s < m and e < i:  ##in between
                        dist.append(0)
                    else:
                        dist.append(i - e)


            else:  ##we have to choose
                cur_dist = 999
                for drug, e, s in zip(y.found_drugs.iloc[0], y.ent_end.iloc[0], y.ent_start.iloc[0]):
                    if restricted == True:
                        if drug not in possible_drugs:
                            break
                    if e < i:
                        chosen_drug = drug
                        cur_dist = i - e
                    elif e > i and s < m:
                        cur_dist = 0
                        chosen_drug = drug

                    else:
                        if only_before == False:  ## also look after entity
                            if s > m:  ## after the entity
                                if (s - m) < cur_dist:
                                    chosen_drug = drug
                                    cur_dist = s - m
                                else:
                                    pass
                        else:
                            pass
                if cur_dist == 999:
                    dist.append(None)
                else:
                    dist.append(cur_dist)
                out.append(chosen_drug)

        return out, dist

    def first_drug(self, data, drugdf, possible_drugs=None,
                   restricted=False):  ##only allow for drugs mentioned earlier

        out = []
        for a, n in zip(data.thread_id, data.post_id):
            #             y = aggdrugdf[aggdrugdf.thread_id == a]
            y = drugdf[drugdf.thread_id == a]
            y = y.reset_index(drop=True)
            ##fix the ordering
            ps = [x.split('_')[1] for x in y.post_id]

            ps2 = [int(i) for i in ps]

            y2 = pd.concat([y, pd.Series(ps2, name='post_id2')], axis=1)
            y2 = y2.sort_values(by='post_id2', axis=0, ascending=True)

            ##subset
            cur = n.split('_')[1]
            cur2 = int(cur)

            y2b = y2[y2.post_id2 < cur2]

            #             print(y2b.head())

            y3 = list(y2b.found_drugs)

            if len(y3) == 0:  # there are none in this thread
                out.append(None)
            else:
                if restricted == True:

                    flat = [i for j in y3 for i in j]
                    flat2 = [i for i in flat if i in possible_drugs]
                    try:
                        out.append(flat2[0])
                    except:
                        out.append(None)
                else:
                    flat = [i for j in y3 for i in j]
                    out.append(flat[0])

        return out

    def run_linking(self, data, drugdf, possible_drugs=None, restricted=False):

        #aggdrugdf = drugdf.groupby('thread_id').agg(list)

        #aggdrugdf = aggdrugdf.reset_index()
        #         init_out = initialize_UNK(data)

        out1 = self.first_drug(data, drugdf, possible_drugs=possible_drugs, restricted=restricted)
        out2, dist = self.nearest_drug_samepost(data, drugdf, possible_drugs=possible_drugs,
                                                restricted=restricted, only_before=True)

        out2b, dist2b = self.nearest_drug_samepost(data, drugdf, possible_drugs=possible_drugs,
                                                   restricted=restricted, only_before=False)

        out3 = []

        for a, b, c, d in zip(out1, out2, out2b, dist):
            if b != None:  # and c <= v:
                out3.append(b)
            elif c != None:
                out3.append(c)
            else:
                out3.append(a)

        return out3


    def main(self, df, restricted=False, possible_drugs=None):
        # words = df.message)
        # threadix = df.thread_id
        # ix = df.post_id
        drugdf = self.extract_drug_data(df)
        # print(drugdf)
        out = self.run_linking(df, drugdf, possible_drugs, restricted)
        # print(out)

        nwdf = pd.concat([df, pd.Series(out, name='linked_drug')], axis=1)

        return nwdf