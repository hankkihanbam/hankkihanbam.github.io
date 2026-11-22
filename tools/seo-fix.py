# 검색용 설정 한 번에 넣기 (여러 번 돌려도 안전). 사용: python3 tools/seo-fix.py
import re,glob,json,subprocess,html
B='https://hankkihanbam.github.io'
TITLES={ # 검색 탭 제목(본문 제목 h1은 그대로)
'index.html':'순례자의 한끼한밤 | 산티아고 순례길·포르투갈 음식 이야기',
'posts/01-tteokbokki.html':'떡볶이가 빨개진 이유, 고추와 포르투갈 | 한끼한밤',
'posts/02-castella.html':'카스텔라 유래, 400살 포르투갈 빵 | 한끼한밤',
'posts/03-eggtart.html':'에그타르트 유래, 189년째 비밀 | 한끼한밤',
'posts/04-scallop.html':'순례자 가리비 의미, 천 년 동안 단 이유 | 한끼한밤',
'posts/05-bread.html':"빵 어원, '빵'은 포르투갈 말 | 한끼한밤",
'posts/06-arrow.html':'순례길 노란 화살표, 신부님이 그렸다 | 한끼한밤',
'posts/07-tempura.html':"덴푸라 어원, '덴푸라'는 일본말이 아니다 | 한끼한밤",
'posts/08-fisterra.html':'피스테라 0km, 산티아고 순례길의 진짜 끝 | 한끼한밤',
'posts/camino-01-meals.html':'산티아고 순례길 32일, 오늘 저녁은 뭘 먹지? | 한끼한밤',
'posts/camino-02-albergue.html':'순례길 알베르게, 오늘은 어디서 자지? | 한끼한밤',
'posts/camino-03-pyrenees.html':'순례길 첫날, 피레네를 하루 만에 넘은 날 | 한끼한밤',
'posts/camino-04-meseta.html':'순례길 메세타, 밀밭에 20분 누워 있던 날 | 한끼한밤',
'posts/camino-05-santiago.html':'순례길 32일째, 산티아고 도착과 순례자 증명서 | 한끼한밤',
'posts/camino-tips.html':'산티아고 순례길 준비물·비용, 32일 걷고 정리 | 한끼한밤',
}
def git(fmt,f,first=False):
    out=subprocess.run(['git','log',f'--format={fmt}','--',f],capture_output=True,text=True).stdout.split()
    return (out[-1] if first else out[0]) if out else None
pub={'@type':'Organization','name':'순례자의 한끼한밤','url':B+'/','logo':{'@type':'ImageObject','url':B+'/images/profile.jpg'},
     'sameAs':['https://www.youtube.com/@hankkihanbam','https://www.instagram.com/hankki_hanbam/']}
for p in ['index.html']+sorted(glob.glob('posts/*.html')):
    s=open(p).read()
    url=B+'/' if p=='index.html' else f'{B}/{p}'
    base=B+'/' if p=='index.html' else B+'/posts/'
    def absu(m):
        v=m.group(2)
        if v.startswith('http'): return m.group(0)
        v=re.sub(r'^\.\./','',v); return m.group(1)+B+'/'+v.lstrip('/')+'"'
    s=re.sub(r'(property="og:image" content=")([^"]+)"',absu,s)
    if p in TITLES: s=re.sub(r'<title>.*?</title>','<title>'+html.escape(TITLES[p],quote=False)+'</title>',s,count=1,flags=re.S)
    # 한 번만 넣는 태그 묶음 (다시 돌리면 교체)
    s=re.sub(r'\n  <!-- seo:start -->.*?<!-- seo:end -->','',s,flags=re.S)
    img=re.search(r'property="og:image" content="([^"]+)"',s).group(1)
    desc=re.search(r'name="description" content="([^"]*)"',s).group(1)
    h1=re.sub(r'<[^>]+>','',re.sub(r'<br\s*\/?>',' ',re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1))).strip()
    h1=re.sub(r'\s+',' ',html.unescape(h1))
    if p=='index.html':
        ld={'@context':'https://schema.org','@graph':[{'@type':'WebSite','name':'순례자의 한끼한밤','alternateName':'한끼한밤','url':B+'/','inLanguage':'ko'},dict(pub,**{'@id':B+'/#org'})]}
    else:
        ld={'@context':'https://schema.org','@type':'BlogPosting','headline':h1[:110],'description':html.unescape(desc),
            'image':[img],'datePublished':git('%cI',p,True),'dateModified':git('%cI',p),
            'author':{'@type':'Organization','name':'순례자의 한끼한밤','url':B+'/'},'publisher':pub,
            'mainEntityOfPage':url,'inLanguage':'ko'}
    block=('\n  <!-- seo:start -->\n  <link rel="canonical" href="%s">\n  <meta property="og:url" content="%s">\n'
           '  <meta property="og:site_name" content="순례자의 한끼한밤">\n  <meta property="og:locale" content="ko_KR">\n'
           '  <meta name="twitter:card" content="summary_large_image">\n'
           '  <link rel="alternate" type="application/rss+xml" title="순례자의 한끼한밤" href="%s/feed.xml">\n'
           '  <script type="application/ld+json">%s</script>\n  <!-- seo:end -->')%(url,url,B,json.dumps(ld,ensure_ascii=False))
    s=s.replace('</head>',block+'\n</head>',1)
    open(p,'w').write(s)
print('ok')
