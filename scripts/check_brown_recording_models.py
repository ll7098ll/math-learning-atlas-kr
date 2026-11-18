"""Exact own examples for graph baselines, units and nested case records."""
from fractions import Fraction as F
import json

def check():
 all_participants=set(range(37));cases=set(range(6));two=set([1,9])
 assert len(all_participants|cases|two)==37 and 37+6+2==45
 possible=[]
 for overlap in range(3):
  transcripts=set(range(overlap))|set(range(6,8-overlap))
  assert len(transcripts)==2
  possible.append(len(cases|transcripts))
 assert possible==[8,7,6]
 # A proportion can rise while the number of coded instances falls.
 assert F(20,100)<F(15,50) and 20>15
 # Bar lengths above a cropped baseline have a different ratio from values.
 assert F(72,36)==2 and F(72-12,36-12)==F(5,2)
 # Equal products preserve the total, not the roles or required resources.
 assert 3*20==20*3==60 and 3!=20
 # Initial recording selection and subsequent transcription selection differ.
 assert F(10,40)*F(4,10)==F(4,40)==F(1,10)
 assert F(4,4)==1 and F(4,40)!=1
 return dict(status='pass',participant_union=37,case_transcript_union_bounds=[6,8],proportions=['1/5','3/10'],values_ratio=2,cropped_bar_length_ratio='5/2',same_total=60,selected_record_fraction='1/10',student_data=False,authors_dataset_reconstructed=False,scope='Exact own counterexamples only;source bar heights are not digitized and local learning/transfer are not validated.')

if __name__=='__main__':print(json.dumps(check()))
