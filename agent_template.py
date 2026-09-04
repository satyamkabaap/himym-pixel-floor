import os, json, sys
def load_persona(name):
    with open(os.path.join('agents','personas',name+'.json'),encoding='utf-8') as f: return json.load(f)['persona']
def get_world_state():
    with open(os.path.join('himym_data','sim_data.json'),encoding='utf-8') as f: return json.load(f)
if __name__=='__main__':
    name=sys.argv[1].strip().lower() if len(sys.argv)>1 else 'ted'
    print(f"I am {name}. Persona: {load_persona(name)[:80]}...")