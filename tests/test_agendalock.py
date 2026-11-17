import itertools
import json
import random
import unittest
from host import c,host,Return,A,B,C,D

def data():return {'title':'Operations agenda','topics':['Logistics','Branding','Safety'],'members':[A,B]}
S1='Safety is my first priority, Logistics is second, and Branding is last.'
S2='I rank Safety highest, then Logistics, then Branding.'
def output(orders=None,statements=None):
    return {'ballots':[{'status':'KNOWN','order':order,'quote':s} for order,s in zip(orders or [[2,0,1],[2,0,1]],statements or [S1,S2])]}
def fresh():
    host.queue=[];host.calls=0;host.message.sender_address=A;o=c.AgendaLock();o.agendas={};o.owners={};return o

def sealed(o):
    key=o.open_agenda('sample',json.dumps(data()));o.submit(key,0,S1);host.message.sender_address=B;o.submit(key,1,S2);host.message.sender_address=A;o.freeze(key,2);return key

def ranked(o,value=None):
    host.queue=[json.dumps(value or output()),json.dumps(value or output())];return json.loads(o.rank(A+':sample',3))

class AgendaTests(unittest.TestCase):
    def test_signed_ballots_closed_lifecycle(self):
        o=fresh();key=sealed(o);r=ranked(o);self.assertEqual(r['proof']['chosen'],[2,0,1]);self.assertEqual(r['proof']['minimum_disagreements'],0)
        self.assertEqual(host.calls,2);r=json.loads(o.start(key,4,r['ranking_hash']))
        for revision,topic in enumerate([2,0,1],5):r=json.loads(o.advance(key,revision,topic))
        self.assertEqual(r['state'],'CLOSED');self.assertEqual(r['completed'],[2,0,1]);self.assertEqual(r['cursor'],3)
        with self.assertRaisesRegex(Exception,'NOT_RUNNING'):o.advance(key,8,1)
        self.assertEqual(json.loads(o.list_agendas(A)),[key])

    def test_missing_ballot_and_member_authentication(self):
        o=fresh();key=o.open_agenda('sample',json.dumps(data()));before=o.get_agenda(key)
        with self.assertRaisesRegex(Exception,'MISSING_BALLOT'):o.freeze(key,0)
        self.assertEqual(o.get_agenda(key),before);host.message.sender_address=C
        with self.assertRaisesRegex(Exception,'MEMBER_ONLY'):o.submit(key,0,S1)
        host.message.sender_address=B
        with self.assertRaisesRegex(Exception,'MODERATOR_ONLY'):o.freeze(key,0)

    def test_immutable_ballot_and_idempotent_retry(self):
        o=fresh();key=o.open_agenda('sample',json.dumps(data()));r=o.submit(key,0,S1);self.assertEqual(o.submit(key,1,S1),r)
        with self.assertRaisesRegex(Exception,'BALLOT_IMMUTABLE'):o.submit(key,1,S2)
        self.assertEqual(o.get_agenda(key),r)

    def test_rank_failures_leave_sealed(self):
        for mode in ['disagree','unknown_disagree','bad_json','model_error']:
            o=fresh();key=sealed(o);before=o.get_agenda(key);other=output()
            if mode=='disagree':other['ballots'][1]['order']=[0,2,1]
            if mode=='unknown_disagree':other['ballots'][0]={'status':'UNKNOWN','order':[],'quote':''}
            host.queue=[json.dumps(output()),'bad' if mode=='bad_json' else RuntimeError('model down') if mode=='model_error' else json.dumps(other)]
            with self.assertRaises(Exception):o.rank(key,3)
            self.assertEqual(o.get_agenda(key),before)

    def test_review_and_cancel_cannot_start(self):
        o=fresh();key=sealed(o);v=output();v['ballots'][1]={'status':'UNKNOWN','order':[],'quote':''};r=ranked(o,v)
        self.assertEqual(r['state'],'REVIEW')
        with self.assertRaisesRegex(Exception,'NOT_READY'):o.start(key,4,r['ranking_hash'])
        host.message.sender_address=B;r=json.loads(o.cancel(key,4));self.assertEqual(r['state'],'CANCELLED')
        with self.assertRaises(Exception):o.rank(key,5)

    def test_running_order_hash_revision_and_permissions(self):
        o=fresh();key=sealed(o);r=ranked(o);before=o.get_agenda(key)
        for revision,h in [(3,r['ranking_hash']),(4,'wrong')]:
            with self.assertRaises(Exception):o.start(key,revision,h)
            self.assertEqual(o.get_agenda(key),before)
        o.start(key,4,r['ranking_hash']);before=o.get_agenda(key)
        for topic in [0,True]:
            with self.assertRaisesRegex(Exception,'WRONG_NEXT_TOPIC'):o.advance(key,5,topic)
            self.assertEqual(o.get_agenda(key),before)
        host.message.sender_address=B
        with self.assertRaisesRegex(Exception,'MODERATOR_ONLY'):o.advance(key,5,2)
        with self.assertRaisesRegex(Exception,'CANNOT_CANCEL'):o.cancel(key,5)

    def test_rank_schema_and_own_quote_grounding(self):
        d=data()|{'statements':[S1,S2]}
        for mutate in [lambda v:v['ballots'][0].update(order=[True,0,1]),lambda v:v['ballots'][0].update(order=[2,2,1]),
                       lambda v:v['ballots'][0].update(quote=S2),lambda v:v['ballots'][0].update(order=[2,0]),lambda v:v.update(extra=True)]:
            v=output();mutate(v)
            with self.assertRaises(Exception):c.interpretation(v,d)
        with self.assertRaises(Exception):c.decode('{"ballots":[],"ballots":[]}')
        self.assertFalse(c.agrees(Exception(),lambda:output(),d))

    def test_input_and_namespace_limits(self):
        for mutate in [lambda d:d.update(topics=['A','a']),lambda d:d.update(members=[A,A]),lambda d:d.update(topics=['A']),
                       lambda d:d.update(members=[A,'0x'+'0'*40]),lambda d:d.update(extra=1)]:
            d=data();mutate(d)
            with self.assertRaises(Exception):c.specification(json.dumps(d))
        o=fresh();key=o.open_agenda('sample',json.dumps(data()));self.assertEqual(key,o.open_agenda('sample',json.dumps(data())))
        d=data();d['title']='Other agenda'
        with self.assertRaisesRegex(Exception,'ID_CONFLICT'):o.open_agenda('sample',json.dumps(d))
        for i in range(23):o.open_agenda('tag-'+str(i),json.dumps(d))
        with self.assertRaisesRegex(Exception,'OWNER_LIMIT'):o.open_agenda('too-many',json.dumps(d))

    def test_cancelled_collection_is_terminal(self):
        o=fresh();key=o.open_agenda('sample',json.dumps(data()));host.message.sender_address=B;o.cancel(key,0)
        for method,args in [(o.submit,(key,1,S2)),(o.freeze,(key,1)),(o.cancel,(key,1))]:
            with self.assertRaises(Exception):method(*args)

    def test_condorcet_cycle_and_all_optima(self):
        d={'topics':['A','B','C']};v={'ballots':[{'status':'KNOWN','order':o} for o in [[0,1,2],[1,2,0],[2,0,1]]]}
        proof=c.derive(d,v);self.assertEqual(proof['minimum_disagreements'],4)
        self.assertEqual(proof['optimal_orders'],[[0,1,2],[1,2,0],[2,0,1]])
        self.assertEqual(proof['chosen'],[0,1,2]);self.assertIn([0,1,2,0],proof['majority_triangles'])

    def test_complete_kemeny_oracle_profiles(self):
        orders=list(itertools.permutations(range(3)))
        for profile in itertools.product(orders,repeat=3):
            proof=c.derive({'topics':['A','B','C']},{'ballots':[{'status':'KNOWN','order':list(o)} for o in profile]})
            score=lambda order:sum(1 for ballot in profile for i in range(3) for j in range(i+1,3) if ballot.index(order[i])>ballot.index(order[j]))
            scored=[(list(o),score(o)) for o in orders];best=min(s for o,s in scored)
            self.assertEqual(proof['minimum_disagreements'],best);self.assertEqual(proof['optimal_orders'],[o for o,s in scored if s==best])
            self.assertEqual(proof['candidates'],[{'order':o,'disagreements':s} for o,s in scored])

    def test_five_topic_random_profiles(self):
        rng=random.Random(61999);orders=list(itertools.permutations(range(5)))
        for _ in range(100):
            profile=[list(rng.choice(orders)) for _ in range(4)]
            proof=c.derive({'topics':list('ABCDE')},{'ballots':[{'status':'KNOWN','order':o} for o in profile]})
            expected=[sum(1 for b in profile for i in range(5) for j in range(i+1,5) if b.index(o[i])>b.index(o[j])) for o in orders]
            self.assertEqual([x['disagreements'] for x in proof['candidates']],expected)
            self.assertEqual(proof['minimum_disagreements'],min(expected))

class SdkJsonRegressionTests(unittest.TestCase):
    def test_sdk_returns_json_objects_without_string_decoding(self):
        o=fresh();key=sealed(o);host.queue=[output(),output()]
        self.assertEqual(json.loads(o.rank(key,3))['state'],'READY')

if __name__=='__main__':unittest.main(verbosity=2)
