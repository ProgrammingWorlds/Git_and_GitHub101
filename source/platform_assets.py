CSS=r'''
body.pw-nav{padding-inline-start:300px}
.pw-side{position:fixed;inset-block:0;inset-inline-start:0;width:300px;background:var(--card);border-inline-end:1px solid var(--line);overflow:auto;padding:14px 14px 40px;z-index:50;font:500 14px/1.5 Manrope,'IBM Plex Sans Arabic',sans-serif}
[lang=ar] .pw-side{font-family:'IBM Plex Sans Arabic',Manrope,sans-serif;font-weight:400}
.pw-brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--fg);font-weight:800;margin-bottom:10px}
.pw-brand img{width:34px;height:34px}
.pw-search{width:100%;padding:9px 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg);font:inherit}
.pw-search:focus{outline:2px solid var(--brand);outline-offset:1px}
.pw-res{margin:6px 0 0;padding:0;list-style:none}
.pw-side .pw-res li a{display:block;padding:7px 8px;border-radius:8px;text-decoration:none;color:var(--fg)}
.pw-res li a:hover{background:var(--soft)}
.pw-res small{display:block;color:var(--mut);font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pw-bar{height:8px;border-radius:99px;background:var(--line);overflow:hidden;margin:12px 0 4px}
.pw-bar i{display:block;height:100%;background:var(--amber);width:0;transition:width .3s}
.pw-pct{font-size:12px;color:var(--mut)}
.pw-side details{margin-top:6px;border-radius:10px}
.pw-side summary{cursor:pointer;padding:7px 8px;border-radius:8px;font-weight:700;list-style:none}
.pw-side summary:hover{background:var(--soft)}
.pw-side summary::-webkit-details-marker{display:none}
.pw-side details[open]>summary{color:var(--brand)}
.pw-side ul{list-style:none;margin:2px 0 6px;padding-inline-start:10px}
.pw-side ul a{display:flex;gap:8px;padding:5px 8px;border-radius:8px;text-decoration:none;color:var(--fg);font-size:13.5px}
.pw-side ul a:hover{background:var(--soft)}
.pw-side ul a.cur{background:var(--soft);font-weight:700;box-shadow:inset 3px 0 0 var(--amber)}
[dir=rtl] .pw-side ul a.cur{box-shadow:inset -3px 0 0 var(--amber)}
.pw-ck{flex:none;width:16px;height:16px;border-radius:50%;border:1.5px solid var(--mut);margin-top:3px;font-size:11px;line-height:13px;text-align:center}
a.done .pw-ck{background:var(--ok);border-color:var(--ok);color:#fff}
.pw-h{margin:14px 8px 4px;font:700 11px 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
[lang=ar] .pw-h{letter-spacing:0;font-family:'IBM Plex Sans Arabic';text-transform:none;font-size:12px}
.pw-burger{display:none;position:fixed;top:10px;inset-inline-start:10px;z-index:60;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:10px;padding:8px 12px;font:700 14px sans-serif;cursor:pointer}
.pw-copy{display:inline-block;margin:4px 0 8px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:8px;padding:4px 10px;font:700 12px Manrope,'IBM Plex Sans Arabic',sans-serif;cursor:pointer}
.pw-copy:hover{background:var(--soft)}
.pw-pre{position:relative}
.pw-pre .pw-copy{position:absolute;top:6px;inset-inline-end:6px;margin:0;opacity:.9}
.tk-git{color:#B36B00;font-weight:700}.tk-sub{color:var(--brand);font-weight:700}.tk-flag{color:#7A3FB5}.tk-str{color:var(--ok)}
:root[data-theme=dark] .tk-git,:root:not([data-theme=light]) .tk-git{color:#FFB23F}
.pw-done{display:inline-block;margin:18px 8px 0 0;padding:10px 18px;border-radius:999px;border:2px solid var(--brand);background:var(--soft);color:var(--fg);font:800 14px Manrope,'IBM Plex Sans Arabic',sans-serif;cursor:pointer}
.pw-done.on{background:var(--ok);border-color:var(--ok);color:#fff}
.pw-score{margin:12px 0;padding:12px 16px;border-radius:12px;font-weight:700}
.pw-score.ok{background:#DDF3E6;color:#0B4A2A}.pw-score.no{background:#FBE3E3;color:#7A1515}
.pw-home{max-width:1060px;margin:0 auto;padding:24px 20px 80px}
.pw-hero{border-radius:22px;padding:42px 32px;color:#fff;background:#0B1430 url(pw-background-ink_1920x1080.png) right center/cover no-repeat;margin:12px 0 22px}
.pw-hero h1{font:800 clamp(30px,5vw,48px)/1.15 Manrope,'IBM Plex Sans Arabic',sans-serif;margin:8px 0}
[lang=ar] .pw-hero h1{font-family:'IBM Plex Sans Arabic';font-weight:700}
.pw-hero p{max-width:560px;color:#DCDFF0;margin:6px 0 18px}
.pw-hero .k2{color:#FFB23F}
.pw-btn{display:inline-block;margin:0 8px 8px 0;padding:11px 20px;border-radius:999px;background:#FFB23F;color:#0B1430;font:800 14px Manrope,'IBM Plex Sans Arabic',sans-serif;text-decoration:none}
.pw-btn.alt{background:transparent;color:#fff;border:2px solid #fff}
.pw-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
.pw-card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px}
.pw-card h3{margin:2px 0 6px;font-size:17px}
.pw-card .n{font:700 12px 'JetBrains Mono',monospace;color:var(--brand)}
.pw-card ul{margin:6px 0;padding-inline-start:18px;font-size:14px}
.pw-card a{color:var(--fg)}
.pw-card .pw-bar{margin:8px 0 2px}
.pw-sec{font:800 22px Manrope,'IBM Plex Sans Arabic',sans-serif;margin:30px 0 12px}
@media(max-width:1000px){body.pw-nav{padding-inline-start:0}.pw-side{transform:translateX(-105%);transition:transform .2s}[dir=rtl] .pw-side{transform:translateX(105%)}.pw-side.open{transform:none!important}.pw-burger{display:block}.wrap{padding-top:56px!important}}
@media print{.pw-side,.pw-burger,.pw-copy,.pw-done{display:none!important}body.pw-nav{padding:0}}
'''
JS=r'''
(function(){
var D=window.PW_NAV, lang=document.documentElement.lang==='ar'?'ar':'en', N=D[lang], KEY='pw-git101-v1';
/* Progress store. To sync with a server, replace load()/save() with API calls
   (GET/PUT /api/progress/git-101) and keep the same JSON shape: {lessons:{"1-1":ts},quizzes:{"1":{score,ts}}}. */
var Store={load:function(){try{var s=JSON.parse(localStorage.getItem(KEY));if(s&&s.lessons)return s}catch(e){}return{lessons:{},quizzes:{}}},
 save:function(s){try{localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}}};
var cur=location.pathname.split('/').pop()||'';
function ids(){var a=[];N.modules.forEach(function(m){m.pages.forEach(function(p){a.push(p.id)})});return a}
function pct(s){var a=ids(),d=a.filter(function(i){return s.lessons[i]}).length;return Math.round(100*d/a.length)}
function esc(t){return String(t).replace(/[&<>]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function norm(t){return String(t).toLowerCase().replace(/[ً-ٟـ]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه')}
function curPage(){var r=null;N.modules.forEach(function(m){m.pages.forEach(function(p){if(p.f===cur)r=p})});return r}
function search(q){q=norm(q).trim();if(!q)return[];var terms=q.split(/\s+/),out=[];
 (window.PW_INDEX||[]).forEach(function(e){if(e.l!==lang)return;var t=norm(e.t),x=norm(e.x),sc=0;
  for(var i=0;i<terms.length;i++){var w=terms[i];if(t.indexOf(w)>-1)sc+=8;var k=x.indexOf(w);if(k>-1){sc+=2;var c=0,p=k;while((p=x.indexOf(w,p+1))>-1&&c<5)c++;sc+=c}else if(t.indexOf(w)<0){sc=-1;break}}
  if(sc>0){var k2=x.indexOf(terms[0]);out.push({e:e,sc:sc,sn:k2>-1?e.x.substr(Math.max(0,k2-30),90):e.x.substr(0,90)})}});
 out.sort(function(a,b){return b.sc-a.sc});return out.slice(0,8)}
function buildSide(){
 var s=Store.load(),side=document.createElement('aside');side.className='pw-side';
 var h='<a class="pw-brand" href="'+N.home+'"><img src="assets/PW-Symbol_color-light.svg" alt=""><span>Git &amp; GitHub 101</span></a>';
 h+='<input class="pw-search" type="search" placeholder="'+N.ui.search+'" aria-label="'+N.ui.search+'"><ul class="pw-res"></ul>';
 h+='<div class="pw-bar"><i></i></div><div class="pw-pct"></div>';
 N.modules.forEach(function(m){var open=m.pages.some(function(p){return p.f===cur});
  h+='<details'+(open?' open':'')+'><summary>'+m.n+'. '+esc(m.t)+'</summary><ul>';
  m.pages.forEach(function(p){h+='<a class="'+(p.f===cur?'cur ':'')+(s.lessons[p.id]?'done':'')+'" href="'+p.f+'" data-id="'+p.id+'"><span class="pw-ck">'+(s.lessons[p.id]?'✓':'')+'</span><span>'+esc(p.t)+'</span></a>'});
  h+='</ul></details>'});
 h+='<div class="pw-h">'+N.ui.extra+'</div><ul>';
 N.extra.forEach(function(p){h+='<a class="'+(p.f===cur?'cur':'')+'" href="'+p.f+'"><span class="pw-ck"></span><span>'+esc(p.t)+'</span></a>'});
 h+='</ul>';side.innerHTML=h;document.body.appendChild(side);document.body.classList.add('pw-nav');
 var b=document.createElement('button');b.className='pw-burger';b.textContent='☰ '+N.ui.menu;b.onclick=function(){side.classList.toggle('open')};document.body.appendChild(b);
 var inp=side.querySelector('.pw-search'),res=side.querySelector('.pw-res');
 inp.addEventListener('input',function(){var r=search(inp.value);res.innerHTML=r.map(function(x){return'<li><a href="'+x.e.f+'">'+esc(x.e.t)+'<small>'+esc(x.sn)+'</small></a></li>'}).join('')||(inp.value?'<li><small style="padding:6px 8px">'+N.ui.none+'</small></li>':'')});
 side.querySelectorAll('ul a.cur').forEach(function(a){a.scrollIntoView({block:'center'})});
 refreshBar()}
function refreshBar(){var s=Store.load(),p=pct(s),side=document.querySelector('.pw-side');if(!side)return;
 side.querySelector('.pw-bar i').style.width=p+'%';side.querySelector('.pw-pct').textContent=p+'% '+N.ui.done;
 side.querySelectorAll('a[data-id]').forEach(function(a){var d=!!s.lessons[a.dataset.id];a.classList.toggle('done',d);a.querySelector('.pw-ck').textContent=d?'✓':''})}
function copyBtns(){
 function mk(txt,after,inside){var b=document.createElement('button');b.className='pw-copy';b.type='button';b.textContent=N.ui.copy;
  b.onclick=function(){var t=txt();function ok(){b.textContent=N.ui.copied;setTimeout(function(){b.textContent=N.ui.copy},1500)}
   if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,function(){fb(t);ok()})}else{fb(t);ok()}};
  if(inside){after.appendChild(b)}else after.parentNode.insertBefore(b,after.nextSibling)}
 function fb(t){var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove()}
 document.querySelectorAll('.lesson p').forEach(function(p){var cs=[].slice.call(p.querySelectorAll('code')).map(function(c){return c.textContent}).filter(function(t){return /^(git|cd|mkdir|echo) /.test(t)});
  if(cs.length&&p.querySelector('br,code')&&/^(git|cd|mkdir|echo) /.test((p.querySelector('code')||{textContent:''}).textContent)&&(cs.length>1||p.textContent.trim()===cs[0].trim())){mk(function(){return cs.join('\n')},p,false)}});
 document.querySelectorAll('pre').forEach(function(pr){pr.classList.add('pw-pre');mk(function(){return pr.textContent},pr,true)})}
function highlight(){document.querySelectorAll('.lesson code').forEach(function(c){var t=c.textContent;if(!/^git /.test(t)||c.children.length)return;
 var parts=t.match(/"[^"]*"|\S+|\s+/g)||[],h='',n=0;parts.forEach(function(w){if(/^\s+$/.test(w)){h+=w;return}n++;
  var e=esc(w);h+=n===1?'<span class="tk-git">'+e+'</span>':n===2&&/^[a-z-]+$/.test(w)?'<span class="tk-sub">'+e+'</span>':/^"/.test(w)?'<span class="tk-str">'+e+'</span>':/^--?[a-zA-Z]/.test(w)?'<span class="tk-flag">'+e+'</span>':e});
 c.innerHTML=h})}
function doneBtn(){var pg=curPage();if(!pg)return;var les=document.querySelector('.lesson');if(!les)return;
 var b=document.createElement('button');b.type='button';b.className='pw-done';
 function set(){var on=!!Store.load().lessons[pg.id];b.classList.toggle('on',on);b.textContent=on?'✓ '+N.ui.completed:N.ui.mark}
 b.onclick=function(){var s=Store.load();if(s.lessons[pg.id])delete s.lessons[pg.id];else s.lessons[pg.id]=Date.now();Store.save(s);set();refreshBar()};
 set();les.appendChild(b)}
function quizScore(){var qs=document.querySelectorAll('.qq');if(!qs.length)return;var last=qs[qs.length-1],pg=curPage();
 var btn=document.createElement('button');btn.type='button';btn.className='pw-done pw-sc';btn.textContent=N.ui.score;var box=document.createElement('div');
 btn.onclick=function(){var ans=0,ok=0;qs.forEach(function(q){var r=q.querySelector('input:checked');if(r){ans++;if(r.dataset.c==='1')ok++}});
  if(ans<qs.length){box.className='pw-score no';box.textContent=N.ui.answerall;return}
  var p=Math.round(100*ok/qs.length),pass=p>=70;box.className='pw-score '+(pass?'ok':'no');box.textContent=ok+'/'+qs.length+' ('+p+'%) — '+(pass?N.ui.pass:N.ui.retry);
  if(pg&&/-q$/.test(pg.id)){var s=Store.load(),m=pg.id.split('-')[0];s.quizzes[m]={score:p,ts:Date.now()};if(pass)s.lessons[pg.id]=s.lessons[pg.id]||Date.now();Store.save(s);refreshBar()}};
 last.parentNode.insertBefore(btn,last.nextSibling);btn.parentNode.insertBefore(box,btn.nextSibling)}
function home(){var s=Store.load(),g=document.getElementById('modules'),h='';
 N.modules.forEach(function(m){var d=m.pages.filter(function(p){return s.lessons[p.id]}).length,p=Math.round(100*d/m.pages.length);
  h+='<div class="pw-card"><div class="n">'+N.ui.module+' '+String(m.n).padStart(2,'0')+'</div><h3>'+esc(m.t)+'</h3><ul>'+m.pages.map(function(x){return'<li><a href="'+x.f+'">'+(s.lessons[x.id]?'✓ ':'')+esc(x.t)+'</a></li>'}).join('')+'</ul><div class="pw-bar"><i style="width:'+p+'%"></i></div><div class="pw-pct">'+p+'%</div></div>'});
 g.innerHTML=h;var all=ids(),nx=all.filter(function(i){return !s.lessons[i]})[0],c=document.getElementById('cont'),first=N.modules[0].pages[0];
 var tgt=null;N.modules.forEach(function(m){m.pages.forEach(function(p){if(p.id===nx)tgt=p})});
 if(c){c.href=(tgt||first).f;c.textContent=Object.keys(s.lessons).length?N.ui.cont:N.ui.start}
 var pb=document.getElementById('totalbar');if(pb){pb.style.width=pct(s)+'%';document.getElementById('totalpct').textContent=pct(s)+'% '+N.ui.done}}
function theme(){var t=document.getElementById('tg');if(t&&!t.dataset.pw){t.dataset.pw=1}}
document.addEventListener('DOMContentLoaded',function(){
 try{var sv=localStorage.getItem('pw-theme');if(sv)document.documentElement.setAttribute('data-theme',sv)}catch(e){}
 if(document.body.dataset.pw==='home'){home();return}
 buildSide();highlight();copyBtns();doneBtn();quizScore()});
})();
'''
