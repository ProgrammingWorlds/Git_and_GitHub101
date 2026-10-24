import asyncio, os
import build as b, build_m1 as m
from playwright.async_api import async_playwright
from pypdf import PdfWriter
O=b.O
def term(lines, cap):
    h=40+22*len(lines); o=f'<svg viewBox="0 0 700 {h}" xmlns="http://www.w3.org/2000/svg" font-family="JetBrains Mono,monospace" font-size="13"><rect width="700" height="{h}" rx="10" fill="#1F1F1F"/><rect width="700" height="26" rx="10" fill="#181818"/><circle cx="16" cy="13" r="4" fill="#FF5F57"/><circle cx="30" cy="13" r="4" fill="#FEBC2E"/><circle cx="44" cy="13" r="4" fill="#28C840"/><text x="350" y="17" fill="#9D9D9D" font-size="11" text-anchor="middle" font-family="sans-serif">{cap}</text>'
    for i,s in enumerate(lines):
        c='#FFB23F' if s.startswith('$') else '#E8E8E8'
        o+=f'<text x="18" y="{54+22*i}" fill="{c}" xml:space="preserve">{s.replace("&","&amp;").replace("<","&lt;")}</text>'
    return o+'</svg>'
OUT=['$ git --version','git version 2.x.x.windows.1']
CFG=['$ git config --global --list','user.name=Your Name','user.email=you@example.com','init.defaultbranch=main']
E={'en':{},'ar':{}}
base=dict(mod='MODULE 02',modt='Installing and Configuring Git',modd='Install Git and VS Code, create your GitHub account, and tell Git who you are.')
basea=dict(mod='الوحدة 02',modt='تثبيت Git وإعداده',modd='ثبّت Git وVS Code، وأنشئ حساب GitHub، وعرّف Git بنفسك.')
E['en']['1']=dict(base,les='LESSON 2.1',lt='Installing Git and VS Code',other='تثبيت Git وVS Code',
 obj=['Install Git on Windows.','Install Visual Studio Code.','Open the integrated terminal and choose Git Bash.','Verify the installation with <code>git --version</code>.'],
 pre='Module 1. A Windows computer and an internet connection.',intro='Before any command works, the tools must be on your computer. This lesson installs both, then checks that Git answers.',
 exp=['<b>Install Git.</b> Go to <code>git-scm.com</code> and choose <b>Download for Windows</b>. Run the installer. The default options are safe for beginners. You may choose Visual Studio Code as the default editor, and choose <b>main</b> as the name for new branches if the installer offers it. Click Next until Install, then Finish.','<b>Verify.</b> Open <b>Git Bash</b> from the Start menu and run <code>git --version</code>. If Git answers with a version number, it is installed.','<b>Install VS Code.</b> Go to <code>code.visualstudio.com</code>, download the Windows installer and run it. Keep <b>Add to PATH</b> enabled.','<b>Open the terminal in VS Code.</b> Use the menu <b>Terminal → New Terminal</b>, or press <code>Ctrl+`</code>. In the terminal panel, use the dropdown arrow next to the <b>+</b> and choose <b>Git Bash</b> as the profile.'],
 ana='Installing tools is like stocking a kitchen before you cook: nothing to cook yet, but every recipe in this course needs these tools.',
 cmd='<p>Run this in Git Bash or the VS Code terminal. <code>--version</code> is an option that asks the program to print its version and exit.</p><code>git --version</code>',
 mis=[('“git is not recognized”','Close and reopen the terminal. If it still fails, run the Git installer again.'),('Opening PowerShell and expecting Bash commands.','Choose Git Bash in the terminal profile list.'),('Skipping Add to PATH for VS Code.','Re-run the installer and enable it.')],
 ex='Install Git and VS Code, open a terminal inside VS Code, select Git Bash, and run <code>git --version</code>.',res='The terminal prints a line starting with <code>git version</code>.',
 q=[('Which command checks the Git installation?',['git --version','git start','git check'],0,'<code>git --version</code> prints the installed version.'),('Which terminal do we use in this course?',['Git Bash','Notepad','Paint'],0,'Git Bash gives us the same commands on Windows.'),('Which shortcut opens a terminal in VS Code?',['Ctrl+`','Ctrl+Z','Alt+F4'],0,'Ctrl+` toggles the integrated terminal.')],
 sm='You installed Git and VS Code, opened a terminal in VS Code, chose Git Bash, and confirmed Git works.',voc=[('Terminal','A text window for typing commands'),('Git Bash','A Bash terminal that comes with Git for Windows'),('PATH','The list of folders Windows searches for programs')],
 nxt='<b>Lesson 2.2 — Creating your GitHub account.</b> The tools are ready. Next you create your online home.',
 svg=term(OUT,'Illustration · Git Bash (not a real screenshot)'),fig='Figure 1 · Illustration of the expected output')
E['en']['2']=dict(base,les='LESSON 2.2',lt='Creating your GitHub account',other='إنشاء حساب GitHub',
 obj=['Create and verify a GitHub account.','Find your way around the dashboard.','Secure the account with two-factor authentication.','Name the ways Git signs in to GitHub.'],
 pre='Lesson 2.1 and an email address you can open.',intro='Your GitHub account is your identity online. Your projects, your history and your future portfolio live there, so we protect it from day one.',
 exp=['<b>Create the account.</b> Go to <code>github.com</code> and choose <b>Sign up</b>. Enter your email, a strong password and a username. Choose a username you would be happy to show an employer.','<b>Verify your email.</b> GitHub sends a code to your email. Enter it to finish. You may also be asked to solve a short puzzle.','<b>The dashboard.</b> After sign-in you see your repositories, activity and suggestions. Your avatar (top right) opens the menu with <b>Your profile</b>, <b>Your repositories</b> and <b>Settings</b>.','<b>Profile.</b> Add a photo and a short bio. Keep personal details you do not want public out of it.','<b>Security.</b> Use a unique password in a password manager. In <b>Settings → Password and authentication</b> enable <b>two-factor authentication (2FA)</b> with an authenticator app, and save the recovery codes somewhere safe.','<b>How Git signs in.</b> Over <b>HTTPS</b>, Git asks for your GitHub login through a sign-in window and keeps it in Git Credential Manager (included with Git for Windows). With <b>SSH</b>, you add a key pair to your account. Never use your GitHub password as a Git password in the terminal. You will set up a method in Module 5.'],
 ana='Your account is like a bank account for your code: a strong password and a second lock (2FA) keep it yours.',
 cmd='No Git commands here. All steps happen in the browser.',
 mis=[('Losing the 2FA recovery codes.','Store them in a password manager or print them.'),('Using a private email in public commits.','Later you can use the GitHub “noreply” address (Lesson 2.3).'),('Choosing a joke username.','Pick a professional one. It becomes part of your URLs.')],
 ex='Create your account, verify the email, add a profile photo, and turn on 2FA.',res='You can open your profile at <code>github.com/your-username</code> and Settings shows 2FA as enabled.',
 q=[('Why enable 2FA?',['A second check protects the account','It makes Git faster','It is required to install Git'],0,'2FA stops access with only a stolen password.'),('Where do your projects live online?',['GitHub','VS Code','Git Bash'],0,'GitHub hosts your remote repositories.'),('Name one way Git signs in to GitHub.',['SSH keys','Email attachments','Screenshots'],0,'HTTPS with Credential Manager and SSH keys are the two common methods.')],
 sm='You created and secured a GitHub account and learned the two sign-in methods Git uses: HTTPS and SSH.',voc=[('2FA','A second proof of identity at sign-in'),('HTTPS / SSH','Two ways Git connects to GitHub'),('Dashboard','Your home page on GitHub')],
 nxt='<b>Lesson 2.3 — First-time Git configuration.</b> Now you tell Git who you are.',
 svg=m.flow([('Git Bash','your computer'),('Sign-in','HTTPS or SSH'),('GitHub','your account')],['git push','verify']),fig='Figure 1 · Git proves who you are before it uploads')
E['en']['3']=dict(base,les='LESSON 2.3',lt='First-time Git configuration',other='إعداد Git لأول مرة',
 obj=['Set your name, email and default branch.','Check your settings.','Explain global and local configuration.','Separate commit identity from GitHub sign-in.'],
 pre='Lessons 2.1 and 2.2.',intro='Every commit records who made it. Git cannot guess this, so you set it once.',
 exp=['<b>Set your identity.</b> Run the first two commands below with your own details. Use the email of your GitHub account, or the private “noreply” address that GitHub shows in <b>Settings → Emails</b>.','<b>Default branch.</b> The third command makes new repositories start with a branch named <code>main</code>.','<b>Check.</b> <code>git config --global --list</code> prints every global setting.','<b>Global vs local.</b> <code>--global</code> saves in your user file and applies to all repositories. Without it, inside a repository, a setting is <b>local</b> and applies only there. Local wins over global.','<b>Identity vs sign-in.</b> Name and email are only labels stamped on commits. They do not prove who you are. <b>Authentication</b> (HTTPS login or SSH key) is what lets you push. You can use SSH later: <code>ssh-keygen -t ed25519 -C "you@example.com"</code> creates a key pair. We finish that in Module 5.'],
 ana='The name and email are the signature on a letter. Anyone can write a signature, but only your key opens the mailbox.',
 cmd='<code>git config --global user.name "Your Name"</code><br><code>git config --global user.email "you@example.com"</code><br><code>git config --global init.defaultBranch main</code><br><code>git config --global --list</code><p><b>Options:</b> <code>--global</code> user-wide setting; <code>--list</code> show settings.</p>',
 mis=[('Typing the quotes wrongly.','Use straight quotes around names with spaces.'),('Using a different email than GitHub.','Commits may not link to your profile. Use your GitHub email.'),('Confusing config with login.','Config only labels commits. Sign-in is separate.')],
 ex='Run the four commands with your details, then check the output matches what you typed.',res='The list shows your <code>user.name</code>, <code>user.email</code> and <code>init.defaultbranch=main</code>.',
 q=[('What does user.name do?',['Labels your commits with your name','Logs you in to GitHub','Renames the project'],0,'It is stamped on each commit.'),('Which wins, local or global?',['Local','Global','Neither'],0,'A local setting overrides a global one in that repository.'),('Does user.email authenticate you?',['No, authentication is separate','Yes','Only on Windows'],0,'It is a label. HTTPS login or SSH key authenticates.')],
 sm='You set your name, email and default branch, verified them, and learned that commit identity is not the same as GitHub sign-in.',voc=[('Global / Local','All repos / one repo'),('Authentication','Proving who you are to GitHub'),('SSH key','A key pair used instead of a password')],
 nxt='<b>Module 3 — Creating your first repository.</b> With Git configured, you will create your first project.',
 svg=term(CFG,'Illustration · Git Bash (not a real screenshot)'),fig='Figure 1 · Illustration of the expected output')
ar_ill='رسم توضيحي · Git Bash (ليس لقطة حقيقية)'
E['ar']['1']=dict(basea,les='الدرس 2.1',lt='تثبيت Git وVS Code',other='Installing Git and VS Code',
 obj=['أن تثبّت Git على ويندوز.','أن تثبّت Visual Studio Code.','أن تفتح الطرفية المدمجة وتختار Git Bash.','أن تتحقق من التثبيت بالأمر <code>git --version</code>.'],
 pre='الوحدة 1، وحاسوب ويندوز واتصال بالإنترنت.',intro='قبل أن يعمل أي أمر يجب أن تكون الأدوات على جهازك. هذا الدرس يثبّت الاثنين ثم يتأكد أن Git يستجيب.',
 exp=['<b>تثبيت Git.</b> افتح <code>git-scm.com</code> واختر <b>Download for Windows</b>. شغّل المثبّت. الخيارات الافتراضية آمنة للمبتدئين. يمكنك اختيار Visual Studio Code محررًا افتراضيًا، واختيار <b>main</b> اسمًا للفروع الجديدة إن عرض المثبّت ذلك. اضغط Next حتى Install ثم Finish.','<b>التحقق.</b> افتح <b>Git Bash</b> من قائمة ابدأ ونفّذ <code>git --version</code>. إن ردّ Git برقم إصدار فهو مثبّت.','<b>تثبيت VS Code.</b> افتح <code>code.visualstudio.com</code> ونزّل مثبّت ويندوز وشغّله. أبقِ خيار <b>Add to PATH</b> مفعّلًا.','<b>فتح الطرفية في VS Code.</b> من القائمة <b>Terminal ← New Terminal</b> أو اضغط <code>Ctrl+`</code>. في لوحة الطرفية اضغط السهم بجانب <b>+</b> واختر <b>Git Bash</b>.'],
 ana='تثبيت الأدوات كتجهيز المطبخ قبل الطبخ: لا يوجد طعام بعد، لكن كل وصفة في هذه الدورة تحتاج هذه الأدوات.',
 cmd='<p>نفّذ هذا في Git Bash أو طرفية VS Code. الخيار <code>--version</code> يطلب من البرنامج طباعة إصداره ثم الخروج.</p><code>git --version</code>',
 mis=[('«git is not recognized»','أغلق الطرفية وافتحها من جديد. وإن استمر الخطأ فأعد تشغيل مثبّت Git.'),('فتح PowerShell وتوقع أوامر Bash.','اختر Git Bash من قائمة ملفات تعريف الطرفية.'),('تعطيل Add to PATH عند تثبيت VS Code.','أعد تشغيل المثبّت وفعّله.')],
 ex='ثبّت Git وVS Code، وافتح طرفية داخل VS Code، واختر Git Bash، ونفّذ <code>git --version</code>.',res='تطبع الطرفية سطرًا يبدأ بـ <code>git version</code>.',
 q=[('أي أمر يتحقق من تثبيت Git؟',['git --version','git start','git check'],0,'<code>git --version</code> يطبع الإصدار المثبّت.'),('أي طرفية نستخدم في هذه الدورة؟',['Git Bash','Notepad','Paint'],0,'Git Bash يعطينا الأوامر نفسها على ويندوز.'),('أي اختصار يفتح طرفية في VS Code؟',['Ctrl+`','Ctrl+Z','Alt+F4'],0,'الاختصار Ctrl+` يفتح الطرفية المدمجة ويغلقها.')],
 sm='ثبّتّ Git وVS Code، وفتحت طرفية في VS Code، واخترت Git Bash، وتأكدت أن Git يعمل.',voc=[('الطرفية (Terminal)','نافذة نصية لكتابة الأوامر'),('Git Bash','طرفية Bash تأتي مع Git لويندوز'),('PATH','قائمة المجلدات التي يبحث فيها ويندوز عن البرامج')],
 nxt='<b>الدرس 2.2 — إنشاء حساب GitHub.</b> الأدوات جاهزة. بعده تنشئ بيتك على الإنترنت.',
 svg=E['en']['1']['svg'].replace('Illustration · Git Bash (not a real screenshot)',ar_ill),fig='الشكل 1 · رسم توضيحي للخرج المتوقع')
E['ar']['2']=dict(basea,les='الدرس 2.2',lt='إنشاء حساب GitHub',other='Creating your GitHub account',
 obj=['أن تنشئ حساب GitHub وتوثّقه.','أن تتعرف على لوحة التحكم.','أن تحمي الحساب بالمصادقة الثنائية.','أن تسمّي طرق تسجيل دخول Git إلى GitHub.'],
 pre='الدرس 2.1 وبريد إلكتروني تستطيع فتحه.',intro='حساب GitHub هويتك على الإنترنت. مشاريعك وتاريخك ومعرض أعمالك المستقبلي كلها هناك، لذلك نحميه منذ اليوم الأول.',
 exp=['<b>إنشاء الحساب.</b> افتح <code>github.com</code> واختر <b>Sign up</b>. أدخل بريدك وكلمة سر قوية واسم مستخدم. اختر اسمًا تفتخر بعرضه على صاحب عمل.','<b>توثيق البريد.</b> يرسل GitHub رمزًا إلى بريدك. أدخله لإكمال التسجيل. وقد يُطلب منك حل لغز قصير.','<b>لوحة التحكم.</b> بعد الدخول ترى مستودعاتك ونشاطك واقتراحات. صورتك (أعلى اليمين) تفتح قائمة فيها <b>Your profile</b> و<b>Your repositories</b> و<b>Settings</b>.','<b>الملف الشخصي.</b> أضف صورة ونبذة قصيرة، ولا تكتب فيها معلومات خاصة لا تريدها علنية.','<b>الأمان.</b> استخدم كلمة سر فريدة في مدير كلمات المرور. من <b>Settings ← Password and authentication</b> فعّل <b>المصادقة الثنائية (2FA)</b> بتطبيق مصادقة، واحفظ رموز الاسترداد في مكان آمن.','<b>كيف يسجّل Git دخوله.</b> عبر <b>HTTPS</b> يطلب Git حساب GitHub من نافذة تسجيل دخول ويحفظه في Git Credential Manager (يأتي مع Git لويندوز). وعبر <b>SSH</b> تضيف زوج مفاتيح إلى حسابك. لا تستخدم كلمة سر GitHub ككلمة سر لـ Git في الطرفية. ستجهّز طريقة في الوحدة 5.'],
 ana='حسابك كحساب مصرفي لكودك: كلمة سر قوية وقفل ثانٍ (2FA) يبقيانه لك.',
 cmd='لا توجد أوامر Git هنا. كل الخطوات في المتصفح.',
 mis=[('ضياع رموز استرداد 2FA.','احفظها في مدير كلمات المرور أو اطبعها.'),('استخدام بريد خاص في commits عامة.','لاحقًا تستطيع استخدام عنوان noreply من GitHub (الدرس 2.3).'),('اختيار اسم مستخدم للمزاح.','اختر اسمًا مهنيًا، فهو جزء من روابطك.')],
 ex='أنشئ حسابك، ووثّق البريد، وأضف صورة، وفعّل 2FA.',res='تستطيع فتح ملفك على <code>github.com/your-username</code> وتظهر 2FA مفعّلة في Settings.',
 q=[('لماذا نفعّل 2FA؟',['فحص ثانٍ يحمي الحساب','يجعل Git أسرع','مطلوبة لتثبيت Git'],0,'2FA تمنع الدخول بكلمة سر مسروقة وحدها.'),('أين تعيش مشاريعك على الإنترنت؟',['GitHub','VS Code','Git Bash'],0,'GitHub يستضيف مستودعاتك البعيدة.'),('اذكر طريقة يسجّل بها Git دخوله إلى GitHub.',['مفاتيح SSH','مرفقات البريد','لقطات الشاشة'],0,'HTTPS مع Credential Manager ومفاتيح SSH هما الطريقتان الشائعتان.')],
 sm='أنشأت حساب GitHub وحميته، وعرفت طريقتي الدخول التي يستخدمها Git: HTTPS وSSH.',voc=[('2FA','إثبات ثانٍ للهوية عند الدخول'),('HTTPS / SSH','طريقتان يتصل بهما Git مع GitHub'),('لوحة التحكم (Dashboard)','صفحتك الرئيسية في GitHub')],
 nxt='<b>الدرس 2.3 — إعداد Git لأول مرة.</b> الآن تخبر Git من أنت.',
 svg=E['en']['2']['svg'].replace('your computer','your PC'),fig='الشكل 1 · يثبت Git هويته قبل أن يرفع')
E['ar']['3']=dict(basea,les='الدرس 2.3',lt='إعداد Git لأول مرة',other='First-time Git configuration',
 obj=['أن تضبط الاسم والبريد والفرع الافتراضي.','أن تتحقق من إعداداتك.','أن تشرح الإعداد العام والمحلي.','أن تفرّق بين هوية الـ commit وتسجيل الدخول إلى GitHub.'],
 pre='الدرسان 2.1 و2.2.',intro='كل commit يسجّل من صنعه. لا يستطيع Git تخمين ذلك، فتضبطه مرة واحدة.',
 exp=['<b>اضبط هويتك.</b> نفّذ أول أمرين أدناه ببياناتك. استخدم بريد حساب GitHub، أو عنوان noreply الذي يعرضه GitHub في <b>Settings ← Emails</b>.','<b>الفرع الافتراضي.</b> الأمر الثالث يجعل المستودعات الجديدة تبدأ بفرع اسمه <code>main</code>.','<b>تحقّق.</b> الأمر <code>git config --global --list</code> يطبع كل الإعدادات العامة.','<b>عام ومحلي.</b> الخيار <code>--global</code> يحفظ في ملف المستخدم ويسري على كل المستودعات. وبدونه، داخل مستودع، يكون الإعداد <b>محليًا</b> ويسري هناك فقط. والمحلي يتغلب على العام.','<b>الهوية مقابل الدخول.</b> الاسم والبريد مجرد وسوم على الـ commits، ولا يثبتان من أنت. أما <b>المصادقة</b> (دخول HTTPS أو مفتاح SSH) فهي ما يسمح لك بالرفع. ويمكنك استخدام SSH لاحقًا: الأمر <code>ssh-keygen -t ed25519 -C "you@example.com"</code> ينشئ زوج مفاتيح، ونكمله في الوحدة 5.'],
 ana='الاسم والبريد توقيع على رسالة. يستطيع أي شخص كتابة توقيع، لكن مفتاحك وحده يفتح صندوق البريد.',
 cmd='<code>git config --global user.name "Your Name"</code><br><code>git config --global user.email "you@example.com"</code><br><code>git config --global init.defaultBranch main</code><br><code>git config --global --list</code><p><b>الخيارات:</b> <code>--global</code> إعداد على مستوى المستخدم؛ <code>--list</code> عرض الإعدادات.</p>',
 mis=[('كتابة علامات الاقتباس بشكل خاطئ.','استخدم علامات اقتباس مستقيمة حول الأسماء التي فيها مسافات.'),('استخدام بريد مختلف عن GitHub.','قد لا ترتبط الـ commits بملفك. استخدم بريد GitHub.'),('الخلط بين config وتسجيل الدخول.','الإعداد يضع وسمًا على الـ commits فقط. الدخول أمر منفصل.')],
 ex='نفّذ الأوامر الأربعة ببياناتك، ثم تأكد أن الخرج يطابق ما كتبته.',res='تعرض القائمة <code>user.name</code> و<code>user.email</code> و<code>init.defaultbranch=main</code>.',
 q=[('ماذا يفعل user.name؟',['يضع اسمك على commits','يسجّل دخولك إلى GitHub','يغيّر اسم المشروع'],0,'يُوضع على كل commit.'),('أيهما يتغلب، المحلي أم العام؟',['المحلي','العام','لا أحد'],0,'الإعداد المحلي يتغلب على العام في ذلك المستودع.'),('هل user.email يوثّق هويتك؟',['لا، المصادقة أمر منفصل','نعم','فقط على ويندوز'],0,'هو وسم. دخول HTTPS أو مفتاح SSH هو الذي يوثّق.')],
 sm='ضبطت اسمك وبريدك والفرع الافتراضي، وتحققت منها، وعرفت أن هوية الـ commit ليست تسجيل الدخول إلى GitHub.',voc=[('عام / محلي','كل المستودعات / مستودع واحد'),('المصادقة (Authentication)','إثبات هويتك لـ GitHub'),('مفتاح SSH','زوج مفاتيح يُستخدم بدل كلمة السر')],
 nxt='<b>الوحدة 3 — إنشاء أول مستودع.</b> بعد إعداد Git ستنشئ مشروعك الأول.',
 svg=E['en']['3']['svg'].replace('Illustration · Git Bash (not a real screenshot)',ar_ill),fig='الشكل 1 · رسم توضيحي للخرج المتوقع')
MQ={'en':dict(h='Practical lab 2 · Configure and verify Git',lab='<ol><li>Open Git Bash and run <code>git --version</code>.</li><li>Run the three <code>git config --global</code> commands with your details.</li><li>Run <code>git config --global --list</code>.</li><li>Check each line against what you typed.</li></ol><table><tr><th>Check</th><th>Pass if…</th></tr><tr><td>Version</td><td>Output starts with <code>git version</code></td></tr><tr><td>Identity</td><td>Name and email match your GitHub account</td></tr><tr><td>Branch</td><td><code>init.defaultbranch=main</code> appears</td></tr></table><div class="box b"><b>Evaluation:</b> 3 of 3 checks = pass.</div>',qh='Module 2 quiz (pass mark: 70%)',
 q=[('Which command prints your global settings?',['git config --global --list','git show config','git list'],0,'<code>--list</code> prints the settings.'),('Which tool is the editor with built-in Git?',['VS Code','GitHub','Git Bash'],0,'VS Code includes Git buttons.'),('What should you do with 2FA recovery codes?',['Store them safely','Share them','Delete them'],0,'They restore access if you lose your device.'),('What does --global mean?',['Applies to all your repositories','Applies to one file','Uploads to GitHub'],0,'It saves in your user-level Git file.'),('Does user.name prove who you are?',['No, it is only a label','Yes','Only with 2FA'],0,'Authentication proves identity; name is a label.')]),
 'ar':dict(h='المختبر العملي 2 · اضبط Git وتحقق منه',lab='<ol><li>افتح Git Bash ونفّذ <code>git --version</code>.</li><li>نفّذ أوامر <code>git config --global</code> الثلاثة ببياناتك.</li><li>نفّذ <code>git config --global --list</code>.</li><li>قارن كل سطر بما كتبته.</li></ol><table><tr><th>الفحص</th><th>ينجح إذا…</th></tr><tr><td>الإصدار</td><td>يبدأ الخرج بـ <code>git version</code></td></tr><tr><td>الهوية</td><td>الاسم والبريد يطابقان حساب GitHub</td></tr><tr><td>الفرع</td><td>يظهر <code>init.defaultbranch=main</code></td></tr></table><div class="box b"><b>معيار التقييم:</b> 3 فحوص من 3 = نجاح.</div>',qh='اختبار الوحدة 2 (علامة النجاح: 70%)',
 q=[('أي أمر يطبع إعداداتك العامة؟',['git config --global --list','git show config','git list'],0,'الخيار <code>--list</code> يطبع الإعدادات.'),('أي أداة هي المحرر الذي فيه Git مدمج؟',['VS Code','GitHub','Git Bash'],0,'VS Code فيه أزرار Git.'),('ماذا تفعل برموز استرداد 2FA؟',['تحفظها بأمان','تشاركها','تحذفها'],0,'تعيد لك الدخول إن فقدت جهازك.'),('ماذا يعني --global؟',['يسري على كل مستودعاتك','يسري على ملف واحد','يرفع إلى GitHub'],0,'يُحفظ في ملف Git على مستوى المستخدم.'),('هل user.name يثبت من أنت؟',['لا، هو وسم فقط','نعم','فقط مع 2FA'],0,'المصادقة تثبت الهوية، والاسم وسم.')])}
m.MQ.update({}); 
def extra(l):
    t=b.T[l]; mq=MQ[l]; e=E[l]['1']
    MQ_q=[(a,)+b.shuf(i,o,c)+(w,) for i,(a,o,c,w) in enumerate(mq['q'])]
    mq={**mq,'q':MQ_q}
    q=''.join(f'<div class="qq"><b>{i+1}. {a}</b>'+''.join(f'<label><input type="radio" name="m{i}" data-c="{int(j==c)}" data-w="{w}"> {x}</label>' for j,x in enumerate(o))+'<div class="fb"></div></div>' for i,(a,o,c,w) in enumerate(mq['q']))
    ans=''.join(f'<li>{o[c]} — {w}</li>' for a,o,c,w in mq['q'])
    return f'<section class="lesson"><div class="lessonhead"><div class="k2">{e["mod"]}</div><h1 class="lt">{mq["h"]}</h1></div>{mq["lab"]}<h3>{mq["qh"]}</h3>{q}<h3>{t["H"]["ans"]}</h3><ul>{ans}</ul></section>'
async def main():
    names=['2-1','2-2','2-3','2-lab-quiz']; other={'en':'ar','ar':'en'}
    for l in('en','ar'):
        body=[b.lesson_html(l,{**b.T[l],**E[l][k]}) for k in '123']+[extra(l)]; e=E[l]['1']
        for i,n in enumerate(names):
            nav=''.join(f'<a href="lesson-{names[j]}-{l}.html"><button>{lab}</button></a>' for j,lab in((i-1,'←' if l=='en' else '→'),(i+1,'→' if l=='en' else '←')) if 0<=j<4)
            tools=f'<div class="tools">{nav}<a href="lesson-{n}-{other[l]}.html"><button>{"العربية" if l=="en" else "English"}</button></a><button id="tg">☾ / ☀</button></div>'
            open(f'{O}lesson-{n}-{l}.html','w',encoding='utf8').write(b.page(l,f'<div class="wrap">{tools}{body[i]}</div>{b.JS}'))
        t=b.T[l]
        cover=b.book_body(l).split('<section class="opener">')[0]
        opener=f'<section class="opener"><div class="n">02</div><div class="k2" style="color:#FFB23F">{e["mod"]}</div><h2>{e["modt"]}</h2><p>{e["modd"]}</p></section>'
        open(f'{O}_c{l}.html','w',encoding='utf8').write(b.page(l,cover+opener+'<div class="bgp"></div><div class="wrap print">'+'<div style="break-after:page"></div>'.join(body)+'</div>'))
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page()
        for l in('en','ar'):
            await pg.goto(f'file://{O}_c{l}.html'); await pg.wait_for_timeout(600)
            foot='<div style="width:100%;font:9px sans-serif;color:#5A6280;padding:0 18mm;display:flex;justify-content:space-between"><span>Programming Worlds Academy · Git &amp; GitHub 101</span><span class="pageNumber"></span></div>'
            await pg.pdf(path=f'/home/claude/{l}_m2.pdf',prefer_css_page_size=True,print_background=True,display_header_footer=True,header_template='<span></span>',footer_template=foot)
        await br.close()
    for l in('en','ar'):
        w=PdfWriter(); w.append(f'/home/claude/{l}_m2.pdf'); w.write(f'{O}Git-and-GitHub-101-{l.upper()}_Module02.pdf'); os.remove(f'{O}_c{l}.html')
asyncio.run(main())
