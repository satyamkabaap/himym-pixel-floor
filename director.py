import json, time, os, sys, random, shutil, socket, threading, webbrowser
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime, timedelta

__version__="5.0.0"
if getattr(sys,'frozen',False):
    BASE_DIR=os.path.dirname(sys.executable); RES_DIR=sys._MEIPASS
else:
    BASE_DIR=os.path.dirname(os.path.abspath(__file__)); RES_DIR=BASE_DIR
DATA_DIR=os.path.join(BASE_DIR,'himym_data')
for d in [DATA_DIR, DATA_DIR+'/personas', DATA_DIR+'/outputs', DATA_DIR+'/inbox']:
    os.makedirs(d, exist_ok=True)

DEFAULT_PERSONAS={
 "ted":{"persona":"Romantic architect, pretentious about design, talks about destiny."},
 "barney":{"persona":"Confident, loves suits, legendary experiences, playbook tactics."},
 "marshall":{"persona":"Loyal lawyer, kind-hearted, loves his wife, monster enthusiast."},
 "lily":{"persona":"Matchmaker, artist, loves wine, friendly manipulation, fierce protector."},
 "robin":{"persona":"Independent Canadian news anchor, loves scotch, hates commitment."}}
QUIPS={
 "ted":["Kids, this is a great story.","Architecture is frozen music.","It's destiny!"],
 "barney":["Suit up!","Wait for it...","LEGENDARY!","Challenge accepted."],
 "marshall":["Lily would love this!","Sandwich? Anyone?","This is serious business."],
 "lily":["This needs wine.","I'm matchmaking, obviously.","Marshall, look at me!"],
 "robin":["I need scotch. Now.","Back in Canada...","This is fine."]}
AUTO_TASKS=["Plan a legendary party for Friday","Write Ted's pitch for the GNB building",
 "Draft the official slap bet contract","Research: best scotch under $50",
 "Design a redecoration for the apartment","Write a toast for the booth anniversary",
 "Marketing slogan for MacLaren's wing night","Fact-check Barney's playbook claims"]
EPISODES=[
 {"id":"slapsgiving","title":"Slapsgiving","weather":"snow","acts":[
   {"focus":"barney","loc":"Booth","lines":[("barney","I hereby declare: no slaps this Slapsgiving.")]},
   {"focus":"marshall","loc":"Booth","lines":[("marshall","Objection. The bet is eternal.")],"fx":"slap"},
   {"focus":"barney","loc":"Booth","lines":[("barney","Ow. Worth it. See you next year.")],
    "end":"Kids, that's the story of how Marshall won Slapsgiving. Again."}]},
 {"id":"french_horn","title":"The Blue French Horn","weather":"rain","acts":[
   {"focus":"ted","loc":"LivingRoom","lines":[("ted","Kids, sometimes destiny requires a little theft.")]},
   {"focus":"ted","loc":"Bar","lines":[("ted","The blue french horn speaks for me.")],"fx":"confetti"},
   {"focus":"robin","loc":"Bar","lines":[("robin","...Fine. But I'm still not crying.")],
    "end":"And that, kids, is why there's a blue french horn on the wall."}]},
 {"id":"legendary_party","title":"The Legendary Party","weather":"clear","acts":[
   {"focus":"barney","loc":"Bar","lines":[("barney","Suit up! Tonight, we make history.")],"fx":"confetti"},
   {"focus":"lily","loc":"Bar","lines":[("lily","I'm matchmaking. Obviously. At a party.")]},
   {"focus":"marshall","loc":"Booth","lines":[("marshall","Sandwich buffet. I'm in heaven.")],
    "end":"It was going to be legendary. It was."}]},
 {"id":"playbook","title":"The Playbook","weather":"clear","acts":[
   {"focus":"barney","loc":"Bar","lines":[("barney","Allow me to introduce... Lorenzo Von Matterhorn.")]},
   {"focus":"robin","loc":"Bar","lines":[("robin","Fact-check: you're not a billionaire. Nice try.")]},
   {"focus":"barney","loc":"Booth","lines":[("barney","...Challenge accepted.")],
    "end":"Kids, never let them watch you revise the playbook."}]}
]
class HIMYMDirector:
    def __init__(self):
        self.data_file=DATA_DIR+'/sim_data.json'; self.memory_file=DATA_DIR+'/memory_store.json'
        self.tasks_file=DATA_DIR+'/tasks.json'; self.rel_file=DATA_DIR+'/relationships.json'
        self.ach_file=DATA_DIR+'/achievements.json'; self.outputs_dir=DATA_DIR+'/outputs'; self.inbox=DATA_DIR+'/inbox'
        self.agents=["ted","barney","marshall","lily","robin"]
        self.locations={"Apartment":["LivingRoom","Kitchen","Bedroom"],"MacLarens":["Bar","Booth"]}
        self.llm_url="http://127.0.0.1:3001/v1/chat/completions"
        self.llm_key=os.environ.get("HIMYM_LLM_KEY","")
        _kf=os.path.join(DATA_DIR,"llm_key.txt")
        if not self.llm_key and os.path.exists(_kf):
            self.llm_key=open(_kf).read().strip()
        self.sim_start=datetime.now(); self.time_scale=30; self.tick=0; self.day=1
        self.weather='clear'; self.memory={}; self.ep=None; self.recap=None; self.recap_n=0
        self.stats={'tasks_done':0,'reviews':0,'revisions':0,'total_slaps':0,'total_legendary':0}
        self.achievements={k:False for k in ['first_slap','slap_10','all_legendary','playbook_used','first_ship','ship_10']}
        self.collab={a:{b:0 for b in self.agents} for a in self.agents}
        self.relationships={
            "ted":{"barney":75,"marshall":90,"lily":85,"robin":70},
            "barney":{"ted":75,"marshall":60,"lily":65,"robin":55},
            "marshall":{"ted":90,"barney":60,"lily":100,"robin":75},
            "lily":{"ted":85,"barney":65,"marshall":100,"robin":80},
            "robin":{"ted":70,"barney":55,"marshall":75,"lily":80}}
        self.tasks=[]; self.events=[]; self.auto=True
        self.load_persistent()
        if os.path.exists(self.tasks_file):
            try: self.tasks=json.load(open(self.tasks_file))
            except Exception: pass
        if not os.path.exists(self.memory_file):
            json.dump({a:[] for a in self.agents}, open(self.memory_file,'w'), indent=2)

    # ---------- persistence ----------
    def load_persistent(self):
        try:
            if os.path.exists(self.rel_file): self.relationships.update(json.load(open(self.rel_file)))
            if os.path.exists(self.ach_file):
                d=json.load(open(self.ach_file)); self.achievements.update(d.get('achievements',{})); self.stats.update(d.get('stats',{}))
        except Exception: pass
    def save_persistent(self):
        json.dump(self.relationships, open(self.rel_file,'w'), indent=2)
        json.dump({'achievements':self.achievements,'stats':self.stats}, open(self.ach_file,'w'), indent=2)

    def log(self,m): self.events.append({'t':datetime.now().strftime('%H:%M:%S'),'m':m}); print('  ⚡',m)
    def unlock(self,k):
        if not self.achievements.get(k): self.achievements[k]=True; self.log(f'🏆 Achievement: {k}!')
    def save_tasks(self): json.dump(self.tasks, open(self.tasks_file,'w'), indent=2)
    def add_task(self,text,src='user'):
        tid=max([t['id'] for t in self.tasks],default=0)+1
        self.tasks.append({'id':tid,'text':text,'stage':'queued','worker':None,'reviewer':None,'draft':'','review':'','revisions':0})
        self.tasks=self.tasks[-12:]; self.save_tasks(); self.log(f'📥 task #{tid} queued ({src}): {text[:60]}'); return tid
    def scan_inbox(self):
        for f in sorted(os.listdir(self.inbox)):
            if f.endswith(('.txt','.md')):
                p=os.path.join(self.inbox,f); text=open(p,encoding='utf-8',errors='ignore').read().strip()
                if text: self.add_task(text,'inbox')
                os.remove(p)
    def tod(self):
        h=(self.sim_start+timedelta(seconds=self.tick*self.time_scale)).hour
        return 'morning' if 6<=h<12 else 'afternoon' if 12<=h<17 else 'evening' if 17<=h<21 else 'night'
    def persona(self,n):
        try: return json.load(open(DATA_DIR+f'/personas/{n}.json'))['persona']
        except Exception: return DEFAULT_PERSONAS[n]['persona']
    def llm(self,agent,prompt):
        try:
            if not self.llm_key: return None
            r=requests.post(self.llm_url,headers={"Authorization":f"Bearer {self.llm_key}"},
                json={"model":"local-model","messages":[{"role":"system","content":self.persona(agent)},{"role":"user","content":prompt}]},timeout=2)
            if r.status_code==200: return r.json()['choices'][0]['message']['content'].strip().strip('"')
        except Exception: pass
        return None
    def recall_line(self,name):
        mem=self.memory.get(name,[])
        if mem and random.random()<0.35:
            m=random.choice(mem[-8:])
            return f"Remember when I was {m.get('status','chilling')} in {m.get('sub','the bar')}? Good times."
        return random.choice(QUIPS[name])
    def update_rel(self,a,b,d):
        for x,y in ((a,b),(b,a)):
            if x in self.relationships and y in self.relationships[x]:
                self.relationships[x][y]=max(0,min(100,self.relationships[x][y]+d))

    # ---------- WORK PIPELINE (reviewer chosen by friendship) ----------
    def pick_worker(self,text):
        t=text.lower()
        if any(k in t for k in ['design','art','decor','paint']): return 'lily'
        if any(k in t for k in ['legal','contract','law','risk']): return 'marshall'
        if any(k in t for k in ['research','fact','news','scotch']): return 'robin'
        if any(k in t for k in ['party','legend','market','pitch','slogan','toast']): return 'barney'
        return 'ted'
    def pick_reviewer(self,w):
        return max([a for a in self.agents if a!=w], key=lambda a: self.relationships.get(w,{}).get(a,0))
    def fb_draft(self,w,text):
        L={'ted':['Design concept: symmetry + destiny','Materials: brick, glass, heart','Timeline: worth the wait'],
        'barney':['Hook: it\'s going to be LEGENDARY','Audience: everyone awesome','CTA: suit up immediately'],
        'marshall':['Clause 1: be excellent to each other','Clause 2: sandwiches mandatory','Risk assessment: low, vibes high'],
        'lily':['Palette: warm yellow + red','Mood: cozy, slightly chaotic','Final touch: wine'],
        'robin':['Fact: sources say yes','Counterpoint: whatever, scotch','Verdict: fine, it works']}
        return '\n'.join('- '+l for l in L.get(w,L['ted']))+f'\n(re: {text[:80]})'
    def fb_review(self,rv,first):
        if rv=='marshall': return random.choice(['APPROVE: legally airtight. Also, awesome.','REVISE: needs a sandwich clause.']) if first else 'APPROVE: good enough for my court.'
        return random.choice(['APPROVE: chef\'s kiss.','REVISE: more wine, less beige.']) if first else 'APPROVE: fine, I love it.'

    def step_tasks(self):
        applies=[]
        if self.auto and not self.ep and not [t for t in self.tasks if t['stage']!='done'] and random.random()<0.5:
            self.add_task(random.choice(AUTO_TASKS),'auto')
        for t in self.tasks:
            if t['stage']=='done': continue
            if t['stage']=='queued':
                t['worker']=self.pick_worker(t['text']); t['stage']='drafting'
                applies.append((t['worker'],'Working',f'On it: {t["text"][:40]}')); self.log(f'🎯 task #{t["id"]} → {t["worker"]}')
            elif t['stage']=='drafting':
                t['draft']=self.llm(t['worker'],f'Draft this in character, 3 short bullets: {t["text"]}') or self.fb_draft(t['worker'],t['text'])
                t['reviewer']=self.pick_reviewer(t['worker']); t['stage']='reviewing'; self.stats['reviews']+=1
                applies+=[(t['worker'],'Chatting','Draft sent for review.'),(t['reviewer'],'Working','Reviewing the draft...')]
                self.log(f'📝 #{t["id"]} drafted by {t["worker"]} → review by {t["reviewer"]} (friendship {self.relationships[t["worker"]][t["reviewer"]]})')
            elif t['stage']=='reviewing':
                t['review']=self.llm(t['reviewer'],f'Start with APPROVE or REVISE, then one in-character sentence. Draft: {t["draft"][:300]}') or self.fb_review(t['reviewer'],t['revisions']==0)
                if t['review'].upper().startswith('APPROVE') or t['revisions']>=1:
                    t['stage']='done'; self.stats['tasks_done']+=1
                    self.update_rel(t['worker'],t['reviewer'],2)                 # shipping builds friendship
                    self.collab[t['worker']][t['reviewer']]+=1; self.collab[t['reviewer']][t['worker']]+=1
                    self.unlock('first_ship')
                    if self.stats['tasks_done']>=10: self.unlock('ship_10')
                    fn=f'task_{t["id"]:03d}_{t["worker"]}.md'
                    open(os.path.join(self.outputs_dir,fn),'w',encoding='utf-8').write(
                        f'# Task {t["id"]}: {t["text"]}\n\n## Draft by {t["worker"]}\n{t["draft"]}\n\n## Review by {t["reviewer"]}\n{t["review"]}\n')
                    applies+=[(t['worker'],'Legendary-ing','Done! Saved to outputs.'),(t['reviewer'],'Chatting',t['review'][:60])]
                    self.log(f'✅ #{t["id"]} approved → outputs/{fn}')
                    if any(k in t['text'].lower() for k in ['party','legend']) and not self.ep and random.random()<0.35:
                        self.start_episode('legendary_party')                    # work triggers episode
                else:
                    t['revisions']+=1; self.stats['revisions']+=1; t['stage']='revising'
                    self.update_rel(t['worker'],t['reviewer'],-1)
                    applies+=[(t['reviewer'],'Chatting',t['review'][:60]),(t['worker'],'Working','Revising...')]
            elif t['stage']=='revising':
                t['draft']=(self.llm(t['worker'],f'Improve using feedback. Feedback: {t["review"][:200]} Draft: {t["draft"][:200]}') or t['draft']+'\n- revised: addressed all notes')
                t['stage']='reviewing'
        self.save_tasks(); return applies

    # ---------- EPISODE ENGINE (wraps spawn follow-up work) ----------
    def start_episode(self,eid):
        ep=next((e for e in EPISODES if e['id']==eid),None)
        if ep and not self.ep:
            self.ep={'d':ep,'act':0,'tick':0}; self.log(f'🎬 episode started: {ep["title"]}'); return True
        return False
    def step_episode(self,agent_data):
        e=self.ep; acts=e['d']['acts']; act=acts[e['act']]; fx=[]
        if e['tick']==0:
            for name,line in act['lines']:
                agent_data[name]['status']='Chatting'; agent_data[name]['last_dialogue']=line; agent_data[name]['sub_location']=act['loc']
            if act.get('fx')=='slap':
                fx.append('slap'); self.stats['total_slaps']+=1; self.update_rel('marshall','barney',-10)
                self.unlock('first_slap')
                if self.stats['total_slaps']>=10: self.unlock('slap_10')
                self.log(f'👋 SLAP! (total {self.stats["total_slaps"]})')
            if act.get('fx')=='confetti':
                fx.append('confetti'); self.stats['total_legendary']+=1; self.unlock('all_legendary')
            if e['d']['id']=='playbook': self.unlock('playbook_used')
            self.log(f'🎬 {e["d"]["title"]} — act {e["act"]+1}/{len(acts)}')
        e['tick']+=1
        out={'id':e['d']['id'],'title':e['d']['title'],'act':e['act']+1,'acts':len(acts),'focus':act.get('focus')}
        if e['tick']>=3:
            e['tick']=0; e['act']+=1
            if e['act']>=len(acts):
                self.recap_n+=1
                self.recap={'n':self.recap_n,'title':e['d']['title'],'line':act.get('end',''),'day':self.day}
                self.add_task(f"Write a recap toast for '{e['d']['title']}'",'episode')   # episode triggers work
                self.ep=None; self.log('🎬 episode wrapped → follow-up task queued')
        return out,fx

    # ---------- main loop ----------
    def run_simulation(self):
        print(f'🎬 HIMYM engine v{__version__} — workflow × episodes, fully integrated. Close window to stop.\n')
        while True:
            try:
                self.tick+=1
                if self.tick%48==1:
                    self.day+=1; self.log(f'🌅 day {self.day} begins')
                    self.weather='rain' if random.random()<0.3 else 'clear'
                tod=self.tod(); self.scan_inbox()
                loc='MacLarens' if tod in('evening','night') else 'Apartment'
                if random.random()<0.12: loc='Apartment' if loc=='MacLarens' else 'MacLarens'
                with open(self.memory_file) as f: self.memory=json.load(f)
                agent_data={}
                for a in self.agents:
                    agent_data[a]={'status':random.choice(['Idle','Drinking','Chatting'] if tod in('evening','night') else ['Idle','Working','Chatting']),
                        'sub_location':random.choice(self.locations[loc]),'last_dialogue':self.recall_line(a),
                        'memory':self.memory.get(a,[])[-3:],'conversation_partner':None,'time_of_day':tod}
                fx=[]
                for name,status,dlg in self.step_tasks():
                    agent_data[name]['status']=status; agent_data[name]['last_dialogue']=dlg
                ep_out=None
                if self.auto and not self.ep and random.random()<0.10:
                    self.start_episode(random.choice(EPISODES)['id'])
                if self.ep:
                    ep_out,efx=self.step_episode(agent_data); fx+=efx
                json.dump({'location':loc,'agents':agent_data,'logs':self.events[-20:],'stats':self.stats,
                    'collab':self.collab,'relationships':self.relationships,'achievements':self.achievements,
                    'tasks':[{'id':t['id'],'text':t['text'],'stage':t['stage'],'worker':t['worker'],'reviewer':t['reviewer']} for t in self.tasks[-8:]],
                    'episode':ep_out,'recap':self.recap,'fx':fx,'day':self.day,
                    'weather':(self.ep and self.ep['d'].get('weather')) or self.weather,
                    'sim_time':(self.sim_start+timedelta(seconds=self.tick*self.time_scale)).isoformat(),'time_of_day':tod},
                    open(self.data_file,'w'), indent=2)
                self.save_persistent()
                print(f'📍 {loc} ({tod}) day {self.day} | ships:{self.stats["tasks_done"]} slaps:{self.stats["total_slaps"]}')
                time.sleep(3)
            except KeyboardInterrupt: print('\n👋 Stopped.'); self.save_persistent(); break
            except Exception as e: print('⚠️',e); time.sleep(2)

DIRECTOR=None
class Handler(SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=DATA_DIR,**k)
    def log_message(s,*a): pass
    def do_POST(s):
        ok=False
        if s.path.startswith(('/api/task','/api/episode')):
            n=int(s.headers.get('Content-Length',0))
            try: j=json.loads(s.rfile.read(n).decode())
            except Exception: j={}
            ok = DIRECTOR.add_task((j.get('text') or '').strip(),'ui') if s.path.startswith('/api/task') and (j.get('text') or '').strip() else DIRECTOR.start_episode(j.get('id',''))
        s.send_response(200); s.send_header('Content-Type','application/json'); s.end_headers()
        s.wfile.write(json.dumps({'ok':bool(ok)}).encode())
    def do_GET(s):
        if s.path.startswith('/api/health'):
            s.send_response(200); s.send_header('Content-Type','application/json'); s.end_headers()
            s.wfile.write(json.dumps({'ok':True,'version':__version__,'day':DIRECTOR.day}).encode())
        else: super().do_GET()

def setup_assets():
    for f in ['dashboard.html','floor_day.png','floor_night.png']:
        src=os.path.join(RES_DIR,f)
        if os.path.exists(src): shutil.copy(src, os.path.join(DATA_DIR,f))
    for n,p in DEFAULT_PERSONAS.items():
        dst=DATA_DIR+f'/personas/{n}.json'
        if not os.path.exists(dst): json.dump(p,open(dst,'w'),indent=2)

if __name__=='__main__':
    setup_assets(); DIRECTOR=HIMYMDirector()
    port=8000
    for p in range(8000,8010):
        try: s=socket.socket(); s.bind(("127.0.0.1",p)); s.close(); port=p; break
        except OSError: continue
    httpd=HTTPServer(("127.0.0.1",port),Handler)
    threading.Thread(target=httpd.serve_forever,daemon=True).start()
    print('='*56); print(f'  HIMYM PIXEL FLOOR v{__version__} — THE CROSSOVER RELEASE'); print(f'  http://localhost:{port}/dashboard.html'); print('='*56)
    threading.Timer(1.2,lambda:webbrowser.open(f'http://localhost:{port}/dashboard.html')).start()
    DIRECTOR.run_simulation(); httpd.shutdown()