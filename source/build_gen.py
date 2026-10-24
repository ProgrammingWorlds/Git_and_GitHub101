import asyncio, os
import build as b
from playwright.async_api import async_playwright
from pypdf import PdfWriter
O=b.O
def term(lines, cap):
    h=40+22*len(lines); o=f'<svg viewBox="0 0 700 {h}" xmlns="http://www.w3.org/2000/svg" font-family="JetBrains Mono,monospace" font-size="13"><rect width="700" height="{h}" rx="10" fill="#1F1F1F"/><rect width="700" height="26" rx="10" fill="#181818"/><circle cx="16" cy="13" r="4" fill="#FF5F57"/><circle cx="30" cy="13" r="4" fill="#FEBC2E"/><circle cx="44" cy="13" r="4" fill="#28C840"/><text x="350" y="17" fill="#9D9D9D" font-size="11" text-anchor="middle" font-family="sans-serif">{cap}</text>'
    for i,s in enumerate(lines):
        c='#FFB23F' if s.startswith('$') else '#E8E8E8'
        o+=f'<text x="18" y="{54+22*i}" fill="{c}" xml:space="preserve">{s.replace("&","&amp;").replace("<","&lt;")}</text>'
    return o+'</svg>'
def pre(s): return '<pre style="direction:ltr;text-align:left;background:#0B1430;color:#fff;border-radius:12px;padding:12px 16px;font:500 12.5px/1.6 \'JetBrains Mono\',monospace;white-space:pre-wrap;margin:8px 0">'+s.replace('&','&amp;').replace('<','&lt;')+'</pre>'
def extra(l,MQ,E):
    t=b.T[l]; mq=MQ[l]; e=E[l]['1']
    def sh(i,o,c):
        k=[1,2,0,2,1,0][i%6]%len(o); idx=[(j+k)%len(o) for j in range(len(o))]
        return [o[j] for j in idx], idx.index(c)
    qs=[]
    for i,(a,o,c,w) in enumerate(mq['q']):
        o2,c2=sh(i,o,c); qs.append((a,o2,c2,w))
    mq={**mq,'q':qs}
    q=''.join(f'<div class="qq"><b>{i+1}. {a}</b>'+''.join(f'<label><input type="radio" name="m{i}" data-c="{int(j==c)}" data-w="{w}"> {x}</label>' for j,x in enumerate(o))+'<div class="fb"></div></div>' for i,(a,o,c,w) in enumerate(mq['q']))
    ans=''.join(f'<li>{o[c]} — {w}</li>' for a,o,c,w in mq['q'])
    return f'<section class="lesson"><div class="lessonhead"><div class="k2">{e["mod"]}</div><h1 class="lt">{mq["h"]}</h1></div>{mq["lab"]}<h3>{mq["qh"]}</h3>{q}<h3>{t["H"]["ans"]}</h3><ul>{ans}</ul></section>'
async def run(num,E,MQ):
    names=[f'{num}-1',f'{num}-2',f'{num}-3',f'{num}-lab-quiz']; other={'en':'ar','ar':'en'}; n2=f'{num:02d}'
    for l in('en','ar'):
        body=[b.lesson_html(l,{**b.T[l],**E[l][k]}) for k in '123']+[extra(l,MQ,E)]; e=E[l]['1']
        for i,n in enumerate(names):
            nav=''.join(f'<a href="lesson-{names[j]}-{l}.html"><button>{lab}</button></a>' for j,lab in((i-1,'←' if l=='en' else '→'),(i+1,'→' if l=='en' else '←')) if 0<=j<4)
            tools=f'<div class="tools">{nav}<a href="lesson-{n}-{other[l]}.html"><button>{"العربية" if l=="en" else "English"}</button></a><button id="tg">☾ / ☀</button></div>'
            open(f'{O}lesson-{n}-{l}.html','w',encoding='utf8').write(b.page(l,f'<div class="wrap">{tools}{body[i]}</div>{b.JS}'))
        cover=b.book_body(l).split('<section class="opener">')[0]
        op=f'<section class="opener"><div class="n">{n2}</div><div class="k2" style="color:#FFB23F">{e["mod"]}</div><h2>{e["modt"]}</h2><p>{e["modd"]}</p></section>'
        open(f'{O}_g{l}.html','w',encoding='utf8').write(b.page(l,cover+op+'<div class="bgp"></div><div class="wrap print">'+'<div style="break-after:page"></div>'.join(body)+'</div>'))
    async with async_playwright() as p:
        br=await p.chromium.launch(); pg=await br.new_page()
        for l in('en','ar'):
            await pg.goto(f'file://{O}_g{l}.html'); await pg.wait_for_timeout(600)
            foot='<div style="width:100%;font:9px sans-serif;color:#5A6280;padding:0 18mm;display:flex;justify-content:space-between"><span>Programming Worlds Academy · Git &amp; GitHub 101</span><span class="pageNumber"></span></div>'
            await pg.pdf(path=f'/home/claude/{l}_g.pdf',prefer_css_page_size=True,print_background=True,display_header_footer=True,header_template='<span></span>',footer_template=foot)
        await br.close()
    for l in('en','ar'):
        w=PdfWriter(); w.append(f'/home/claude/{l}_g.pdf'); w.write(f'{O}Git-and-GitHub-101-{l.upper()}_Module{n2}.pdf'); os.remove(f'{O}_g{l}.html')
