/* v10 Coworker upgrades: live work screens, take-the-wheel, audit trail */
(function(){
const ROOMS=['LivingRoom','Kitchen','Bedroom','Bar','Booth'];
const STATUSES=['Working','Idle','Chatting','Drinking','Legendary-ing'];
/* ensure drawer exists (works with or without ui_plus) */
let dw=document.getElementById('drawer');
if(!dw){dw=document.createElement('div');dw.id='drawer';dw.innerHTML='<div class="dw-card"><h3 id="dwName"></h3><div class="dw-role" id="dwRole"></div></div>';document.body.appendChild(dw);}
const card=dw.querySelector('.dw-card')||dw;
card.insertAdjacentHTML('beforeend',
 '<div class="dw-sec">LIVE WORK SCREEN</div><div class="cw-term" id="cwTerm">(click a character)</div>'+
 '<div class="dw-sec">GOVERNANCE</div>'+
 '<div class="dw-row"><button class="btn" id="cwTake">🎮 take the wheel</button><button class="btn" id="cwRelease" style="display:none">↩ hand back</button></div>'+
 '<div class="cw-panel" id="cwPanel">'+
 '<select id="cwMove"><option value="">move to…</option>'+ROOMS.map(r=>`<option>${r}</option>`).join('')+'</select>'+
 '<select id="cwStatus"><option value="">set status…</option>'+STATUSES.map(s=>`<option>${s}</option>`).join('')+'</select>'+
 '<input id="cwTask" placeholder="assign a task…"><button class="btn" id="cwApply">apply</button></div>'+
 '<div class="dw-sec">THIS AGENT · AUDIT</div><div id="cwAudit" style="display:flex;flex-direction:column;gap:4px"></div>');
let cwAgent=null,tw={agent:null,src:'',pos:0};
function post(j){fetch('/api/control',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(j)}).catch(()=>{});}
C.addEventListener('click',()=>{if(!hover)return;cwAgent=hover;dw.classList.add('open');
 const p=CAST[hover]||{label:hover,role:'?'};
 const n=document.getElementById('dwName');if(n)n.textContent=p.label.toUpperCase()+(state.controlled===hover?' 🎮':''); 
 const r=document.getElementById('dwRole');if(r)r.textContent=p.role;});
document.getElementById('cwTake').onclick=()=>{if(!cwAgent)return;post({agent:cwAgent,take:true});
 document.getElementById('cwPanel').style.display='flex';document.getElementById('cwTake').style.display='none';document.getElementById('cwRelease').style.display='';toast('🎮 you are driving '+((CAST[cwAgent]||{label:cwAgent}).label));};
document.getElementById('cwRelease').onclick=()=>{if(!cwAgent)return;post({agent:cwAgent,release:true});
 document.getElementById('cwPanel').style.display='none';document.getElementById('cwRelease').style.display='none';document.getElementById('cwTake').style.display='';};
document.getElementById('cwApply').onclick=()=>{if(!cwAgent)return;
 const mv=document.getElementById('cwMove').value,st=document.getElementById('cwStatus').value,tk=document.getElementById('cwTask').value.trim();
 post({agent:cwAgent,move:mv||undefined,status:st||undefined,task:tk||undefined});
 document.getElementById('cwMove').value='';document.getElementById('cwStatus').value='';document.getElementById('cwTask').value='';};
/* typewriter for the live screen */
setInterval(()=>{const el=document.getElementById('cwTerm');if(!el||!cwAgent)return;
 const src=((state.agents||{})[cwAgent]||{}).screen||'(idle — no live work right now; assign a task below)';
 if(src!==tw.src||cwAgent!==tw.agent)tw={agent:cwAgent,src,pos:0};
 tw.pos=Math.min(src.length,tw.pos+3);
 el.innerHTML=esc(src.slice(0,tw.pos))+'<span class="cw-caret">▌</span>';},40);
/* per-agent audit refresh */
setInterval(()=>{const el=document.getElementById('cwAudit');if(!el||!cwAgent)return;
 el.innerHTML=(state.audit||[]).filter(a=>a.m.includes(cwAgent)).slice(-4).reverse().map(a=> 
  `<div class="audit-ln"><span class="ak ${a.k}">${a.k.toUpperCase()}</span>${esc(a.m)}</div>`).join('')||'<div style="font-size:10px;color:var(--lined)">no recorded actions yet</div>';},1500);
/* full audit tab */
const at=document.createElement('div');at.className='tab';at.dataset.t='audit';at.textContent='audit';
document.querySelector('.tabs').appendChild(at);
const ap=document.createElement('div');ap.className='panel';ap.dataset.p='audit';ap.innerHTML='<div class="grid" id="auditGrid"></div>'; 
document.querySelector('.panels').appendChild(ap);
at.onclick=()=>{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));document.querySelectorAll('.panel').forEach(x=>x.classList.remove('on'));at.classList.add('on');ap.classList.add('on');renderAudit();};
function renderAudit(){document.getElementById('auditGrid').innerHTML=(state.audit||[]).slice().reverse().map(a=> 
 `<div class="audit-ln"><span style="color:var(--lined)">${a.t}</span><span class="ak ${a.k}">${a.k.toUpperCase()}</span><span style="flex:1">${esc(a.m)}</span></div>`).join('')||'<div class="rowline">audit empty — every routing, ship & takeover lands here.</div>';}
setInterval(()=>{if(ap.classList.contains('on'))renderAudit();},2000);
})();
