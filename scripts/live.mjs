import {runtime,need} from './runtime.mjs';
const {people,journal,read,step,checkpoint}=await runtime('agendalock');
const topics=['Logistics','Branding','Safety'];
const key=(actor,tag)=>people[actor].address+':'+tag;
const opts=(actor,tag,extra={})=>({readMethod:'get_agenda',recordId:key(actor,tag),...extra});
const payload=(title,actors)=>JSON.stringify({title,topics,members:actors.map(a=>people[a].address)});
const s1='Safety is my first priority, Logistics is second, and Branding is last.';
const s2='I rank Safety highest, then Logistics, then Branding.';
async function mainCase(){
 const id=key('owner','planning'),o=extra=>opts('owner','planning',extra);
 await step('open-main','owner','open_agenda',['planning',payload('Operations planning',['owner','member'])],o({check:r=>r.state==='COLLECTING'}));
 await step('submit-owner','owner','submit',[id,0,s1],o({check:r=>r.revision===1}));
 await step('submit-member','member','submit',[id,1,s2],o({check:r=>r.revision===2}));
 await step('cannot-rewrite-ballot','owner','submit',[id,2,s2],o({error:'BALLOT_IMMUTABLE'}));
 await step('nonmoderator-freeze','outsider','freeze',[id,2],o({error:'MODERATOR_ONLY'}));
 await step('freeze-main','owner','freeze',[id,2],o({check:r=>r.state==='SEALED'&&r.revision===3}));
 const r=await step('rank-main','member','rank',[id,3],o({check:r=>r.state==='READY'&&JSON.stringify(r.proof.chosen)==='[2,0,1]'&&r.proof.minimum_disagreements===0}));
 await step('nonmoderator-start','member','start',[id,4,r.ranking_hash],o({error:'MODERATOR_ONLY'}));
 await step('wrong-ranking-hash','owner','start',[id,4,'0'.repeat(64)],o({error:'RANKING_MISMATCH'}));
 await step('start-main','owner','start',[id,4,r.ranking_hash],o({check:r=>r.state==='RUNNING'&&r.revision===5}));
 await step('cannot-skip-topic','owner','advance',[id,5,0],o({error:'WRONG_NEXT_TOPIC'}));
 await step('complete-safety','owner','advance',[id,5,2],o({check:r=>r.cursor===1&&r.state==='RUNNING'}));
 await step('complete-logistics','owner','advance',[id,6,0],o({check:r=>r.cursor===2}));
 await step('complete-branding','owner','advance',[id,7,1],o({check:r=>r.state==='CLOSED'&&r.cursor===3}));
 await step('cannot-repeat-closed','owner','advance',[id,8,1],o({error:'NOT_RUNNING'}));
}
async function unknownCase(){
 const id=key('third','unclear'),o=extra=>opts('third','unclear',extra);
 await step('open-unclear','third','open_agenda',['unclear',payload('Unranked priorities',['third','member'])],o({check:r=>r.state==='COLLECTING'}));
 await step('unclear-owner','third','submit',[id,0,'All three topics are equally important to me; I do not rank them.'],o({check:r=>r.revision===1}));
 await step('unclear-member','member','submit',[id,1,s2],o({check:r=>r.revision===2}));
 await step('freeze-unclear','third','freeze',[id,2],o({check:r=>r.state==='SEALED'}));
 const r=await step('rank-unclear','third','rank',[id,3],o({check:r=>r.state==='REVIEW'&&r.proof.unknown_members.includes(0)}));
 await step('review-cannot-start','third','start',[id,4,r.ranking_hash],o({error:'NOT_READY'}));
 await step('member-cancel','member','cancel',[id,4],o({check:r=>r.state==='CANCELLED'}));
}
async function cycleCase(){
 const id=key('outsider','cycle'),o=extra=>opts('outsider','cycle',extra),actors=['outsider','owner','member'];
 await step('open-cycle','outsider','open_agenda',['cycle',payload('Cyclic priorities',actors)],o({check:r=>r.state==='COLLECTING'}));
 const statements=['Logistics is first, Branding second, Safety third.','Branding is first, Safety second, Logistics third.','Safety is first, Logistics second, Branding third.'];
 for(const [i,actor] of actors.entries())await step('cycle-'+i,actor,'submit',[id,i,statements[i]],o({check:r=>r.revision===i+1}));
 await step('freeze-cycle','outsider','freeze',[id,3],o({check:r=>r.state==='SEALED'}));
 const r=await step('rank-cycle','owner','rank',[id,4],o({check:r=>r.state==='READY'&&r.proof.optimal_orders.length===3&&r.proof.minimum_disagreements===4&&r.proof.majority_triangles.length>0}));
 await step('start-cycle','outsider','start',[id,5,r.ranking_hash],o({check:r=>r.state==='RUNNING'}));
 for(const [i,topic] of r.proof.chosen.entries())await step('cycle-complete-'+i,'outsider','advance',[id,6+i,topic],o({check:r=>r.cursor===i+1}));
}
const results=await Promise.allSettled([mainCase(),unknownCase(),cycleCase()]);
for(const r of results)if(r.status==='rejected')throw r.reason;
journal.final_records={planning:await read('get_agenda',[key('owner','planning')]),unclear:await read('get_agenda',[key('third','unclear')]),cycle:await read('get_agenda',[key('outsider','cycle')])};
need(journal.final_records.planning.state==='CLOSED'&&journal.final_records.cycle.state==='CLOSED','Final agenda closure missing');
journal.acceptance_completed=true;await checkpoint();console.log('AgendaLock acceptance complete',journal.address);
