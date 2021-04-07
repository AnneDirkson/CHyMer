##This is the main script of CHyMER
#
# Author: Anne Dirkson
# Date: 6 April 2021
#
# This script imports the methods to extract and normalize ADR; as well as those to link them to the most likely medication.
# Here data is reformatted for each step and additional attributes are added

from NormalizeADR import ADRNormalizer
from ExtractADR import
from DrugLinker import DrugLinker

class RunPipeline():

    def __init__(self):
        with open('data/default_names_dict.json', 'r') as fp:
            self.default_names = json.load(fp)

        with open('data/lvl_up_dict.json', 'r') as fp:
            self.lvl_up_dict = json.load(fp)

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

    def adjust_col (row):
        return row[0]

    def main(self):
        df2 = self.get_messages_of_ADR(self, df, orig_data)

df3['thread_id'] = df3.thread_id.apply(lambda x: adjust_col(x))
drugdf['thread_id'] = drugdf.thread_id.apply(lambda x: adjust_col(x))


outb = DrugLinker().main(df3, drugdf, restricted = True, possible_drugs = restricted_list)

##output is a new df with normalized cui and names
NormalizedResults = ADRNormalizer().main(input_dir, output_dir, model_dir, dictionary_path)

##syn_cui_text is the original synonym the term was linked to
DefaultName = []
LvlUpCUI = []
LvlUpName = []

for a in NormalizedResults.cui:
     DefaultName.append(self.default_names[a])
     LvlUpCUI.append(self.lvl_up_dict[a])
for b in LvlUpCUI:
    LvlUpName.append(self.default_names[b])

NormalizedResults2 = pd.concat([NormalizedResults, pd.Series(DefaultName, name='cui_txt'), pd.Series(LvlUpCUI, name = 'lvl_up_cui'), pd.Series(LvlUpName, name= 'lvl_up_name')], axis=1)


##add messages






