##This is the script for normalizing ADR which is largely based on the BioSyn method
# by Sung et al. I (A.R. Dirkson) adapted the composite splitting script to allow for
# splitting in unlabelled data + reconfigured the input data and input targets.
# I have switched off the abbreviation expansion in the biosyn module as it has already been
# done during pre-processing. I have also set lower case; remove punc and split composites
# to True.

from biosyn.query_preprocess_inference import QueryPreprocess
from biosyn.eval import RunNormalizer
import pandas as pd
from collections import defaultdict

class ADRNormalizer():

    def __init__(self):
        pass

    def remove_UNK(self, df):
        normalized_txt = []
        removed = ['/', '-', "'", '&', '(', '\\', ',', '%', '[UNK]']
        for i in df.ent:
            i2 = i.split(" ")
            i3 = [x for x in i2 if x not in removed]
            i4 = " ".join(i3)

            normalized_txt.append(i4)
        return normalized_txt

    def reformat_data_fornorm(self, texts, output_dir):
        x = [-1] * len(texts)
    #     x2 = [-1)+ '|'+ str(-1)] * len(texts)
        x2 = [''] * len(texts)

        df = pd.concat([pd.Series(x), pd.Series(x2), pd.Series(x), pd.Series(x), pd.Series(x2), pd.Series(x), pd.Series(x2), pd.Series(texts), pd.Series(x2), pd.Series(x)], axis=1)

        df.to_csv(output_dir + 'entities.concept', sep = '|', header = None, index = False)

    ##adapt the original entities file
    def create_dict_composite (self, df): ##df is the file with the found entities
        dict_composite = defaultdict(list)
        for a,b in zip(df.ent, df.post_id):
            dict_composite[b].append(a)
        return dict_composite

    def adapt_out_to_composite(self, out2, dict_composite):
        nw_thread_id = []
        nw_postid = []
        nw_ent_start = []
        nw_ent_end = []
        nw_ent = []

        for key in dict_composite:
            val = dict_composite[key]

            df = out2[out2.post_id == key]

            if len(df) == len(val):  ##no composites
                nw_thread_id.extend(df.thread_id)
                nw_postid.extend(df.post_id)
                nw_ent_start.extend(df.ent_start)
                nw_ent_end.extend(df.ent_end)
                nw_ent.extend([" ".join(x) for x in list(df.ent)])

            else:  ##there are composites
                print(val)
                print(df)
                ##loop through the entities found with splitting
                x = 0
                for num, e in enumerate(val):
                    #                 x = 0
                    e_sp = e.split(" ")
                    print(num)

                    if len(df) == 1:  ##it is just this one
                        num = 0
                        nw_thread_id.append(df.thread_id.iloc[num])
                        nw_postid.append(df.post_id.iloc[num])
                        nw_ent_start.append(df.ent_start.iloc[num])
                        nw_ent_end.append(df.ent_end.iloc[num])

                        nw_ent.append(e)
                    else:

                        try:
                            if df.ent.iloc[num - x] == e or e_sp[0] == df.ent.iloc[num - x][0]:  ##same
                                nw_thread_id.append(df.thread_id.iloc[num - x])
                                nw_postid.append(df.post_id.iloc[num - x])
                                nw_ent_start.append(df.ent_start.iloc[num - x])
                                nw_ent_end.append(df.ent_end.iloc[num - x])

                                nw_ent.append(e)


                            else:  ##not the case - likely end of entity
                                print(e_sp)
                                #                         print(x)
                                print(df.ent.iloc[num - 1 - x])
                                if df.ent.iloc[num - 1 - x][-1] == e_sp[-1]:
                                    nw_thread_id.append(df.thread_id.iloc[num - 1 - x])
                                    nw_postid.append(df.post_id.iloc[num - 1 - x])
                                    nw_ent_start.append(df.ent_start.iloc[num - 1 - x])
                                    nw_ent_end.append(df.ent_end.iloc[num - 1 - x])
                                    nw_ent.append(e)
                                    x += 1
                                else:
                                    print('PROBLEM')
                                    print(val)
                                    print(df)
                        except:
                            print(e_sp)
                            #                         print(x)
                            print(df.ent.iloc[num - 1 - x])
                            if df.ent.iloc[num - 1 - x][-1] == e_sp[-1]:
                                nw_thread_id.append(df.thread_id.iloc[num - 1 - x])
                                nw_postid.append(df.post_id.iloc[num - 1 - x])
                                nw_ent_start.append(df.ent_start.iloc[num - 1 - x])
                                nw_ent_end.append(df.ent_end.iloc[num - 1 - x])
                                nw_ent.append(e)
                                x += 1
                            else:
                                print('PROBLEM')
                                print(val)
                                print(df)

        nwdf = pd.concat([pd.Series(nw_thread_id, name='thread_id'), pd.Series(nw_postid, name='post_id'),
                          pd.Series(nw_ent_start, name='ent_start'), pd.Series(nw_ent_end, name='ent_end'),
                          pd.Series(nw_ent, name='ent')], axis=1)

        return nwdf


    def link2ADR(self, results, df):
        d = results['queries']
        df2 = self.adapt_out_to_composite(df, dict_composite)

        out_dict = {}
        out_dict_name = {}
        for i in d:
            j = i['mentions']

            for y in j:
                n = y['candidates'][0]['cui']
                n2 = y['candidates'][0]['name']
                m = y['mention']
                out_dict[m] = n
                out_dict_name[m] = n2
        ##use these dictionaries to normalize the entities
        normalized_txt = []
        normalized_cui = []
        for k, i in zip(df2.post_id, df2.ent):
            normalized_cui.append(out_dict[i4])
            normalized_txt.append(out_dict_name[i4])

        df3 = pd.concat([df2, pd.Series(normalized_cui, name='cui'), pd.Series(normalized_txt, name='syn_cui_text')], axis=1)
        return df3

    def main(self, df, output_dir1, output_dir2, model_dir, dictionary_path, use_cuda):

        normalized_text = self.remove_UNK(df)
        self.reformat_data_fornorm(normalized_text, output_dir1)
        input_dir = output_dir1
        QueryPreprocess().main(input_dir, output_dir2)
        data_dir = output_dir2
        results = RunNormalizer().main(model_dir, dictionary_path, data_dir, use_cuda, topk = 10)
        ##link normalization to original df with entities

        df = df.drop(['ent'])
        df1 = pd.concat([df, pd.Series(normalized_text, name= 'ent')], axis=1)
        df2 = self.link2ADR(self, results, df1)

        ## remove doubles per message
        df3 = df2.drop_duplicates(subset=['post_id', 'cui'], keep='first')

        return df3