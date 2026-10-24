import asyncio, re
from playwright.async_api import async_playwright
from pypdf import PdfWriter
O = '/mnt/user-data/outputs/git-101-course/'

T = {
'en': dict(dir='ltr', lang='en', title='Git & GitHub 101', sub='From Zero to Your First Pull Request', slogan='Beyond Code. Beyond Limits.',
  acad='Programming Worlds Academy', logo='PW-Logo-Primary-Stacked_color-dark.svg', mod='MODULE 01', modt='Understanding Git & GitHub',
  modd='What version control is, why every developer uses it, and how Git, GitHub and VS Code fit together.',
  les='LESSON 1.1', lt='What is version control?', other='ما هو التحكم بالإصدارات؟',
  H=dict(obj='Learning objectives', pre='Prerequisites', intro='Introduction', exp='Explanation', ana='Real-world analogy', dia='Diagram',
   cmd='Commands', mis='Common mistakes and solutions', ex='Practical exercise', res='Expected result', q='Knowledge check', ans='Answers',
   sum='Summary', voc='Key vocabulary', nxt='Next lesson', fig='Figure 1 · Copying folders vs. a Git history'),
  obj=['Explain what version control is in your own words.','Describe three problems caused by copying project folders by hand.','Explain how Git records changes as a chain of commits.','Tell the difference between local and distributed version control.'],
  pre='None. You only need a computer and a project, even a simple text file, that you have edited more than once.',
  intro='Imagine you are writing an important report. On Monday you save <code>report.docx</code>. On Tuesday you change it and save <code>report_final.docx</code>. By Friday you have <code>report_final2.docx</code> and <code>report_REAL_final.docx</code>, and you are not sure which one is right. Version control solves exactly this problem, and it does it for every file in a project at once.',
  exp=['<b>Version control</b> is a system that records every change made to a set of files, who made it, when, and why. You can go back to any earlier moment, compare two moments, and work with other people without overwriting each other.',
       '<b>Why developers need it.</b> Code changes constantly. A new feature can break something that worked yesterday. With version control you can see exactly what changed and undo it safely. Teams also need it: five people can edit the same project and combine their work.',
       '<b>The problem with copying folders.</b> Copies take space, names become confusing, nothing explains <i>why</i> a copy exists, and two people copying the same folder can never merge their changes automatically.',
       '<b>How Git works.</b> Git does not keep random copies. When you tell it to, it saves a <b>commit</b>: a snapshot of your project plus a message and an author. Each commit points to the one before it, so your history is a chain you can walk backwards.',
       '<b>Local and distributed.</b> Older systems kept the history on one central server. Git is <b>distributed</b>: every developer has the full history on their own computer. You can work offline, and if a server is lost, any copy can restore it.'],
  ana='Think of a video game with save slots. Each save is a moment you can return to. A commit is a save point for your project, and the message is the label you write on it, such as “Before the boss fight”.',
  cmd='There are no commands in this lesson. In Lesson 2.1 you will install Git and run your first one, <code>git --version</code>.',
  mis=[('“Git is a backup tool.”','Git records meaningful changes you choose to save. Keep real backups too.'),('“I must be online to use Git.”','Git works fully offline. You only need internet to share with GitHub.'),('“Version control is only for big teams.”','It helps a single person from the first day of a project.')],
  ex='Find a project or document you have edited many times. Write down three situations where you wished you could go back or compare versions. For each one, note which Git idea (history, commit, or sharing) would help.',
  res='A short list of three real situations, each matched to an idea from this lesson. There is no right or wrong list. It prepares you for Lesson 1.2.',
  q=[('What does a commit store?',['A snapshot of the project, a message, and an author','Only the names of changed files','A copy of the internet'],0,'A commit is a snapshot with a message and author, linked to the commit before it.'),
     ('Why is Git called distributed?',['Every developer has the full history locally','It only runs on one server','It distributes free files'],0,'Each copy contains the whole history, so work does not depend on one central server.'),
     ('Which is a problem of copying folders by hand?',['Unclear names and no explanation of changes','Files become read-only','Windows deletes the copies'],0,'Names like final2 do not say what changed or why, and copies cannot be merged automatically.')],
  sm='Version control records the history of a project. Git saves snapshots called commits, keeps the full history on every computer, and lets you return to any point or combine work from several people.',
  voc=[('Version control','A system that records changes to files over time'),('Commit','A saved snapshot with a message and author'),('History','The chain of commits in a project'),('Distributed','Every copy holds the full history')],
  nxt='<b>Lesson 1.2 — Git vs GitHub vs VS Code.</b> You now know what Git does. Next you will meet the three tools you will use and see how they work together.',
  d_old='Copying folders', d_new='Git history', d_c='commit'),
'ar': dict(dir='rtl', lang='ar', title='Git و GitHub 101', sub='من الصفر إلى أول Pull Request', slogan='Beyond Code. Beyond Limits.',
  acad='أكاديمية عوالم البرمجة', logo='PW-Logo-Arabic_color-dark.svg', mod='الوحدة 01', modt='فهم Git وGitHub',
  modd='ما هو التحكم بالإصدارات، ولماذا يستخدمه كل مطوّر، وكيف تعمل أدوات Git وGitHub وVS Code معًا.',
  les='الدرس 1.1', lt='ما هو التحكم بالإصدارات؟', other='What is version control?',
  H=dict(obj='أهداف التعلم', pre='المتطلبات المسبقة', intro='مقدمة', exp='الشرح', ana='تشبيه من الحياة', dia='مخطط توضيحي',
   cmd='الأوامر', mis='أخطاء شائعة وحلولها', ex='تمرين عملي', res='النتيجة المتوقعة', q='اختبر فهمك', ans='الإجابات',
   sum='الخلاصة', voc='مصطلحات أساسية', nxt='الدرس التالي', fig='الشكل 1 · نسخ المجلدات مقابل سجل Git'),
  obj=['أن تشرح بكلماتك ما هو التحكم بالإصدارات.','أن تذكر ثلاث مشكلات تسببها نسخ مجلدات المشروع يدويًا.','أن تفهم كيف يسجّل Git التغييرات كسلسلة من الـ commits.','أن تفرّق بين التحكم بالإصدارات المحلي والموزّع.'],
  pre='لا شيء. تحتاج فقط إلى حاسوب ومشروع، ولو ملفًا نصيًا بسيطًا، عدّلته أكثر من مرة.',
  intro='تخيّل أنك تكتب تقريرًا مهمًا. يوم الاثنين تحفظ <code>report.docx</code>. يوم الثلاثاء تعدّله وتحفظ <code>report_final.docx</code>. وبحلول الجمعة يصبح عندك <code>report_final2.docx</code> و<code>report_REAL_final.docx</code>، ولم تعد متأكدًا أيّها الصحيح. التحكم بالإصدارات يحل هذه المشكلة بالضبط، ويفعل ذلك لكل ملفات المشروع دفعة واحدة.',
  exp=['<b>التحكم بالإصدارات (Version Control)</b> نظام يسجّل كل تغيير يحدث على مجموعة ملفات: من أجراه، ومتى، ولماذا. تستطيع العودة إلى أي لحظة سابقة، ومقارنة لحظتين، والعمل مع آخرين دون أن يمحو أحدكم عمل الآخر.',
       '<b>لماذا يحتاجه المطوّرون؟</b> الكود يتغيّر باستمرار، وقد تُفسد ميزة جديدة شيئًا كان يعمل بالأمس. مع التحكم بالإصدارات ترى بالضبط ما الذي تغيّر وتتراجع عنه بأمان. والفرق أيضًا تحتاجه: يستطيع خمسة أشخاص تعديل المشروع نفسه ودمج أعمالهم.',
       '<b>مشكلة نسخ المجلدات.</b> النسخ تستهلك مساحة، والأسماء تصبح مربكة، ولا شيء يشرح <i>لماذا</i> وُجدت نسخة ما، وشخصان ينسخان المجلد نفسه لا يمكن دمج تعديلاتهما تلقائيًا.',
       '<b>كيف يعمل Git؟</b> لا يحتفظ Git بنسخ عشوائية. عندما تطلب منه، يحفظ <b>commit</b>: لقطة من مشروعك مع رسالة واسم صاحبها. وكل commit يشير إلى الذي قبله، فيصبح تاريخ مشروعك سلسلة تستطيع المشي فيها إلى الخلف.',
       '<b>محلي وموزّع.</b> الأنظمة القديمة كانت تحفظ التاريخ في خادم مركزي واحد. أما Git فهو <b>موزّع</b>: لدى كل مطوّر التاريخ كاملًا على جهازه. يمكنك العمل دون إنترنت، وإن ضاع الخادم فأي نسخة تستطيع استعادته.'],
  ana='فكّر بلعبة فيديو فيها خانات حفظ. كل حفظ لحظة تستطيع العودة إليها. والـ commit نقطة حفظ لمشروعك، والرسالة هي الاسم الذي تكتبه عليها، مثل «قبل المعركة الأخيرة».',
  cmd='لا توجد أوامر في هذا الدرس. في الدرس 2.1 ستثبّت Git وتشغّل أول أمر وهو <code>git --version</code>.',
  mis=[('«Git أداة نسخ احتياطي.»','Git يسجّل التغييرات ذات المعنى التي تختار حفظها. احتفظ بنسخ احتياطية حقيقية أيضًا.'),('«يجب أن أكون متصلًا بالإنترنت لأستخدم Git.»','Git يعمل دون إنترنت تمامًا. تحتاج الإنترنت فقط للمشاركة عبر GitHub.'),('«التحكم بالإصدارات للفرق الكبيرة فقط.»','يفيد الشخص الواحد منذ اليوم الأول للمشروع.')],
  ex='اختر مشروعًا أو مستندًا عدّلته مرات كثيرة. اكتب ثلاث حالات تمنّيت فيها العودة إلى نسخة سابقة أو مقارنة النسخ. وبجانب كل حالة اكتب أي فكرة من Git تفيدك (التاريخ، أو الـ commit، أو المشاركة).',
  res='قائمة قصيرة من ثلاث حالات حقيقية، كل واحدة مرتبطة بفكرة من هذا الدرس. لا توجد قائمة صحيحة وأخرى خاطئة. هذا التمرين يهيّئك للدرس 1.2.',
  q=[('ماذا يخزّن الـ commit؟',['لقطة من المشروع ورسالة واسم صاحبها','أسماء الملفات المتغيرة فقط','نسخة من الإنترنت'],0,'الـ commit لقطة مع رسالة ومؤلف، ومرتبطة بالـ commit الذي قبلها.'),
     ('لماذا يسمى Git موزّعًا؟',['لأن لدى كل مطوّر التاريخ كاملًا على جهازه','لأنه يعمل على خادم واحد فقط','لأنه يوزّع ملفات مجانية'],0,'كل نسخة تحتوي التاريخ كاملًا، فلا يعتمد العمل على خادم مركزي واحد.'),
     ('ما مشكلة نسخ المجلدات يدويًا؟',['أسماء غير واضحة ولا تفسير للتغييرات','تصبح الملفات للقراءة فقط','ويندوز يحذف النسخ'],0,'أسماء مثل final2 لا تقول ما الذي تغيّر ولماذا، ولا يمكن دمج النسخ تلقائيًا.')],
  sm='التحكم بالإصدارات يسجّل تاريخ المشروع. يحفظ Git لقطات تسمى commits، ويُبقي التاريخ كاملًا على كل جهاز، ويسمح لك بالعودة إلى أي نقطة أو دمج عمل عدة أشخاص.',
  voc=[('التحكم بالإصدارات (Version control)','نظام يسجّل تغييرات الملفات مع الزمن'),('Commit','لقطة محفوظة مع رسالة واسم صاحبها'),('التاريخ (History)','سلسلة الـ commits في المشروع'),('موزّع (Distributed)','كل نسخة تحتوي التاريخ كاملًا')],
  nxt='<b>الدرس 1.2 — Git مقابل GitHub مقابل VS Code.</b> عرفت الآن ما يفعله Git. بعده ستتعرّف على الأدوات الثلاث التي ستستخدمها وكيف تعمل معًا.',
  d_old='نسخ المجلدات', d_new='سجل Git', d_c='commit'),
}

CSS = '''
@font-face{font-family:Manrope;src:url(assets/fonts/Manrope-Medium.ttf);font-weight:500}
@font-face{font-family:Manrope;src:url(assets/fonts/Manrope-Bold.ttf);font-weight:700}
@font-face{font-family:Manrope;src:url(assets/fonts/Manrope-ExtraBold.ttf);font-weight:800}
@font-face{font-family:'IBM Plex Sans Arabic';src:url(assets/fonts/IBMPlexSansArabic-Regular.ttf);font-weight:400}
@font-face{font-family:'IBM Plex Sans Arabic';src:url(assets/fonts/IBMPlexSansArabic-SemiBold.ttf);font-weight:600}
@font-face{font-family:'IBM Plex Sans Arabic';src:url(assets/fonts/IBMPlexSansArabic-Bold.ttf);font-weight:700}
@font-face{font-family:'JetBrains Mono';src:url(assets/fonts/JetBrainsMono-Medium.ttf);font-weight:500}
:root{--bg:#F6F5F1;--fg:#0B1430;--mut:#5A6280;--card:#fff;--line:#CDD1DE;--brand:#2C31C4;--soft:#EEEFFE;--amber:#FFB23F;--amber-s:#FFF1D9;--ok:#13693F;--err:#A12424}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0B1430;--fg:#F6F5F1;--mut:#A9AFC2;--card:#1B2340;--line:#2E3550;--brand:#8C90FF;--soft:#1A1E73;--amber-s:#2E2410}}
:root[data-theme=dark]{--bg:#0B1430;--fg:#F6F5F1;--mut:#A9AFC2;--card:#1B2340;--line:#2E3550;--brand:#8C90FF;--soft:#1A1E73;--amber-s:#2E2410}
h2,h3{break-after:avoid}tr{break-inside:avoid}figure,.box,.qq{break-inside:avoid}*{box-sizing:border-box}html{background:var(--bg)}
body{margin:0;color:var(--fg);font:500 15px/1.65 Manrope,'IBM Plex Sans Arabic',sans-serif}
[lang=ar] body,body[lang=ar]{font-family:'IBM Plex Sans Arabic',Manrope,sans-serif;font-weight:400;line-height:1.85}
.cover{height:297mm;width:210mm;background:#0B1430 url(assets/pw-background-ink_1920x1080.png) right center/auto 100% no-repeat;color:#fff;padding:22mm 20mm;display:flex;flex-direction:column;justify-content:space-between;page:cover;break-after:page}
.cover img{height:46mm;align-self:flex-start}
.cover .k{font:600 12px var(--mono,'JetBrains Mono');letter-spacing:.14em;color:#FFB23F}
[lang=ar] .cover .k{letter-spacing:0;font-family:'IBM Plex Sans Arabic';font-size:14px}
.cover h1{font-size:60px;line-height:1.05;font-weight:800;letter-spacing:-.025em;margin:10px 0 14px;max-width:150mm}
[lang=ar] .cover h1{font-weight:700;letter-spacing:0}
.cover p{font-size:20px;color:#BBBDF9;margin:0;max-width:120mm}
.cover .s{font:600 12px 'JetBrains Mono';letter-spacing:.12em;color:#A9AFC2}
.opener{height:297mm;width:210mm;background:#0B1430 url(assets/pw-pattern-Module-Field_ink_1024.png) right bottom/150mm no-repeat;color:#fff;padding:28mm 20mm;display:flex;flex-direction:column;justify-content:flex-end;page:cover;break-after:page}
.opener .n{font:800 120px/1 Manrope;color:#FFB23F;margin-bottom:8px}[lang=ar] .opener .n{font-family:'IBM Plex Sans Arabic';font-weight:700;font-size:96px}
.opener h2{font-size:42px;line-height:1.12;font-weight:800;margin:0 0 12px;color:#fff}.opener p{color:#BBBDF9;font-size:18px;max-width:130mm;margin:0 0 36mm}
.bgp{position:fixed;inset-inline-end:0;bottom:0;width:70mm;height:70mm;background:url(assets/pw-pattern-Module-Field_paper_1024.png) right bottom/cover no-repeat;opacity:.55;z-index:-1}
[dir=rtl] .bgp{transform:scaleX(-1)}
.lessonhead{border-bottom:3px solid var(--amber);padding-bottom:14px;margin-bottom:8px}
.k2{font:600 11px 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:var(--brand)}[lang=ar] .k2{font-family:'IBM Plex Sans Arabic';letter-spacing:0;text-transform:none;font-size:13px}
h1.lt{font-size:34px;line-height:1.1;font-weight:800;letter-spacing:-.02em;margin:6px 0 2px}[lang=ar] h1.lt{font-weight:700;letter-spacing:0}
.alt{color:var(--mut);font-size:15px;direction:ltr;text-align:start}[lang=ar] .alt{direction:ltr;text-align:right;font-family:Manrope}
h3{font-size:18px;font-weight:700;margin:22px 0 6px;color:var(--brand);display:flex;align-items:center;gap:10px}
h3:before{content:"";width:10px;height:10px;background:var(--amber);border-radius:2px}
ul{padding-inline-start:22px;margin:6px 0}li{margin:3px 0}
code{font:500 .88em 'JetBrains Mono',monospace;background:var(--soft);border-radius:4px;padding:1px 6px;direction:ltr;unicode-bidi:isolate;display:inline-block}
.box{border-radius:12px;padding:12px 16px;border-inline-start:4px solid var(--amber);background:var(--amber-s);margin:8px 0}
.box.b{border-color:var(--brand);background:var(--soft)}
figure{margin:12px 0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}figure svg{width:100%;height:auto;display:block;direction:ltr}
figcaption{font-size:12px;color:var(--mut);padding-top:6px}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden;font-size:13px}th,td{padding:8px 12px;text-align:start;border-bottom:1px solid var(--line);vertical-align:top}th{background:var(--soft)}
.qq{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0;break-inside:avoid}
.qq label{display:block;padding:6px 8px;border-radius:8px;cursor:pointer}.qq label:hover{background:var(--soft)}
.fb{margin-top:6px;font-size:13px;display:none}.fb.on{display:block}.fb.ok{color:var(--ok)}.fb.no{color:var(--err)}
.print .qq label{cursor:default}.wrap{max-width:820px;margin:0 auto;padding:24px 20px 80px}
.tools{display:flex;gap:8px;justify-content:flex-end;margin-bottom:12px}.tools button{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:999px;padding:6px 14px;font:700 13px Manrope,'IBM Plex Sans Arabic';cursor:pointer}
@page{size:A4;margin:18mm 18mm 20mm}@page cover{margin:0}
@media print{html{background:var(--bg)}.tools{display:none}.wrap{padding:0;max-width:none}h3,figure,table,.box{break-inside:avoid}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''

def esc(s): return s

def svg(t):
    return f'''<svg viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg" font-family="Manrope,IBM Plex Sans Arabic,sans-serif" font-size="13" fill="#0B1430">
<text x="20" y="22" font-weight="700" fill="#A12424">{t['d_old']}</text><text x="380" y="22" font-weight="700" fill="#2C31C4">{t['d_new']}</text>
<g font-family="JetBrains Mono,monospace" font-size="12"><rect x="20" y="36" width="270" height="30" rx="6" fill="#FCE4E4"/><text x="32" y="56">report.docx</text><rect x="20" y="76" width="270" height="30" rx="6" fill="#FCE4E4"/><text x="32" y="96">report_final.docx</text><rect x="20" y="116" width="270" height="30" rx="6" fill="#FCE4E4"/><text x="32" y="136">report_final2.docx</text><rect x="20" y="156" width="270" height="30" rx="6" fill="#FCE4E4"/><text x="32" y="176">report_REAL_final.docx</text></g>
<path d="M340 40v150" stroke="#CDD1DE" stroke-dasharray="4 4"/>
<path d="M410 110H640" stroke="#3B41E3" stroke-width="3"/>
<g fill="#3B41E3"><circle cx="410" cy="110" r="14"/><circle cx="490" cy="110" r="14"/><circle cx="570" cy="110" r="14"/></g><circle cx="640" cy="110" r="14" fill="#FFB23F"/>
<g fill="#fff" font-family="JetBrains Mono,monospace" font-size="11" text-anchor="middle"><text x="410" y="114">C1</text><text x="490" y="114">C2</text><text x="570" y="114">C3</text></g><text x="640" y="150" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11">HEAD</text>
</svg>'''

def shuf(i,o,c):
    k=[1,2,0,2,1,0][i%6]%len(o); idx=[(j+k)%len(o) for j in range(len(o))]
    return [o[j] for j in idx], idx.index(c)

def lesson_html(l, t=None):
    t = t or T[l]; H = T[l]['H']; L = 'ar' if l == 'ar' else 'en'
    q = ''
    qq=[]
    for i,(qs,opts,c,why) in enumerate(t['q']):
        o2,c2=shuf(i+1,opts,c); qq.append((qs,o2,c2,why))
    t={**t,'q':qq}
    for i, (qs, opts, c, why) in enumerate(t['q']):
        o = ''.join(f'<label><input type="radio" name="q{i}" data-c="{int(j==c)}" data-w="{why}"> {x}</label>' for j, x in enumerate(opts))
        q += f'<div class="qq"><b>{i+1}. {qs}</b>{o}<div class="fb"></div></div>'
    ans = ''.join(f'<li>{o[c]} — {why}</li>' for _, o, c, why in t['q'])
    mis = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in t['mis'])
    voc = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in t['voc'])
    return f'''<section class="lesson"><div class="lessonhead"><div class="k2">{t['mod']} · {t['les']}</div><h1 class="lt">{t['lt']}</h1><div class="alt">{t['other']}</div></div>
<h3>{H['obj']}</h3><ul>{''.join(f'<li>{x}</li>' for x in t['obj'])}</ul>
<h3>{H['pre']}</h3><p>{t['pre']}</p><h3>{H['intro']}</h3><p>{t['intro']}</p>
<h3>{H['exp']}</h3>{''.join(f'<p>{p}</p>' for p in t['exp'])}
<h3>{H['ana']}</h3><div class="box b">{t['ana']}</div>
<h3>{H['dia']}</h3><figure>{t.get('svg') or svg(t)}<figcaption>{t.get('fig') or H['fig']}</figcaption></figure>
<h3>{H['cmd']}</h3><p>{t['cmd']}</p>
<h3>{H['mis']}</h3><table>{mis}</table>
<h3>{H['ex']}</h3><div class="box">{t['ex']}</div><h3>{H['res']}</h3><p>{t['res']}</p>
<h3>{H['q']}</h3>{q}<h3>{H['ans']}</h3><ul>{ans}</ul>
<h3>{H['sum']}</h3><p>{t['sm']}</p><h3>{H['voc']}</h3><table>{voc}</table>
<h3>{H['nxt']}</h3><div class="box b">{t['nxt']}</div></section>'''

JS = '''<script>
document.querySelectorAll('.qq input').forEach(i=>i.onchange=()=>{const f=i.closest('.qq').querySelector('.fb');const ok=i.dataset.c==='1';f.className='fb on '+(ok?'ok':'no');f.textContent=(ok?'✓ ':'✗ ')+i.dataset.w});
const D=document.documentElement;function th(v){D.dataset.theme=v;try{localStorage.setItem('pw-theme',v)}catch(e){}}
try{const s=localStorage.getItem('pw-theme');if(s)D.dataset.theme=s}catch(e){}
document.getElementById('tg').onclick=()=>th(D.dataset.theme==='dark'?'light':'dark');
</script>'''

def page(l, body, tools=''):
    t = T[l]
    return f'<!doctype html><html lang="{t["lang"]}" dir="{t["dir"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t["title"]} · {t["les"]}</title><link rel="icon" href="assets/PW-Symbol_color-light.svg"><style>{CSS}</style></head><body lang="{t["lang"]}">{body}</body></html>'

def book_body(l):
    t = T[l]
    cover = f'<section class="cover"><img src="assets/{t["logo"]}" alt="Programming Worlds"><div><div class="k">{t["acad"].upper() if l=="en" else t["acad"]}</div><h1><bdi dir="ltr">{t["title"] if l=="en" else "Git &amp; GitHub 101"}</bdi></h1><p>{t["sub"]}</p></div><div class="s">{t["slogan"].upper()}</div></section>'
    opener = f'<section class="opener"><div class="n">01</div><div class="k2" style="color:#FFB23F">{t["mod"]}</div><h2>{t["modt"]}</h2><p>{t["modd"]}</p></section>'
    return cover + opener + '<div class="bgp"></div><div class="wrap print">' + lesson_html(l) + '</div>'

async def main():
    # HTML lesson pages (interactive)
    for l in ('en', 'ar'):
        t = T[l]
        tools = f'<div class="tools"><a href="lesson-1-1-{"ar" if l=="en" else "en"}.html"><button>{"العربية" if l=="en" else "English"}</button></a><button id="tg">☾ / ☀</button></div>'
        open(f'{O}lesson-1-1-{l}.html', 'w', encoding='utf8').write(page(l, f'<div class="wrap">{tools}{lesson_html(l)}</div>{JS}'))
        open(f'{O}_book-{l}.html', 'w', encoding='utf8').write(page(l, book_body(l)))
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for l in ('en', 'ar'):
            await pg.goto(f'file://{O}_book-{l}.html'); await pg.wait_for_timeout(600)
            foot = '<div style="width:100%;font:9px sans-serif;color:#5A6280;padding:0 18mm;display:flex;justify-content:space-between"><span>Programming Worlds Academy · Git &amp; GitHub 101</span><span class="pageNumber"></span></div>'
            await pg.pdf(path=f'/home/claude/{l}_book.pdf', prefer_css_page_size=True, print_background=True, display_header_footer=True, header_template='<span></span>', footer_template=foot)
        await b.close()
    for l in ('en', 'ar'):
        w = PdfWriter(); w.append(f'/home/claude/{l}_book.pdf'); w.write(f'{O}Git-and-GitHub-101-{l.upper()}_Module01-Lesson1.1_PREVIEW.pdf')
    import os
    for l in ('en', 'ar'): os.remove(f'{O}_book-{l}.html')
if __name__=='__main__': asyncio.run(main())
