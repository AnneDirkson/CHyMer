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

class

    def adjust_col (row):
    return row[0]

df3['thread_id'] = df3.thread_id.apply(lambda x: adjust_col(x))
drugdf['thread_id'] = drugdf.thread_id.apply(lambda x: adjust_col(x))


outb = DrugLinker().main(df3, drugdf, restricted = True, possible_drugs = restricted_list)

