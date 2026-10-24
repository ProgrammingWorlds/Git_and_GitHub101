import os,re,asyncio,glob,json
from playwright.async_api import async_playwright
from pypdf import PdfReader
O='/mnt/user-data/outputs/git-101-course/'
res={}
htmls=sorted(glob.glob(O+'*.html')); res['html_pages']=len(htmls)
bad=[]
for f in htmls:
    h=open(f,encoding='utf8').read()
    for m in re.findall(r'(?:href|src)="([^"#:]+?)(?:#[^"]*)?"',h):
        if m.startswith(('http','mailto','data')): continue
        if not os.path.exists(O+m): bad.append((os.path.basename(f),m))
res['broken_links']=sorted(set(bad))[:20]
# sections per lesson
cnt=set()
for m in range(1,13):
    for k in '123':
        for l in('en','ar'):
            h=open(f'{O}lesson-{m}-{k}-{l}.html',encoding='utf8').read(); cnt.add(h.count('<h3>'))
res['h3_per_lesson_values']=sorted(cnt)
res['pdfs']={os.path.basename(p):len(PdfReader(p).pages) for p in sorted(glob.glob(O+'*.pdf'))}
async def main():
    errs={};ovf=[]
    async with async_playwright() as p:
        br=await p.chromium.launch()
        ctx=await br.new_context(viewport={'width':390,'height':800}); pg=await ctx.new_page()
        cur=[]
        pg.on('pageerror',lambda e:cur.append(str(e))); pg.on('console',lambda m: cur.append(m.text) if m.type=='error' else None)
        for f in htmls:
            cur.clear(); await pg.goto('file://'+f); await pg.wait_for_timeout(120)
            if cur: errs[os.path.basename(f)]=list(cur)[:2]
            w=await pg.evaluate('document.documentElement.scrollWidth')
            if w>392: ovf.append((os.path.basename(f),w))
        await br.close()
    res['js_errors']=errs; res['mobile_horizontal_overflow']=ovf
asyncio.run(main())
print(json.dumps(res,ensure_ascii=False,indent=1))
