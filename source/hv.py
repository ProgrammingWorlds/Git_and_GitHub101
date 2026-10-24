def vsc(rows, cap, calls=()):
    h=70+24*len(rows)+40
    o=f'<svg dir="ltr" viewBox="0 0 700 {h}" xmlns="http://www.w3.org/2000/svg" font-family="Manrope,sans-serif" font-size="12"><rect width="700" height="{h}" rx="10" fill="#1F1F1F"/><rect width="700" height="24" rx="10" fill="#181818"/><text x="350" y="16" fill="#9D9D9D" font-size="11" text-anchor="middle">{cap}</text><rect y="24" width="44" height="{h-24-22}" fill="#181818"/><rect x="44" y="24" width="330" height="{h-24-22}" fill="#181818"/><text x="60" y="48" fill="#BBB" font-size="11" font-weight="700">SOURCE CONTROL</text><rect x="60" y="58" width="300" height="26" rx="3" fill="#313131" stroke="#0078D4"/><text x="70" y="75" fill="#9D9D9D" font-family="JetBrains Mono,monospace">Message</text><rect x="60" y="90" width="300" height="24" rx="3" fill="#0078D4"/><text x="210" y="106" fill="#fff" text-anchor="middle" font-weight="700">Commit</text>'
    for i,(n,b) in enumerate(rows):
        y=140+24*i
        o+=f'<text x="76" y="{y}" fill="#E8E8E8">{n}</text><text x="340" y="{y}" fill="#E2C08D" font-weight="700" text-anchor="end">{b}</text>'
    o+=f'<rect y="{h-22}" width="700" height="22" fill="#0078D4"/><text x="12" y="{h-7}" fill="#fff" font-weight="700">main</text>'
    for i,(x,y,nn) in enumerate(calls):
        o+=f'<circle cx="{x}" cy="{y}" r="11" fill="#FFB23F"/><text x="{x}" y="{y+4}" text-anchor="middle" font-family="JetBrains Mono,monospace" font-weight="700" fill="#0B1430">{nn}</text>'
    return o+'</svg>'
def tl(branches, cap=''):
    return branches
