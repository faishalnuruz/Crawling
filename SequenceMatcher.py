import difflib
from difflib import SequenceMatcher
from functools import partial
import pandas as pd

def apply_sm(Fb): 
    return difflib.SequenceMatcher(None, Fb['Kota'], Fb['Nama']).ratio()

df111 = pd.DataFrame({'A': {1: 'One'}, 'B': {1: 'Two'}})
df111.apply(partial(apply_sm, Fb['Kota']='A', Fb['Nama']='B'), axis=1)


def similar(Cr,Fb):
return SequenceMatcher(None, Cr,Fb).ratio()
    
seq = difflib.SequenceMatcher(None, Cr,Fb)
d=seq.ratio()*100

m = SequenceMatcher(None, Cr,Fb)
m.ratio()

import distance

jd = lambda x, y: 1 - distance.jaccard(x, y)

test_df = pd.concat([Cr.iloc[:, 2] for Cr in [Fb, Cr]], axis=1, keys=['one', 'two'])
oke = test_df.apply(lambda x: jd(x[0], x[1]), axis=1)

test_df = pd.concat([Cr.iloc[:, 3] for Cr in [Fb, Cr]], axis=1, keys=['one', 'two'])
oke1 = test_df.apply(lambda x: jd(x[0], x[1]), axis=1)

oke2 = pd.concat([oke, oke1], axis=1)

jd = lambda x, y: 1 - distance.jaccard(x, y)
go = Cr.head().iloc[:, 0].apply(lambda x: Fb.head().iloc[:, 0].apply(lambda y: jd(x, y)))



def similar(Cr):
    x = SequenceMatcher(None, Cr['Kota'], Cr['Nama']).ratio()
    score = x*100
    results = round(score, 2)
    return results
    
 dataframe['result'] = dataframe.apply(lambda Cr: similar(), axis=1)