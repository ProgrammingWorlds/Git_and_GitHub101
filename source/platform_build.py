import re, json, os, html
import build as b
from appendix_data import *
import platform_assets as pa
O=b.O
UI={'en':dict(search='Search lessons…',extra='Resources',menu='Menu',none='No results',copy='Copy',copied='Copied',completed='Completed',mark='Mark as complete',done='complete',score='Check my score',answerall='Answer every question first.',pass_='Passed',pass0='Passed',retry='Try again',start='Start the course',cont='Continue',module='Module',pass_x=''),
    'ar':dict(search='ابحث في الدروس…',extra='مصادر',menu='القائمة',none='لا نتائج',copy='نسخ',copied='تم النسخ',completed='مكتمل',mark='حدّد كمكتمل',done='مكتمل',score='تحقق من نتيجتي',answerall='أجب عن كل الأسئلة أولًا.',pass_='ناجح',pass0='ناجح',retry='حاول مجددًا',start='ابدأ الكورس',cont='تابع',module='الوحدة',pass_x='')}
for l in UI: UI[l]['pass']=UI[l]['pass_']
EXTRA={'en':[('final-project','Final project and rubric'),('cheatsheet','Git cheat sheet'),('glossary','Glossary'),('troubleshooting','Troubleshooting guide'),('screenshots','Screenshot checklist')],
       'ar':[('final-project','المشروع النهائي والمعايير'),('cheatsheet','ورقة أوامر Git'),('glossary','المصطلحات'),('troubleshooting','دليل حل المشاكل'),('screenshots','قائمة اللقطات')]}
LAB={'en':'Lab and quiz','ar':'المختبر والاختبار'}
def h1(f):
    return re.findall(r'<h1 class="lt">(.*?)</h1>',open(O+f,encoding='utf8').read())[0]
def strip(h):
    h=re.sub(r'<(script|style|svg)[\s\S]*?</\1>','',h); h=re.sub(r'<[^>]+>',' ',h); return re.sub(r'\s+',' ',html.unescape(h)).strip()
def nav():
    D={}
    for l in('en','ar'):
        mods=[]
        for m in range(1,13):
            pages=[dict(id=f'{m}-{k}',f=f'lesson-{m}-{k}-{l}.html',t=f'{m}.{k} '+h1(f'lesson-{m}-{k}-{l}.html')) for k in '123']
            pages.append(dict(id=f'{m}-q',f=f'lesson-{m}-lab-quiz-{l}.html',t=f'{m}.4 '+LAB[l]))
            mods.append(dict(n=m,t=MODS[l][m-1],pages=pages))
        D[l]=dict(home=f'index-{l}.html',modules=mods,extra=[dict(f=f'{k}-{l}.html',t=t) for k,t in EXTRA[l]],ui=UI[l])
    return D
def index():
    ix=[]
    for l in('en','ar'):
        for m in range(1,13):
            for k in ['1','2','3','lab-quiz']:
                f=f'lesson-{m}-{k}-{l}.html'; t=open(O+f,encoding='utf8').read()
                ix.append(dict(l=l,f=f,t=(f'{m}.{k} '+h1(f)) if k!='lab-quiz' else f'{m}.4 '+h1(f),x=strip(t.split('<div class="wrap">')[1])[:6000]))
        for k,_ in EXTRA[l]:
            f=f'{k}-{l}.html'
            if os.path.exists(O+f): ix.append(dict(l=l,f=f,t=dict(EXTRA[l])[k],x=strip(open(O+f,encoding='utf8').read().split('<div class="wrap">')[1])[:6000]))
    return ix
def patch(f):
    p=O+f; h=open(p,encoding='utf8').read()
    if '<!--pw-->' in h: h=re.sub(r'<!--pw-->.*?<!--/pw-->','',h,flags=re.S)
    m=re.search(r'<h1 class="lt">(.*?)</h1>',h)
    if m: h=re.sub(r'<title>.*?</title>','<title>Git &amp; GitHub 101 · '+re.sub(r'<[^>]+>','',m.group(1))+'</title>',h,count=1)
    h=h.replace('</head>','<!--pw--><link rel="stylesheet" href="assets/platform.css"><!--/pw--></head>',1)
    h=h.replace('</body>','<!--pw--><script src="assets/nav-data.js"></script><script src="assets/search-index.js"></script><script src="assets/platform.js"></script><!--/pw--></body>',1)
    open(p,'w',encoding='utf8').write(h)
def tools(l,name):
    o='ar' if l=='en' else 'en'
    return f'<div class="tools"><a href="index-{l}.html"><button>⌂</button></a><a href="{name}-{o}.html"><button>{"العربية" if l=="en" else "English"}</button></a><button id="tg">☾ / ☀</button></div>'
def wrap(l,name,body):
    return b.page(l,f'<div class="wrap">{tools(l,name)}<section class="lesson">{body}</section></div>{b.JS}')
def code(s): return '<code>'+html.escape(s)+'</code>'
def appendix_bodies(l):
    en=l=='en'; i=1 if en else 2
    B={}
    # cheat sheet
    s=f'<div class="lessonhead"><div class="k2">{"RESOURCE" if en else "مصدر"}</div><h1 class="lt">{"Git cheat sheet" if en else "ورقة أوامر Git"}</h1><div class="alt">{"Windows · Git Bash · VS Code" if en else "Windows · Git Bash · VS Code"}</div></div>'
    for g,rows in CHEAT:
        gname=g.split(' / ')[0 if en else 1]
        s+=f'<h3>{gname}</h3><table><tr><th>{"Command" if en else "الأمر"}</th><th>{"What it does" if en else "ماذا يفعل"}</th></tr>'+''.join(f'<tr><td>{code(r[0])}</td><td>{r[i]}</td></tr>' for r in rows)+'</table>'
    B['cheatsheet']=s
    s=f'<div class="lessonhead"><div class="k2">{"RESOURCE" if en else "مصدر"}</div><h1 class="lt">{"Glossary" if en else "المصطلحات"}</h1></div><table><tr><th>{"Term" if en else "المصطلح"}</th><th>{"Meaning" if en else "المعنى"}</th></tr>'+''.join(f'<tr><td><b>{t}</b></td><td>{r[i]}</td></tr>' for r in GLOSS for t in [r[0]])+'</table>'
    B['glossary']=s
    s=f'<div class="lessonhead"><div class="k2">{"RESOURCE" if en else "مصدر"}</div><h1 class="lt">{"Troubleshooting guide" if en else "دليل حل المشاكل"}</h1></div>'
    for r in TROUBLE:
        a=(r[0],r[1],r[2]) if en else (r[3],r[4],r[5])
        s+=f'<h3>{html.escape(a[0])}</h3><p><b>{"Cause:" if en else "السبب:"}</b> {a[1]}</p><div class="box b"><b>{"Fix:" if en else "الحل:"}</b> {a[2]}</div>'
    B['troubleshooting']=s
    s=f'<div class="lessonhead"><div class="k2">{"RESOURCE" if en else "مصدر"}</div><h1 class="lt">{"Screenshot checklist" if en else "قائمة اللقطات المطلوبة"}</h1></div><p>{"The course uses clearly labeled illustrations instead of real screenshots. To replace them, capture each item on Windows with an English interface and the dark theme, then send the files with the lesson number. Annotations (numbered callouts) are added afterwards." if en else "يستخدم الكورس رسومات توضيحية معنونة بدل اللقطات الحقيقية. للاستبدال التقط كل عنصر على Windows بواجهة إنجليزية والمظهر الداكن وأرسل الملفات مع رقم الدرس. تُضاف الأرقام التوضيحية بعد ذلك."}</p><table><tr><th>#</th><th>{"Lesson" if en else "الدرس"}</th><th>{"Capture" if en else "التقط"}</th></tr>'+''.join(f'<tr><td>{n+1}</td><td>{r[0]}</td><td>{r[i]}</td></tr>' for n,r in enumerate(SHOTS))+'</table>'
    B['screenshots']=s
    rub_en=[('Repository and structure',15,'Clear names, index.html, style.css, README, .gitignore'),('Commit history',20,'8+ commits with specific messages'),('Branches and pull requests',25,'3+ branches, 2+ merged PRs with descriptions'),('Website content',20,'Home, About, Projects, Contact work and look tidy'),('GitHub Pages',10,'Live URL opens with working CSS'),('README and safety',10,'README explains the project; no secrets committed')]
    rub_ar=[('المستودع والبنية',15,'أسماء واضحة وindex.html وstyle.css وREADME و.gitignore'),('تاريخ الـ commits',20,'8 commits أو أكثر برسائل محددة'),('الفروع والـ PRs',25,'3 فروع أو أكثر وpull requestان مدموجان بوصف'),('محتوى الموقع',20,'Home وAbout وProjects وContact تعمل وبمظهر مرتب'),('GitHub Pages',10,'الرابط الحي يفتح والـ CSS يعمل'),('README والأمان',10,'README يشرح المشروع؛ لا أسرار محفوظة')]
    R=rub_en if en else rub_ar
    s=f'<div class="lessonhead"><div class="k2">{"CAPSTONE" if en else "المشروع الختامي"}</div><h1 class="lt">{"Final project and rubric" if en else "المشروع النهائي والمعايير"}</h1></div>'
    s+=('<h3>Brief</h3><p>Build a one-page portfolio website with Home, About, Projects and Contact sections using plain HTML and CSS. Manage it with Git and GitHub like a team project and publish it with GitHub Pages.</p><h3>Requirements</h3><ul><li>Repository named <code>portfolio-website</code> with index.html, style.css, README.md and .gitignore.</li><li>At least 8 commits with specific messages.</li><li>At least 3 feature branches and 2 merged pull requests with descriptions.</li><li>No secrets in the repository.</li><li>Live GitHub Pages URL.</li></ul><h3>Starter and solution</h3><p>Starter files: <code>final-project/starter</code>. A sample solution: <code>final-project/solution</code>. Use the solution only to compare after you finish.</p><h3>Rubric (100 points, pass mark 70)</h3>' if en else '<h3>الوصف</h3><p>ابنِ موقع Portfolio من صفحة واحدة بأقسام Home وAbout وProjects وContact بـ HTML وCSS عاديين. أدِره بـ Git وGitHub كمشروع فريق وانشره بـ GitHub Pages.</p><h3>المتطلبات</h3><ul><li>مستودع باسم <code>portfolio-website</code> فيه index.html وstyle.css وREADME.md و.gitignore.</li><li>8 commits على الأقل برسائل محددة.</li><li>3 فروع ميزات على الأقل وpull requestان مدموجان بوصف.</li><li>لا أسرار في المستودع.</li><li>رابط GitHub Pages حي.</li></ul><h3>ملفات البداية والحل</h3><p>ملفات البداية: <code>final-project/starter</code>. وحل نموذجي: <code>final-project/solution</code>. استخدم الحل للمقارنة بعد أن تنتهي فقط.</p><h3>المعايير (100 نقطة، علامة النجاح 70)</h3>')
    s+=f'<table><tr><th>{"Criterion" if en else "المعيار"}</th><th>{"Points" if en else "النقاط"}</th><th>{"Full marks when…" if en else "العلامة الكاملة عندما…"}</th></tr>'+''.join(f'<tr><td>{a}</td><td>{p}</td><td>{c}</td></tr>' for a,p,c in R)+'</table>'
    B['final-project']=s
    return B
def home_page(l):
    en=l=='en'; o='ar' if en else 'en'
    t=b.T[l]
    body=f'''<div class="pw-home"><div class="tools"><a href="index-{o}.html"><button>{"العربية" if en else "English"}</button></a><button id="tg">☾ / ☀</button></div>
<div class="pw-hero"><div class="k2">PROGRAMMING WORLDS ACADEMY</div><h1><bdi dir="ltr">Git &amp; GitHub 101</bdi></h1><p>{"From zero to your first pull request. 12 modules, 36 lessons, 12 labs and a final project, for Windows and VS Code." if en else "من الصفر إلى أول Pull Request. 12 وحدة و36 درسًا و12 مختبرًا ومشروع نهائي، لنظام Windows وVS Code."}</p>
<a class="pw-btn" id="cont" href="lesson-1-1-{l}.html">{UI[l]["start"]}</a><a class="pw-btn alt" href="cheatsheet-{l}.html">{"Cheat sheet" if en else "ورقة الأوامر"}</a>
<div class="pw-bar"><i id="totalbar"></i></div><div class="pw-pct" id="totalpct" style="color:#DCDFF0"></div>
<div class="k2" style="margin-top:16px;color:#FFB23F;letter-spacing:.12em">BEYOND CODE. BEYOND LIMITS.</div></div>
<div class="pw-sec">{"Modules" if en else "الوحدات"}</div><div class="pw-grid" id="modules"></div>
<div class="pw-sec">{"Resources" if en else "مصادر"}</div><div class="pw-grid">'''+''.join(f'<div class="pw-card"><h3><a href="{k}-{l}.html">{t_}</a></h3></div>' for k,t_ in EXTRA[l])+'</div></div>'
    return b.page(l,body+b.JS).replace('<body ','<body data-pw="home" ',1)
def main():
    for l in('en','ar'):
        for name,body in appendix_bodies(l).items():
            open(f'{O}{name}-{l}.html','w',encoding='utf8').write(wrap(l,name,body))
        open(f'{O}index-{l}.html','w',encoding='utf8').write(home_page(l))
    open(O+'index.html','w',encoding='utf8').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Git &amp; GitHub 101</title><script>var l="en";try{l=localStorage.getItem("pw-lang")||((navigator.language||"").slice(0,2)==="ar"?"ar":"en")}catch(e){}location.replace("index-"+l+".html")</script><p><a href="index-en.html">English</a> · <a href="index-ar.html">العربية</a></p>')
    files=[f for f in os.listdir(O) if re.match(r'(lesson-.*|cheatsheet-.*|glossary-.*|troubleshooting-.*|screenshots-.*|final-project-.*|index-.*)\.html$',f)]
    for f in files: patch(f)
    open(O+'assets/platform.css','w').write(pa.CSS)
    open(O+'assets/platform.js','w').write(pa.JS)
    open(O+'assets/nav-data.js','w',encoding='utf8').write('window.PW_NAV='+json.dumps(nav(),ensure_ascii=False)+';')
    open(O+'assets/search-index.js','w',encoding='utf8').write('window.PW_INDEX='+json.dumps(index(),ensure_ascii=False)+';')
    print(len(files),'pages patched')
if __name__=='__main__': main()
