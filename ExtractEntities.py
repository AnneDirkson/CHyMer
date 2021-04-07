#!/usr/bin/env python
# coding: utf-8

# In[8]:


from collections import defaultdict


# In[ ]:





# In[170]:


class EntityExtractor(): 
    
    def __init__(self): 
        pass
    
    ### use methods to extract concepts and add to df

    def extract_adr_words(self, sent, tags):
        adr_tags = []
        adr_words = []
        ent_range = []
        dist = defaultdict(list)
        tempwords = []
        temprange = []
        temptags = [] 

        for num, a in enumerate(tags):
            # print(a)
            try: 
                word = sent[num]
            except IndexError: 
                print('Tags and sent are not equal')
                print(len(s))
                print(len(t))


            if a.endswith('ADR'):
                if a.startswith('B'):
                    if len(temptags) != 0:
                        adr_tags.append(temptags)
                        adr_words.append(tempwords)
                        ent_range.append(temprange)


                    tempwords= []
                    temptags = []
                    temprange = []

                    tempwords.append(word)
                    temptags.append(a)
                    temprange.append(num)

                    dist['start_ent'].append(num)
#                     try:

#                         if tags[num+1].startswith('HI') and a.startswith('DB'):
#                             dist['end_ent'].append(num)
#                         elif tags[num+1].startswith('I') or tags[num+1].startswith('HI'):
#                             pass
#                         else:
                    dist['end_ent'].append(num)

#                     except IndexError:
#                         dist['end_ent'].append(num)
                elif a.startswith('I'):
                    tempwords.append(word)
                    temprange.append(num)
                    temptags.append(a)

                    try:
                        dist['end_ent'][-1] == num
                    except IndexError:
                        break
            else:
                pass
        adr_words.append(tempwords)
        adr_tags.append(temptags)
        ent_range.append(temprange)
        try: 
            if num not in dist['sent_end']: 
                dist['sent_end'].append(num)
        except: 
            print(sent)

        return adr_tags, adr_words, dist, ent_range

    def main(self, nwermsgs, nwtags3): 
        all_adr = []
        all_tgs = []
        all_ix = []
        all_ent_ranges= []

        for s,t in zip(nwermsgs, nwtags3): 

            outtgs, outwords, ix, ent_range = self.extract_adr_words(s,t)

            outwords3 = [i for i in outwords if i != []]
            outtgs3 = [i for i in outtgs if i != []]

            all_adr.append(outwords3)
            all_tgs.append(outtgs3)
            all_ix.append(ix)
            all_ent_ranges.append(ent_range)
        return all_adr, all_tgs, all_ix, all_ent_ranges
  


# In[ ]:


##At some point need to make a generic one for any label


# In[ ]:


class EntityExtractorSTR(): 
    
    def __init__(self): 
        pass
    
    ### use methods to extract concepts and add to df

    def extract_adr_words(self, sent, tags):
        adr_tags = []
        adr_words = []
        ent_range = []
        dist = defaultdict(list)
        tempwords = []
        temprange = []
        temptags = [] 

        for num, a in enumerate(tags): 
            try: 
                word = sent[num]
            except IndexError: 
                print('Tags and sent are not equal')
                print(len(s))
                print(len(t))
            if word == '.': 
                dist['sent_end'].append(num)
            else: 
                if a.endswith('STR'): 
                    if a.startswith('B') or a.startswith('DB') or a.startswith('HB'): 
                        if len(temptags) != 0: 
                            adr_tags.append(temptags)
                            adr_words.append(tempwords)
                            ent_range.append(temprange)


                        tempwords= []
                        temptags = []
                        temprange = []

                        tempwords.append(word)
                        temptags.append(a)
                        temprange.append(num)

                        dist['start_ent'].append(num)
    #                     try: 

    #                         if tags[num+1].startswith('HI') and a.startswith('DB'): 
    #                             dist['end_ent'].append(num)
    #                         elif tags[num+1].startswith('I') or tags[num+1].startswith('HI'): 
    #                             pass
    #                         else: 
                        dist['end_ent'].append(num)

    #                     except IndexError: 
    #                         dist['end_ent'].append(num)
                    elif a.startswith('I') or a.startswith('DI'): 
                        tempwords.append(word)
                        temprange.append(num)
                        temptags.append(a)

                        try: 
                            dist['end_ent'][-1] == num
                        except IndexError: 
                            break

                    elif a.startswith('HI'): ##can have DB in between 
                        if tags[num-1] != 'HB-STR': ##it is loose and could be sandwiched (or it just a second HI)

                            if tags[num-1] == 'HI-STR': ##it is OK
                                tempwords.append(word)
                                temptags.append(a)
                                temprange.append(num)
                                try: 
                                    dist['end_ent'][-1] == num
                                except IndexError: 
                                    break
                            else: ##it is sandwiched - start new entity - previous is not HB-STR or HI-STR

                                if len(temptags) != 0: 
                                    adr_tags.append(temptags)
                                    adr_words.append(tempwords)
                                    ent_range.append(temprange)

                                tempwords= []
                                temptags = []
                                temprange = []

                                tempwords.append(word)
                                temptags.append(a)
                                temprange.append(num)
                                dist['start_ent'].append(num)
    #                             if tags[num+1] != a: 
                                dist['end_ent'].append(num)

                        else: 
                            tempwords.append(word)
                            temptags.append(a)
                            temprange.append(num)
    #                         try: 
    #                             if tags[num+1]!= a: 
    #                                  dist['end_ent'].append(num)
    #                         except IndexError: 
                            dist['end_ent'][-1] == num
                else: 
                    pass
        adr_words.append(tempwords)
        adr_tags.append(temptags)
        ent_range.append(temprange)
        try: 
            if num not in dist['sent_end']: 
                dist['sent_end'].append(num)
        except: 
            print(tags)

        return adr_tags, adr_words, dist, ent_range
    
    def sent_end_inbetween(self, start1, end1, start2, end2, sent_ends): 
        p = 0
        for num, end in enumerate(sent_ends): 
    #         print(end)
            if num == 0 : 
                q = 0 
            else: 
                q = sent_ends[num-1]
            if q < start1 < end and q < end2 < end: 
                p = 1
                return True

            elif q < start2 < end and q < end1 < end: 
                p = 1
                return True

        if p== 0: 
            return False
       
    def overlap_correction(self,adrlst, tagslst, ixlst, ent_range, s): 
        flat = [i for j in tagslst for i in j]
        if 'HB-STR' in flat: 
            nwadrlst =  [[] for _ in range(len(adrlst))]
            nwtagslst = [[] for _ in range(len(adrlst))]
            
            nwentrange =  [[] for _ in range(len(adrlst))]

            nwixlst = defaultdict(list)
            nwixlst['start_ent'] = [[]] * len(adrlst)
            nwixlst['end_ent'] =[[]] * len(adrlst)
            nwixlst['sent_end'] = ixlst['sent_end'] ##does not change
    #         print(nwixlst)
            for num, i in enumerate(tagslst): 
                y = adrlst[num]
                w = ent_range[num]
    #             print(y)
                start = ixlst['start_ent'][num]
                try: 
                    end = ixlst['end_ent'][num]
                except: 
                    print(ixlst)
                    print(adrlst)

                if i[0] == 'HB-STR' or i[0] == 'HI-STR': 
    #                 print('Yes')
                    cnt = 0
                    to_change = []
                    for x in [-1, -2, -3,-4]: ##check 4 to left 
                        try: 
    #                         print(num+x)
                            if num+x >= 0: 
    #                             print(num+x)
                                if tagslst[num+x][0] != 'DB-STR': 
                                    break

                                else:

                                    cnt +=1 
                                    to_change.append(num+x)
                        except IndexError: 
                            pass
    #                 print(to_change)    
                    for x in [1,2,3,4]: ##try right side
                        try: 
                            if tagslst[num+x][0] != 'DB-STR':
                                break
                            else: 
                                cnt +=1 
                                to_change.append(num+x)
                        except IndexError: 
                            pass
    #                 print(cnt)
                    if 1 < cnt < 3: ##good
    #                     print(to_change)
                        for z in to_change: 


                            nwadrlst[z].extend(y)
                            nwtagslst[z].extend(i)
                            nwentrange[z].extend(w)

                        ##possibly change start or end
                            if start < ixlst['start_ent'][z]: ##start entity earlier
                                nwixlst['start_ent'][z] = start
                            elif end > ixlst['end_ent'][z]: ## end later
                                nwixlst['end_ent'][z] = end

                    else: ##use the sentence endings if more than 3
#                         print('Using sentence endings')
                        cnt = 0
                        orig_change = to_change
                        to_change = []
                        for x in [-1, -2, -3,-4]: ##check 4 to left 
                            try: 
        #                         print(num+x)
                                if num+x >= 0: 
        #                             print(num+x)
                                    if tagslst[num+x][0] != 'DB-STR': 
                                        break
        #                             if tagslst[num+x][0] == 'DB-STR':
                                    else:
        #                                 print(num+x)
                                        start2 = ixlst['start_ent'][num+x]
                                        end2 = ixlst['end_ent'][num+x]
                                        if self.sent_end_inbetween(start, end, start2, end2, ixlst['sent_end']): ##fulfills both conditions
                                            cnt +=1 
                                            to_change.append(num+x)
                            except IndexError: 
                                pass
        #                 print(to_change)    
                        for x in [1,2,3,4]: ##try right side
                            try: 
                                if tagslst[num+x][0] != 'DB-STR':
                                    break
                                else: 
        #                                 print(num+x)
                                    start2 = ixlst['start_ent'][num+x]
                                    end2 = ixlst['end_ent'][num+x]
                                    if self.sent_end_inbetween(start, end, start2, end2, ixlst['sent_end']): ##fulfills both conditions
                                        cnt +=1 
                                        to_change.append(num+x)
                            except IndexError: 
                                pass
        #                 print(cnt)
                        if 1 < cnt < 5: ##good
    #                         print(cnt)
                            for z in to_change: 


                                nwadrlst[z].extend(y)
                                nwtagslst[z].extend(i)
                                nwentrange[z].extend(w)

                            ##possibly change start or end
                                if start < ixlst['start_ent'][z]: ##start entity earlier
                                    nwixlst['start_ent'][z] = start
                                elif end > ixlst['end_ent'][z]: ## end later
                                    nwixlst['end_ent'][z] = end
                        elif cnt < 2: 
                            for z in orig_change: 
                                nwadrlst[z].extend(y)
                                nwtagslst[z].extend(i)
                                nwentrange[z].extend(w)

                            ##possibly change start or end
                                if start < ixlst['start_ent'][z]: ##start entity earlier
                                    nwixlst['start_ent'][z] = start
                                elif end > ixlst['end_ent'][z]: ## end later
                                    nwixlst['end_ent'][z] = end

#                         elif cnt == 5: 
                              
#                             for z in to_change: 

#                                 nwadrlst[z].extend(y)
#                                 nwtagslst[z].extend(i)
#                                 nwentrange[z].extend(w)

#                             ##possibly change start or end
#                                 if start < ixlst['start_ent'][z]: ##start entity earlier
#                                     nwixlst['start_ent'][z] = start
#                                 elif end > ixlst['end_ent'][z]: ## end later
#                                     nwixlst['end_ent'][z] = end
                        else: ##only use one side with shortest distance
                            
            
                            dist_left = (ixlst['start_ent'][num]) - (ixlst['end_ent'][num-1])
            
                            dist_right = (ixlst['start_ent'][num+1]) - (ixlst['end_ent'][num])
                            
                
                            if dist_left < dist_right: ##smaller dist wins
                                print('Left wins')
                                to_change2 = [i for i in to_change if i < num]
                            
                            else: 
                                to_change2 = [i for i in to_change if i > num]
                                
                            for z in to_change2: 


                                nwadrlst[z].extend(y)
                                nwtagslst[z].extend(i)
                                nwentrange[z].extend(w)

                            ##possibly change start or end
                                if start < ixlst['start_ent'][z]: ##start entity earlier
                                    nwixlst['start_ent'][z] = start
                                elif end > ixlst['end_ent'][z]: ## end later
                                    nwixlst['end_ent'][z] = end
        
#                             print(num)
#                             print(cnt)
#                             print(to_change)
#                             print('Not good!')
#                             print(adrlst)
#                             print(tagslst)
#                             print(ixlst)
#                             print(s)
#                             print(ent_range)

                elif i[0] == 'HI-STR': ##loose end
                    print('Happening')
                    if 1 < cnt < 5: ##good
    #                     print(to_change)
                        for z in to_change: 

                            nwentrange[z].extend(w)
                            nwadrlst[z].extend(y)
                            nwtagslst[z].extend(i)

                        ##possibly change start or end
                            if start < ixlst['start_ent'][z]: ##start entity earlier
                                nwixlst['start_ent'][z] = start
                            elif end > ixlst['end_ent'][z]: ## end later
                                nwixlst['end_ent'][z] = end

                elif i[0] == 'DB-STR':  

                    try: 
                        if nwixlst['start_ent'][num] > 0 :  ## start entity already taken
                            pass
                        else: 
                            nwixlst['start_ent'][num] = start
                    except TypeError: 
                        nwixlst['start_ent'][num] = start

                    nwixlst['end_ent'][num]=end

                    nwadrlst[num].extend(y)
                    nwtagslst[num].extend(i)
                    nwentrange[num].extend(w)

                else: 
                    nwentrange[num].extend(w)
                    nwtagslst[num]= i
                    nwadrlst[num] = y
                    nwixlst['end_ent'][num]=end
                    nwixlst['start_ent'][num]=start

            return nwadrlst, nwtagslst, nwixlst, nwentrange           
        else: 
            return adrlst, tagslst, ixlst, ent_range
                
        ##run on all and check for HI starts -- need to glue to previous HB and need to remove from start and end ent
        
    def main(self, nwermsgs, nwtags3): 
        all_adr = []
        all_tgs = []
        all_ix = []
        all_ent_ranges= []

        for s,t in zip(nwermsgs, nwtags3): 

            outtgs, outwords, ix, ent_range = self.extract_adr_words(s,t) 

            outwords2, outtgs2, ix2, ent_range2 = self.overlap_correction(outwords, outtgs, ix, ent_range, s)

            outwords3 = [i for i in outwords2 if i != []]
            outtgs3 = [i for i in outtgs2 if i != []]

            all_adr.append(outwords3)
            all_tgs.append(outtgs3)
            all_ix.append(ix2)
            all_ent_ranges.append(ent_range2)
        return all_adr, all_tgs, all_ix, all_ent_ranges
  


# In[171]:


# import pickle 

# def load_obj(name):
#     with open(name + '.pkl', 'rb') as f:
#         return pickle.load(f, encoding='latin1')
    

# def save_obj(obj, name):
#     with open(name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        
# import pandas as pd


# In[185]:


##get input 
##Get data 

# data = load_obj('/data/dirksonar/Project4_entityextract/NER_Corpus_ADR_nw_withID')

# data = load_obj('C:\\Users\\dirksonar\\Documents\\Data\\Project4_entityextract\\Annotated data\\GISTdata\\Output\\Annotators/Corpus/NER_Corpus_Coping')
# data = load_obj('C:\\Users\\dirksonar\\Documents\\Data\\Project4_entityextract\\Annotated data\\GISTdata\\Output\\Annotators/Corpus/NER_Corpus_ADR_nw_withID')
# 


# In[186]:


# data.head()


# In[187]:


# datagroup = data.groupby('sent_id').agg(list)


# In[188]:


# datagroup.head(100)


# In[196]:


# for num, i in enumerate(datagroup.tag): 
#     if len(set(i)) == 1: 
#         pass
#     else: 
#         print(num)


# In[189]:


# sents = datagroup.word
# tgs = datagroup.tag


# In[177]:


# tgs.iloc[15]


# In[197]:


# adr_tags, adr_words, dist, ent_range = EntityExtractor().extract_adr_words(sents.iloc[6], tgs.iloc[6])


# In[198]:


# adr_words


# In[199]:


# ent_range


# In[182]:


# nwadrlst, nwtagslst, nwixlst, nwentrange = EntityExtractor().overlap_correction(adr_words, adr_tags, ix, entrange, msg)


# In[183]:


# nwadrlst


# In[168]:


# nwentrange


# In[169]:


# nwtagslst


# In[54]:


# nwadrlst


# In[62]:


##usage 

# adr_tags, adr_words, dist, ent_range = EntityExtractor().main(sents, tgs)


# In[65]:


# ent_range


# In[ ]:




