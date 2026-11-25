# 블로그 홈·글 사이 연결을 tools/posts.json 하나로 다시 만들기
# 사용: python3 tools/build-site.py   (그다음 python3 tools/seo-fix.py && zsh tools/make-sitemap.sh)
# 하는 일
#  1) index.html 본문을 posts.json 순서(새 글 먼저)대로 새로 씀 — 주제(cats)별 목록, 글이 없는 주제는 숨김
#  2) 각 글: 맨 위 작은 표시 = "주제 · 형식"(주제를 누르면 홈 그 주제로), 위 메뉴, 글 끝 '같은 주제의 다른 글' 상자
import json, os, re, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
YT = 'https://www.youtube.com/channel/UC54aWAuI4aS1uYWHjAnIY-w'
IG = 'https://www.instagram.com/hankki_hanbam/'
D = json.load(open('tools/posts.json'))
CATS = {c['id']: c for c in D['cats']}
KINDS = D['kinds']
POSTS = [p for p in D['posts'] if os.path.exists(f"posts/{p['file']}.html")]
e = lambda x: html.escape(x, quote=True)

def kind(p):
    k = KINDS[p['kind']]
    if p['kind'] == 'long' and p.get('len'): k = f"{p['len']} 영상"
    if p['kind'] == 'card' and p.get('len'): k = f"정보 카드 {p['len']}"
    return k

def day(p):
    d = datetime.date.fromisoformat(p['date']); return f'{d.month}월 {d.day}일'

def row(p, pre=''):
    return (f'''          <a class="r" href="{pre}posts/{p['file']}.html">
            <img class="r-img" src="{pre}assets/img/{p['thumb']}" width="900" height="1125" loading="lazy" alt="">
            <span class="r-txt"><b>{e(p['title'])}</b><small>{e(p['sub'])}</small><span class="r-meta"><span class="k k-{p['kind']}">{kind(p)}</span>{day(p)}</span></span>
          </a>''')

# ── 1) 홈 ──
idx = open('index.html').read()
head = idx[:idx.index('<body')]
cnt = {c: sum(1 for p in POSTS if p['cat'] == c) for c in CATS}
shown = [c for c in D['cats'] if cnt[c['id']]]
new = POSTS[0]
jump = '\n'.join(f'''          <a href="#{c['id']}"><b>{e(c['name'])}</b><span>{cnt[c['id']]}편</span></a>''' for c in shown)
navs = '\n'.join(f'''        <a href="#{c['id']}">{e(c['name'].split()[-1] if c['id'] != 'food' else '음식')}</a>''' for c in shown)
topics = []
for c in shown:
    rows = '\n'.join(row(p) for p in POSTS if p['cat'] == c['id'])
    topics.append(f'''      <section class="topic" id="{c['id']}" aria-labelledby="{c['id']}-h">
        <div class="topic-head">
          <h2 id="{c['id']}-h">{e(c['name'])}</h2>
          <p>{e(c['desc'])}</p>
        </div>
        <div class="rows">
{rows}
        </div>
      </section>''')
about = next((p for p in POSTS if p['cat'] == 'about'), None)
about_link = f'<a class="btn ghost" href="posts/{about["file"]}.html">채널 소개 카드 보기 <span class="arr">→</span></a>' if about else ''

body = f'''<body class="home">
  <a class="skip" href="#main">본문으로 건너뛰기</a>

  <header class="top">
    <div class="wrap">
      <a class="brand" href="./"><img src="images/profile.jpg" alt="">순례자의 한끼한밤</a>
      <nav class="nav" aria-label="주 메뉴">
{navs}
        <a href="#about">소개</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="h-intro">
      <div class="wrap h-grid">
        <div class="h-hello">
          <h1>순례자에게,<br><em>한 끼</em>와 하룻밤을</h1>
          <p>2025년 산티아고 순례길 800km를 32일 동안 걸었습니다. 그 길에서 먹은 한 끼와 묵은 하룻밤, 우리가 매일 먹는 음식에 담긴 이야기를 영상과 글로 나눕니다.</p>
          <nav class="jump" aria-label="주제 바로가기">
{jump}
            <a href="#about"><b>처음 오셨나요?</b><span>소개</span></a>
          </nav>
        </div>
        <div class="h-new">
          <h2>새로 올라온 글</h2>
          <a class="feat" href="posts/{new['file']}.html">
            <img src="assets/img/{new['thumb']}" width="900" height="1125" fetchpriority="high" alt="">
            <span class="feat-txt"><span class="r-meta"><span class="k k-{new['kind']}">{kind(new)}</span>{day(new)}</span><b>{e(new['title'])}</b><small>{e(new['sub'])}</small><span class="go">읽기 <span class="arr">→</span></span></span>
          </a>
        </div>
      </div>
    </section>

    <div class="wrap topics" id="topics">
{chr(10).join(topics)}
    </div>

    <section class="about" id="about" aria-labelledby="about-h">
      <div class="wrap about-grid">
        <img class="about-img" src="assets/img/art-porto.jpg" width="1672" height="941" loading="lazy" alt="밤의 포르투 도루강 강변, 불 켜진 창문과 강 위의 나무 돛배를 그린 유화">
        <div>
          <h2 id="about-h">처음 오셨나요?</h2>
          <p>2025년 여름, 산티아고 순례길 프랑스길을 32일 동안 걸었습니다. 매일 저녁 처음 보는 사람들과 한 식탁에 앉았고, 낯선 알베르게 침대에서 잠들었어요.</p>
          <p>언젠가 포르투에 순례자를 위한 식당과 숙소를 여는 게 꿈입니다. 그때까지는 길과 음식에 얽힌 이야기를 한 편씩 꺼내 놓을게요.</p>
          <dl class="when">
            <div><dt>월·수·금</dt><dd>1분 영상</dd></div>
            <div><dt>화·목</dt><dd>인스타 정보 카드</dd></div>
            <div><dt>영상이 올라온 날</dt><dd>여기에 글로 정리</dd></div>
          </dl>
          <div class="actions">
            <a class="btn" href="{YT}" target="_blank" rel="noopener">유튜브 구독하기 <span class="arr">→</span></a>
            <a class="btn ghost" href="{IG}" target="_blank" rel="noopener">인스타그램</a>
            {about_link}
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <span>🕯️ 순례자의 한끼한밤 · Hankki Hanbam</span>
      <span><a href="{YT}" target="_blank" rel="noopener">YouTube</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></span>
      <span class="credit">그림: 순례자의 한끼한밤 (AI로 그린 유화) · 사진: 순례길에서 직접 찍음</span>
    </div>
  </footer>

  <script src="assets/counter.js" defer></script>
</body>
</html>
'''
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + '2025년 산티아고 순례길 800km를 32일 동안 걸은 사람이 나누는 음식의 역사와 순례길 이야기. 떡볶이·빵의 뿌리부터 순례길 음식, 포르투갈길 준비물까지 영상과 글로.', head, 1)
if 'home.css' not in head:
    head = head.replace('<link rel="stylesheet" href="paper.css?v=8">', '<link rel="stylesheet" href="paper.css?v=8">\n  <link rel="stylesheet" href="home.css?v=1">')
open('index.html', 'w').write(head + body)

# ── 2) 글마다 ──
for p in POSTS:
    f = f"posts/{p['file']}.html"; s = open(f).read()
    c = CATS.get(p['cat'])
    label = (f'<a href="../#{c["id"]}">{e(c["name"])}</a>' if c else '<a href="../#about">채널 소개</a>') + f' · {kind(p)}'
    s = re.sub(r'(<section class="article-hero">.*?<div class="tag">).*?(</div>)', lambda m: m.group(1) + label + m.group(2), s, 1, re.S)
    s = re.sub(r'<nav class="nav" aria-label="주 메뉴">.*?</nav>', lambda m: '<nav class="nav" aria-label="주 메뉴">\n        <a href="../#topics">모든 글</a>\n        <a href="' + YT + '" target="_blank" rel="noopener">유튜브</a>\n      </nav>', s, 1, re.S)
    same = [q for q in POSTS if q is not p and q['cat'] == p['cat']]
    other = [q for q in POSTS if q is not p and q['cat'] != p['cat'] and q['cat'] != 'about']
    pick = (same + other)[:3]
    title = '같은 주제의 다른 글' if same else '다른 이야기'
    li = '\n'.join(f'''          <li><a href="{q['file']}.html">{e(q['title'])}</a> <span class="li-k">{kind(q)}</span></li>''' for q in pick)
    box = f'''<div class="box related">
        <h3>{title}</h3>
        <ul>
{li}
        </ul>
        <p class="all"><a href="../#topics">모든 글 보기 →</a></p>
      </div>'''
    s, n = re.subn(r'<div class="box(?: related)?">\s*<h3>(?:한끼한밤 이야기|함께 읽기|정보 카드|같은 주제의 다른 글|다른 이야기)</h3>.*?</div>', lambda m: box, s, 1, re.S)
    if not n:
        s = s.replace('      <p class="ending">', box + '\n\n      <p class="ending">', 1)
    open(f, 'w').write(s)
print('홈:', len(POSTS), '편 /', ', '.join(f"{c['name']} {cnt[c['id']]}" for c in shown))
