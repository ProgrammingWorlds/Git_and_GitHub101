import asyncio, os
import build as b
from playwright.async_api import async_playwright
from pypdf import PdfWriter
O=b.O
def flow(bx, ar):
    out='<svg viewBox="0 0 700 150" xmlns="http://www.w3.org/2000/svg" font-family="Manrope,IBM Plex Sans Arabic,sans-serif" font-size="13" fill="#0B1430">'
    n=len(bx); w=140 if n==4 else 170; gap=(700-n*w)/(n-1)
    for i,(a,c) in enumerate(bx):
        x=i*(w+gap); f='#EEEFFE' if i<n-1 else '#FFF1D9'
        out+=f'<rect x="{x}" y="30" width="{w}" height="70" rx="12" fill="{f}" stroke="#3B41E3"/><text x="{x+w/2}" y="62" text-anchor="middle" font-weight="700">{a}</text><text x="{x+w/2}" y="82" text-anchor="middle" font-size="11" fill="#5A6280">{c}</text>'
        if i<n-1:
            x1=x+w+4; x2=x+w+gap-4; m=(x1+x2)/2
            out+=f'<path d="M{x1} 65H{x2}" stroke="#3B41E3" stroke-width="2.5" marker-end="url(#a)"/><text x="{m}" y="55" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="11" font-weight="700">{ar[i]}</text>'
    return out+'<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#3B41E3"/></marker></defs></svg>'
E={'en':{},'ar':{}}
E['en']['1.2']=dict(les='LESSON 1.2',lt='Git vs GitHub vs VS Code',other='Git مقابل GitHub مقابل VS Code',
 obj=['Define Git, GitHub and VS Code in one sentence each.','Explain local and remote repositories.','Tell public repositories from private ones.'],
 pre='Lesson 1.1.',intro='Beginners often use “Git” and “GitHub” as if they were one thing. They are three different tools that work together, and knowing the difference removes most early confusion.',
 exp=['<b>Git</b> is a free program on your computer. It records the history of your files. It works without internet.','<b>GitHub</b> is a website that stores Git projects online. It adds sharing and teamwork: backups, issues, pull requests and a profile page.','<b>VS Code</b> (Visual Studio Code) is a code editor. It has Git built in, so you can stage, commit and push with buttons instead of typing.','A <b>repository</b> (repo) is a project folder plus its Git history. Your copy is the <b>local repository</b>. The copy on GitHub is the <b>remote repository</b>. A <b>commit</b> is one saved snapshot, and a <b>branch</b> is a line of commits. You will study branches in Module 7.','<b>Public</b> repositories can be seen by anyone. <b>Private</b> repositories are visible only to you and people you invite. Never put passwords in either kind.'],
 ana='Writing a book: VS Code is your writing desk, Git is the editor who keeps every draft, and GitHub is the shared cloud folder your team reads.',
 cmd='No commands yet. In Lesson 2.1 you will install the tools and run <code>git --version</code>.',
 mis=[('Thinking GitHub is required to use Git.','Git works alone. GitHub is optional, but very useful for sharing.'),('Thinking VS Code and Git are the same.','VS Code is an editor. It only gives you buttons for Git.'),('Making a repo public by accident.','Check the visibility setting before you create or publish a repository.')],
 ex='Open github.com in your browser. Open any public repository. Find three things: the README text, the list of files, and the branch name (usually <code>main</code>).',
 res='You can point to the README, the file list and the branch selector on the page. You did not need an account for this.',
 q=[('Which tool stores your project online?',['GitHub','VS Code','Windows Terminal'],0,'GitHub hosts remote repositories.'),('Where is the local repository?',['On your computer','Only on GitHub','Inside the browser'],0,'The local repository is the project history stored on your own machine.'),('Who can see a private repository?',['Only you and people you invite','Everyone','Only GitHub staff'],0,'Private means visible only to you and chosen collaborators.')],
 sm='Git tracks changes, GitHub hosts repositories online, and VS Code is the editor with Git buttons. Your computer holds the local repository, GitHub holds the remote one.',
 voc=[('Repository','A project folder with its Git history'),('Local / Remote','On your computer / on GitHub'),('Public / Private','Visible to everyone / only to invited people'),('Branch','A line of commits')],
 nxt='<b>Lesson 1.3 — The Git workflow.</b> Next you will follow a file from your editor to GitHub, stage by stage.',
 svg=flow([('VS Code','editor'),('Git','your computer'),('GitHub','online')],['edit','push']),fig='Figure 1 · How the three tools fit together')
E['en']['1.3']=dict(les='LESSON 1.3',lt='Understanding the Git workflow',other='فهم سير عمل Git',
 obj=['Name the four places a change can live.','Recognize untracked, modified, staged and committed files.','Explain add → commit → push.'],
 pre='Lessons 1.1 and 1.2.',intro='Git does not save everything automatically. You choose what to save and when. That choice happens in stages, and learning them makes every later command easy to understand.',
 exp=['<b>Working directory</b>: your project folder, where you edit files.','<b>Untracked</b> files are new files Git has never seen. <b>Modified</b> files are tracked files you changed since the last commit.','<b>Staging area</b>: a waiting room. You place the changes you want in the next commit here. The command is <code>git add</code>.','<b>Local repository</b>: the history on your computer. <code>git commit</code> saves the staged changes as a new commit.','<b>Remote repository</b>: the copy on GitHub. <code>git push</code> sends your new commits there.','The <b>commit history</b> is the list of all commits. <b>Remember:</b> staging is not committing, and committing is not pushing. Each is a separate step.'],
 ana='Packing a parcel: you edit in your room (working directory), put the items you chose into the box (staging), seal and label it (commit), then send it by post (push).',
 cmd='You will learn these commands in Modules 4 and 5. For now, just recognize them: <code>git add</code>, <code>git commit -m "message"</code>, <code>git push</code>.',
 mis=[('Thinking add saves the work.','It only prepares changes. Nothing is saved until you commit.'),('Thinking commit uploads to GitHub.','Commit saves on your computer only. Push uploads.'),('Expecting new files to be tracked automatically.','New files are untracked until you add them.')],
 ex='Imagine you edit <code>index.html</code>, then run <code>git add index.html</code>, then <code>git commit -m "Add homepage"</code>. Write which stage the change is in after each of the three actions.',
 res='After editing: modified, in the working directory. After add: staged. After commit: saved in the local repository, not yet on GitHub.',
 q=[('Which command sends commits to GitHub?',['git push','git add','git commit'],0,'push uploads commits to the remote repository.'),('A brand-new file Git has never seen is…',['Untracked','Committed','Pushed'],0,'New files are untracked until you add them.'),('Does git add create a commit?',['No, it only stages changes','Yes','Only on Fridays'],0,'Staging prepares changes. Commit creates the snapshot.')],
 sm='A change travels from the working directory to the staging area (add), to the local repository (commit), and to the remote repository (push).',
 voc=[('Working directory','Your project folder'),('Staging area','Where changes wait for the next commit'),('Untracked / Modified','New file / changed tracked file'),('Push','Send commits to the remote')],
 nxt='<b>Module 2 — Installing and configuring Git.</b> You know the theory. Now you will install the tools and run your first command.',
 svg=flow([('Working directory','edit files'),('Staging area','chosen changes'),('Local repo','your commits'),('Remote repo','GitHub')],['git add','git commit','git push']),fig='Figure 1 · The add → commit → push workflow')
E['ar']['1.2']=dict(les='الدرس 1.2',lt='Git مقابل GitHub مقابل VS Code',other='Git vs GitHub vs VS Code',
 obj=['أن تعرّف Git وGitHub وVS Code بجملة لكل منها.','أن تشرح المستودع المحلي والمستودع البعيد.','أن تفرّق بين المستودع العام والخاص.'],
 pre='الدرس 1.1.',intro='يستخدم المبتدئون كلمتي Git وGitHub وكأنهما شيء واحد. هما في الحقيقة أداتان مختلفتان، وVS Code ثالثتهما. ومعرفة الفرق تزيل معظم الحيرة في البداية.',
 exp=['<b>Git</b> برنامج مجاني على جهازك يسجّل تاريخ ملفاتك، ويعمل دون إنترنت.','<b>GitHub</b> موقع يحفظ مشاريع Git على الإنترنت، ويضيف المشاركة والعمل الجماعي: نسخًا احتياطية، وقضايا (Issues)، وطلبات دمج (Pull Requests)، وصفحة تعريفية.','<b>VS Code</b> (Visual Studio Code) محرر أكواد فيه Git مدمج، فتستطيع التجهيز والحفظ والرفع بأزرار بدل الكتابة.','<b>المستودع (Repository)</b> هو مجلد المشروع مع تاريخ Git. نسختك هي <b>المستودع المحلي</b>، والنسخة على GitHub هي <b>المستودع البعيد</b>. و<b>الـ commit</b> لقطة محفوظة واحدة، و<b>الفرع (branch)</b> خط من الـ commits. ستدرس الفروع في الوحدة 7.','المستودعات <b>العامة</b> يراها أي شخص، و<b>الخاصة</b> لا يراها إلا أنت ومن تدعوهم. لا تضع كلمات السر في أي منهما أبدًا.'],
 ana='تأليف كتاب: VS Code طاولة الكتابة، وGit المحرّر الذي يحتفظ بكل مسودة، وGitHub المجلد المشترك على السحابة الذي يقرؤه فريقك.',
 cmd='لا توجد أوامر بعد. في الدرس 2.1 ستثبّت الأدوات وتشغّل <code>git --version</code>.',
 mis=[('الظن أن GitHub ضروري لاستخدام Git.','Git يعمل وحده. GitHub اختياري لكنه مفيد جدًا للمشاركة.'),('الظن أن VS Code وGit شيء واحد.','VS Code محرر فقط، ويعطيك أزرارًا لاستخدام Git.'),('جعل المستودع عامًا بالخطأ.','تحقّق من إعداد الخصوصية قبل إنشاء المستودع أو نشره.')],
 ex='افتح github.com في المتصفح، ثم افتح أي مستودع عام. جد ثلاثة أشياء: نص README، وقائمة الملفات، واسم الفرع (غالبًا <code>main</code>).',
 res='تستطيع الإشارة إلى README وقائمة الملفات ومحدد الفرع في الصفحة. لم تحتج إلى حساب لهذا.',
 q=[('أي أداة تحفظ مشروعك على الإنترنت؟',['GitHub','VS Code','Windows Terminal'],0,'GitHub يستضيف المستودعات البعيدة.'),('أين يوجد المستودع المحلي؟',['على جهازك','على GitHub فقط','داخل المتصفح'],0,'المستودع المحلي هو تاريخ المشروع المحفوظ على جهازك.'),('من يرى المستودع الخاص؟',['أنت ومن تدعوهم فقط','الجميع','موظفو GitHub فقط'],0,'الخاص يعني أنه مرئي لك وللمتعاونين الذين تختارهم.')],
 sm='Git يتتبّع التغييرات، وGitHub يستضيف المستودعات على الإنترنت، وVS Code محرر فيه أزرار Git. جهازك يحمل المستودع المحلي وGitHub يحمل البعيد.',
 voc=[('المستودع (Repository)','مجلد مشروع مع تاريخ Git'),('محلي / بعيد','على جهازك / على GitHub'),('عام / خاص','مرئي للجميع / للمدعوين فقط'),('الفرع (Branch)','خط من الـ commits')],
 nxt='<b>الدرس 1.3 — سير عمل Git.</b> بعده ستتبع ملفًا من محررك حتى GitHub مرحلة بمرحلة.',
 svg=E['en']['1.2']['svg'],fig='الشكل 1 · كيف تعمل الأدوات الثلاث معًا')
E['ar']['1.3']=dict(les='الدرس 1.3',lt='فهم سير عمل Git',other='Understanding the Git workflow',
 obj=['أن تسمّي الأماكن الأربعة التي قد يوجد فيها التغيير.','أن تميّز الملفات غير المتتبَّعة والمعدّلة والمجهّزة والمحفوظة.','أن تشرح add ثم commit ثم push.'],
 pre='الدرسان 1.1 و1.2.',intro='لا يحفظ Git كل شيء تلقائيًا. أنت تختار ماذا تحفظ ومتى. وهذا الاختيار يحدث على مراحل، وتعلّمها يجعل كل أمر لاحق سهل الفهم.',
 exp=['<b>مجلد العمل (Working directory)</b>: مجلد مشروعك حيث تعدّل الملفات.','الملفات <b>غير المتتبَّعة (Untracked)</b> ملفات جديدة لم يرها Git بعد. والملفات <b>المعدّلة (Modified)</b> ملفات متتبَّعة غيّرتها منذ آخر commit.','<b>منطقة التجهيز (Staging area)</b>: غرفة انتظار. تضع فيها التغييرات التي تريدها في الـ commit القادم. الأمر هو <code>git add</code>.','<b>المستودع المحلي</b>: التاريخ على جهازك. الأمر <code>git commit</code> يحفظ التغييرات المجهّزة كـ commit جديد.','<b>المستودع البعيد</b>: النسخة على GitHub. الأمر <code>git push</code> يرسل إليه الـ commits الجديدة.','<b>سجل الـ commits</b> هو قائمة كل الـ commits. <b>تذكّر:</b> التجهيز ليس حفظًا، والحفظ ليس رفعًا. كل منهما خطوة مستقلة.'],
 ana='تجهيز طرد بريدي: تعدّل في غرفتك (مجلد العمل)، وتضع ما اخترته في الصندوق (التجهيز)، وتغلقه وتكتب عليه (commit)، ثم ترسله بالبريد (push).',
 cmd='ستتعلم هذه الأوامر في الوحدتين 4 و5. الآن يكفي أن تتعرف عليها: <code>git add</code> و<code>git commit -m "message"</code> و<code>git push</code>.',
 mis=[('الظن أن add يحفظ العمل.','هو يجهّز التغييرات فقط. لا يُحفظ شيء حتى تنفّذ commit.'),('الظن أن commit يرفع إلى GitHub.','الـ commit يحفظ على جهازك فقط. الرفع يتم بـ push.'),('توقع أن تُتتبَّع الملفات الجديدة تلقائيًا.','الملفات الجديدة غير متتبَّعة حتى تضيفها بـ add.')],
 ex='تخيّل أنك عدّلت <code>index.html</code>، ثم نفّذت <code>git add index.html</code>، ثم <code>git commit -m "Add homepage"</code>. اكتب في أي مرحلة يكون التغيير بعد كل إجراء من الثلاثة.',
 res='بعد التعديل: معدّل في مجلد العمل. بعد add: مجهّز. بعد commit: محفوظ في المستودع المحلي ولم يصل GitHub بعد.',
 q=[('أي أمر يرسل الـ commits إلى GitHub؟',['git push','git add','git commit'],0,'push يرفع الـ commits إلى المستودع البعيد.'),('الملف الجديد الذي لم يره Git يسمى…',['غير متتبَّع (Untracked)','محفوظ (Committed)','مرفوع (Pushed)'],0,'الملفات الجديدة غير متتبَّعة حتى تضيفها بـ add.'),('هل ينشئ git add عملية commit؟',['لا، هو يجهّز التغييرات فقط','نعم','فقط يوم الجمعة'],0,'التجهيز يحضّر التغييرات، والـ commit هو الذي ينشئ اللقطة.')],
 sm='ينتقل التغيير من مجلد العمل إلى منطقة التجهيز (add)، ثم إلى المستودع المحلي (commit)، ثم إلى المستودع البعيد (push).',
 voc=[('مجلد العمل','مجلد مشروعك'),('منطقة التجهيز','حيث تنتظر التغييرات الـ commit القادم'),('غير متتبَّع / معدّل','ملف جديد / ملف متتبَّع تغيّر'),('Push','إرسال الـ commits إلى المستودع البعيد')],
 nxt='<b>الوحدة 2 — تثبيت Git وإعداده.</b> عرفت النظرية. الآن ستثبّت الأدوات وتشغّل أول أمر.',
 svg=E['en']['1.3']['svg'].replace('Working directory','Working dir').replace('edit files','edit'),fig='الشكل 1 · سير عمل add ثم commit ثم push')
MQ={'en':dict(h='Practical lab 1 · Identify every stage',lab='<p>Read the scenario and fill in the table. Scenario: you create <code>style.css</code>, edit <code>index.html</code>, then run <code>git add index.html</code>, <code>git commit -m "Add homepage"</code>, and <code>git push</code>.</p><table><tr><th>Moment</th><th>Where is <code>index.html</code>’s change?</th><th>Where is <code>style.css</code>?</th></tr><tr><td>After editing</td><td>Modified (working directory)</td><td>Untracked</td></tr><tr><td>After git add</td><td>Staged</td><td>Untracked</td></tr><tr><td>After git commit</td><td>Local repository</td><td>Untracked</td></tr><tr><td>After git push</td><td>Remote repository (GitHub)</td><td>Untracked</td></tr></table><div class="box b"><b>Evaluation:</b> 4 correct rows = pass. Note that <code>style.css</code> stays untracked because it was never added.</div>',qh='Module 1 quiz (pass mark: 70%)',
  q=[('What is Git?',['A program that tracks file history','A website','A code editor'],0,'Git is the version control program on your computer.'),('What is GitHub?',['A website that hosts Git repositories','A terminal','A file format'],0,'GitHub stores remote repositories online.'),('What does staging do?',['Prepares changes for the next commit','Uploads to GitHub','Deletes files'],0,'Staging selects the changes for the next commit.'),('After git commit, where are your changes?',['In the local repository','On GitHub','Nowhere'],0,'Commit saves on your computer; push is the step that uploads.'),('Can Git work without internet?',['Yes','No','Only on Windows'],0,'Git is distributed; the history is local.')]),
 'ar':dict(h='المختبر العملي 1 · حدّد كل مرحلة',lab='<p>اقرأ السيناريو واملأ الجدول. السيناريو: تنشئ <code>style.css</code>، وتعدّل <code>index.html</code>، ثم تنفّذ <code>git add index.html</code> و<code>git commit -m "Add homepage"</code> و<code>git push</code>.</p><table><tr><th>اللحظة</th><th>أين تغيير <code>index.html</code>؟</th><th>أين <code>style.css</code>؟</th></tr><tr><td>بعد التعديل</td><td>معدّل (مجلد العمل)</td><td>غير متتبَّع</td></tr><tr><td>بعد git add</td><td>مجهّز</td><td>غير متتبَّع</td></tr><tr><td>بعد git commit</td><td>المستودع المحلي</td><td>غير متتبَّع</td></tr><tr><td>بعد git push</td><td>المستودع البعيد (GitHub)</td><td>غير متتبَّع</td></tr></table><div class="box b"><b>معيار التقييم:</b> 4 صفوف صحيحة = نجاح. لاحظ أن <code>style.css</code> يبقى غير متتبَّع لأنك لم تضفه بـ add.</div>',qh='اختبار الوحدة 1 (علامة النجاح: 70%)',
  q=[('ما هو Git؟',['برنامج يتتبّع تاريخ الملفات','موقع إلكتروني','محرر أكواد'],0,'Git هو برنامج التحكم بالإصدارات على جهازك.'),('ما هو GitHub؟',['موقع يستضيف مستودعات Git','طرفية','صيغة ملفات'],0,'GitHub يحفظ المستودعات البعيدة على الإنترنت.'),('ماذا تفعل عملية التجهيز (staging)؟',['تحضّر التغييرات للـ commit القادم','ترفع إلى GitHub','تحذف الملفات'],0,'التجهيز يحدد التغييرات التي ستدخل الـ commit القادم.'),('بعد git commit أين توجد تغييراتك؟',['في المستودع المحلي','على GitHub','لا مكان'],0,'الـ commit يحفظ على جهازك، والرفع خطوة منفصلة.'),('هل يعمل Git دون إنترنت؟',['نعم','لا','فقط على ويندوز'],0,'Git موزّع، والتاريخ محلي.')])}
def extra(l):
    t=b.T[l]; m=MQ[l]
    MQ_q=[(a,)+b.shuf(i,o,c)+(w,) for i,(a,o,c,w) in enumerate(m['q'])]
    m={**m,'q':MQ_q}
    q=''.join(f'<div class="qq"><b>{i+1}. {a}</b>'+''.join(f'<label><input type="radio" name="m{i}" data-c="{int(j==c)}" data-w="{w}"> {x}</label>' for j,x in enumerate(o))+'<div class="fb"></div></div>' for i,(a,o,c,w) in enumerate(m['q']))
    ans=''.join(f'<li>{o[c]} — {w}</li>' for a,o,c,w in m['q'])
    return f'<section class="lesson"><div class="lessonhead"><div class="k2">{t["mod"]}</div><h1 class="lt">{m["h"]}</h1></div>{m["lab"]}<h3>{m["qh"]}</h3>{q}<h3>{t["H"]["ans"]}</h3><ul>{ans}</ul></section>'
def pages(l):
    return [b.lesson_html(l)]+[b.lesson_html(l,{**b.T[l],**E[l][k]}) for k in('1.2','1.3')]
async def main():
    names=['1-1','1-2','1-3','1-lab-quiz']; other={'en':'ar','ar':'en'}
    for l in('en','ar'):
        t=b.T[l]; body=pages(l)+[extra(l)]
        for i,n in enumerate(names):
            nav=''.join(f'<a href="lesson-{names[j]}-{l}.html"><button>{lab}</button></a>' for j,lab in((i-1,'←' if l=='en' else '→'),(i+1,'→' if l=='en' else '←')) if 0<=j<4)
            tools=f'<div class="tools">{nav}<a href="lesson-{n}-{other[l]}.html"><button>{"العربية" if l=="en" else "English"}</button></a><button id="tg">☾ / ☀</button></div>'
            open(f'{O}lesson-{n}-{l}.html','w',encoding='utf8').write(b.page(l,f'<div class="wrap">{tools}{body[i]}</div>{b.JS}'))
        full=b.book_body(l).split('<div class="wrap print">')[0]+'<div class="bgp"></div><div class="wrap print">'+'<div style="break-after:page"></div>'.join(body)+'</div>'
        open(f'{O}_b{l}.html','w',encoding='utf8').write(b.page(l,full))
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page()
        for l in('en','ar'):
            await pg.goto(f'file://{O}_b{l}.html'); await pg.wait_for_timeout(600)
            foot='<div style="width:100%;font:9px sans-serif;color:#5A6280;padding:0 18mm;display:flex;justify-content:space-between"><span>Programming Worlds Academy · Git &amp; GitHub 101</span><span class="pageNumber"></span></div>'
            await pg.pdf(path=f'/home/claude/{l}_m1.pdf',prefer_css_page_size=True,print_background=True,display_header_footer=True,header_template='<span></span>',footer_template=foot)
        await br.close()
    for l in('en','ar'):
        w=PdfWriter(); w.append(f'/home/claude/{l}_m1.pdf'); w.write(f'{O}Git-and-GitHub-101-{l.upper()}_Module01.pdf'); os.remove(f'{O}_b{l}.html')
    for f in os.listdir(O):
        if 'PREVIEW' in f or f.startswith('lesson-1-1-') and False: os.remove(O+f)
if __name__=="__main__": asyncio.run(main())
