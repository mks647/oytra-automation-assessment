"""Reproduce RealWorld API findings against disposable local data only."""
import json, urllib.request, urllib.error, uuid
from pathlib import Path
BASE='http://localhost:3000/api'
records=[]
def call(label,method,path,body=None,token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Token '+token
    req=urllib.request.Request(BASE+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
    try:
        with urllib.request.urlopen(req,timeout=15) as r: status=r.status; raw=r.read().decode()
    except urllib.error.HTTPError as e: status=e.code;raw=e.read().decode()
    try: result=json.loads(raw) if raw else {}
    except ValueError: result={'raw':raw}
    safe=json.loads(json.dumps(result))
    if isinstance(safe,dict) and isinstance(safe.get('user'),dict): safe['user'].pop('token',None)
    records.append({'test':label,'method':method,'path':path,'request':body,'status':status,'response':safe})
    return status,result
suffix=uuid.uuid4().hex[:8]
email=f'qa-{suffix}@example.test'
s,u=call('Sign up happy path','POST','/users',{'user':{'email':email,'username':'qa-'+suffix,'password':'LocalTest123!'}})
assert s==201,(s,u)
s,l=call('Login happy path','POST','/users/login',{'user':{'email':email,'password':'LocalTest123!'}});assert s==200
t=l['user']['token']
s,a=call('Create article','POST','/articles',{'article':{'title':'QA '+suffix,'description':'QA test','body':'Test article','tagList':['python','qa']}},t);assert s==201
slug=a['article']['slug']
s,a=call('Edit body only (check tag preservation)','PUT','/articles/'+slug,{'article':{'body':'Edited body'}},t)
assert s==200
call('Whitespace title accepted','POST','/articles',{'article':{'title':'   ','description':'   ','body':'   '}},t)
call('Invalid email and one character password','POST','/users',{'user':{'email':'invalid-'+suffix,'username':'weak-'+suffix,'password':'x'}})
call('One-character password with valid email','POST','/users',{'user':{'email':'weak-valid-'+suffix+'@example.test','username':'weak-valid-'+suffix,'password':'x'}})
call('Missing user payload','POST','/users/login',{})
call('Invalid pagination','GET','/articles?limit=abc')
call('Set bio','PUT','/user',{'user':{'bio':'Temporary QA biography'}},t)
call('Clear bio using empty string','PUT','/user',{'user':{'bio':''}},t)
call('Get bio after clear','GET','/user',token=t)
s,_=call('Delete article','DELETE','/articles/'+slug,token=t);assert s==204
call('Deleted article lookup','GET','/articles/'+slug)
call('Logged out (token removed)','GET','/user')
# Test malformed JSON handling independently.
req=urllib.request.Request(BASE+'/users',data=b'{bad-json',headers={'Content-Type':'application/json'},method='POST')
try: urllib.request.urlopen(req)
except urllib.error.HTTPError as e: records.append({'test':'Malformed JSON','method':'POST','path':'/users','request':'{bad-json','status':e.code,'response':e.read().decode()})
out=Path(__file__).resolve().parents[1]/'evidence'/'qa-results.json';out.write_text(json.dumps(records,indent=2))
for r in records: print(r['test'],r['status'],json.dumps(r['response'])[:180])
