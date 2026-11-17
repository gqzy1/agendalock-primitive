"""Offline ordinal/Kemeny certificate verification without importing contract code."""
import hashlib
import itertools
import json
import sys

def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def verify(r):
    data,accepted,proof=r['input'],r['accepted'],r['proof'];n=len(data['topics']);members=data['members']
    assert r['input_hash']==sha({'version':'agendalock-1','input':data})
    assert set(r['statements'])==set(members)
    assert r['ballot_hash']==sha({'input_hash':r['input_hash'],'statements':r['statements']})
    assert r['ranking_hash']==sha({'version':'agendalock-1','id':r['id'],'ballot_hash':r['ballot_hash'],'accepted':accepted,'proof':proof})
    assert len(accepted['ballots'])==len(members)
    unknown=[];orders=[]
    for i,b in enumerate(accepted['ballots']):
        if b['status']=='UNKNOWN':
            unknown.append(i);assert b['order']==[] and b['quote']=='';continue
        assert b['status']=='KNOWN' and sorted(b['order'])==list(range(n))
        assert b['quote'] == r['statements'][members[i]];orders.append(b['order'])
    if unknown:
        assert proof=={'status':'REVIEW','unknown_members':unknown};assert r['state'] in ['REVIEW','CANCELLED'];return
    assert proof['status']=='READY'
    pairwise=[[sum(o.index(a)<o.index(b) for o in orders) for b in range(n)] for a in range(n)]
    assert proof['pairwise_support']==pairwise
    candidates=[]
    for order in itertools.permutations(range(n)):
        # Direct inversion count independently computes the objective, without using support sums.
        score=sum(o.index(order[i])>o.index(order[j]) for o in orders for i in range(n) for j in range(i+1,n))
        candidates.append({'order':list(order),'disagreements':score})
    best=min(c['disagreements'] for c in candidates);optimal=[c['order'] for c in candidates if c['disagreements']==best]
    assert proof['candidates']==candidates and proof['minimum_disagreements']==best and proof['optimal_orders']==optimal and proof['chosen']==optimal[0]
    chosen=optimal[0]
    objections=[{'before':chosen[i],'after':chosen[j],'opposing_members':[k for k,o in enumerate(orders) if o.index(chosen[j])<o.index(chosen[i])]} for i in range(n) for j in range(i+1,n)]
    assert proof['objections']==objections
    cycles=[[a,b,c,a] for a in range(n) for b in range(a+1,n) for c in range(a+1,n) if b!=c and pairwise[a][b]>pairwise[b][a] and pairwise[b][c]>pairwise[c][b] and pairwise[c][a]>pairwise[a][c]]
    assert proof['majority_triangles']==cycles
    assert r['completed']==chosen[:r['cursor']]
    if r['state']=='CLOSED':assert r['cursor']==n
    elif r['state']=='RUNNING':assert 0<=r['cursor']<n
    else:assert r['state'] in ['READY','CANCELLED'] and r['cursor']==0

if __name__=='__main__':
    records=json.load(open(sys.argv[1]))
    for record in records.values():verify(record)
    print('Independent ballot, all-candidate optimum, cycle, execution-prefix and commitment verification passed for',len(records),'agendas.')
