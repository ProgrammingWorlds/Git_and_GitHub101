import asyncio, os, html
import build as b
from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter
from appendix_data import *
import platform_build as pb
O=b.O
FOOT='<div style="width:100%;font:9px sans-serif;color:#5A6280;padding:0 18mm;display:flex;justify-content:space-between"><span>Programming Worlds Academy · Git &amp; GitHub 101</span><span class="pageNumber"></span></div>'
def cover(l): return b.book_body(l).split('<section class="opener">')[0]
def opener(l,n,k,t,d): return f'<section class="opener"><div class="n">{n}</div><div class="k2" style="color:#FFB23F">{k}</div><h2>{t}</h2><p>{d}</p></section>'
def toc(l):
    en=l=='en'; s=f'<section class="lesson"><div class="lessonhead"><div class="k2">{"CONTENTS" if en else "المحتويات"}</div><h1 class="lt">{"Table of contents" if en else "فهرس المحتويات"}</h1></div>'
    s+=f'<p>{"Each module starts on its own opener page. Page numbers restart inside each module and are shown in that module footer." if en else "تبدأ كل وحدة بصفحة افتتاحية خاصة بها. ترقيم الصفحات يبدأ من جديد داخل كل وحدة ويظهر في تذييل الوحدة."}</p>'
    for m in range(1,13):
        s+=f'<h3>{"Module" if en else "الوحدة"} {m}. {MODS[l][m-1]}</h3><ul>'
        for k in '123': s+=f'<li>{m}.{k} {pb.h1(f"lesson-{m}-{k}-{l}.html")}</li>'
        s+=f'<li>{m}.4 {pb.LAB[l]}</li></ul>'
    s+=f'<h3>{"Resources" if en else "مصادر"}</h3><ul>'+''.join(f'<li>{t}</li>' for _,t in pb.EXTRA[l])+'</ul></section>'
    return s
def about(l):
    en=l=='en'
    return f'''<section class="lesson"><div class="lessonhead"><div class="k2">{"BEFORE YOU START" if en else "قبل أن تبدأ"}</div><h1 class="lt">{"About this course" if en else "عن هذا الكورس"}</h1></div>
<h3>{"Who it is for" if en else "لمن هذا الكورس"}</h3><p>{"Beginners who have never used Git. You need a Windows computer and an internet connection." if en else "للمبتدئين الذين لم يستخدموا Git من قبل. تحتاج حاسوب Windows واتصالًا بالإنترنت."}</p>
<h3>{"How the course works" if en else "كيف يعمل الكورس"}</h3><ul><li>{"12 modules, each with 3 lessons, a practical lab and a 5-question quiz (pass mark 70%)." if en else "12 وحدة، في كل وحدة 3 دروس ومختبر عملي واختبار من 5 أسئلة (علامة النجاح 70%)."}</li><li>{"You practise on a project called my-first-project, then build a portfolio website." if en else "تتدرب على مشروع اسمه my-first-project ثم تبني موقع Portfolio."}</li><li>{"Commands run in Git Bash; the VS Code equivalents are shown where they exist." if en else "تُنفَّذ الأوامر في Git Bash، وتُعرض مكافئات VS Code حيث وُجدت."}</li><li>{"Figures are labeled illustrations, not real screenshots." if en else "الأشكال رسومات توضيحية معنونة، وليست لقطات حقيقية."}</li></ul>
<h3>{"Conventions" if en else "الاصطلاحات"}</h3><p>{"Code and commands are always written left to right and in a monospaced font. Git terms stay in English in the Arabic edition." if en else "الكود والأوامر تُكتب دائمًا من اليسار إلى اليمين بخط أحادي المسافة. وتبقى مصطلحات Git بالإنجليزية في النسخة العربية."}</p></section>'''
async def pdf(pg,body,out,l,foot=True):
    open(f'/home/claude/_b_{l}.html','w',encoding='utf8').write(b.page(l,body))
    await pg.goto(f'file:///home/claude/_b_{l}.html'); await pg.wait_for_timeout(500)
    await pg.pdf(path=out,prefer_css_page_size=True,print_background=True,display_header_footer=foot,header_template='<span></span>',footer_template=FOOT if foot else '<span></span>')
async def main():
    # assets must resolve: write temp html next to assets via symlink
    if not os.path.exists('/home/claude/assets'): os.symlink(O+'assets','/home/claude/assets')
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page()
        for l in('en','ar'):
            en=l=='en'; B=pb.appendix_bodies(l)
            parts=[B[k] for k in('cheatsheet','glossary','troubleshooting','final-project','screenshots')]
            wrapp=lambda x:'<section class="lesson">'+x+'</section>'
            body=cover(l)+opener(l,'+',"APPENDICES" if en else "الملاحق","Resources" if en else "مصادر","Cheat sheet, glossary, troubleshooting, final project and screenshot checklist." if en else "ورقة الأوامر والمصطلحات وحل المشاكل والمشروع النهائي وقائمة اللقطات.")+'<div class="bgp"></div><div class="wrap print">'+'<div style="break-after:page"></div>'.join(wrapp(x) for x in parts)+'</div>'
            await pdf(pg,body,f'/home/claude/{l}_app.pdf',l)
            await pdf(pg,'<div class="wrap print">'+wrapp(B['cheatsheet'])+'</div>',f'{O}Git-Cheat-Sheet-{l.upper()}.pdf',l)
            body=cover(l)+'<div class="bgp"></div><div class="wrap print">'+toc(l)+'<div style="break-after:page"></div>'+about(l)+'</div>'
            await pdf(pg,body,f'/home/claude/{l}_front.pdf',l)
            w=PdfWriter(); front=PdfReader(f'/home/claude/{l}_front.pdf'); w.append(front); 
            w.add_outline_item('Cover' if en else 'الغلاف',0)
            w.add_outline_item('Contents' if en else 'المحتويات',1)
            for m in range(1,13):
                r=PdfReader(f'{O}Git-and-GitHub-101-{l.upper()}_Module{m:02d}.pdf'); st=len(w.pages)
                w.append(r,pages=(1,len(r.pages)))
                w.add_outline_item(f'{"Module" if en else "الوحدة"} {m}. {MODS[l][m-1]}',st)
            ra=PdfReader(f'/home/claude/{l}_app.pdf'); st=len(w.pages); w.append(ra,pages=(1,len(ra.pages))); w.add_outline_item('Resources' if en else 'مصادر',st)
            w.add_metadata({'/Title':'Git & GitHub 101 — Programming Worlds Academy','/Author':'Programming Worlds Academy'})
            w.write(f'{O}Git-and-GitHub-101-{l.upper()}_Full.pdf'); print(l,len(w.pages),'pages')
        await br.close()
asyncio.run(main())
