# 인스타 캐러셀(정보 카드) → 블로그 글 만들기
# 사용: python3 tools/make-card-post.py <설정.json>
# 설정 예:
# {"slug":"card-01-packing", "slides":"~/Documents/한끼한밤/인스타/결과/캐러셀01_준비물",
#  "title":"포르투갈길 준비물, 이것만 챙기세요", "desc":"검색용 한 줄 설명",
#  "lead":"첫 문장", "body":["본문 문단", "..."], "points":["장마다 한 줄 요약", "..."],
#  "alts":["1장 그림 설명", "..."], "en":"영어 한 줄", "ig":"https://www.instagram.com/p/...",
#  "summary":"홈 목록 한 줄", "date":"2026년 11월"}
# 하는 일: 장 그림을 900x1125로 줄여(위치정보 없음) assets/img/<slug>-N.jpg 로 저장,
#          posts/<slug>.html 생성, tools/posts.json 맨 앞에 추가(cat: food/camino/portugal, 기본 camino) → build-site.py로 홈·이어서 읽기 갱신.
import json, os, re, sys, glob, subprocess, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NEWCH = 'https://www.youtube.com/channel/UC54aWAuI4aS1uYWHjAnIY-w'
FF = os.path.expanduser('~/Documents/한끼한밤/작업도구/영상제작/node_modules/@remotion/compositor-darwin-x64')
e = lambda x: html.escape(x, quote=True)

cfg = json.load(open(sys.argv[1]))
slug = cfg['slug']
src = os.path.expanduser(cfg['slides'])
files = sorted(glob.glob(os.path.join(src, '*.jpg')), key=lambda f: int(re.sub(r'\D', '', os.path.basename(f)) or 0))
assert files, '장 그림이 없음: ' + src
imgs = []
for i, f in enumerate(files, 1):
    out = f'assets/img/{slug}-{i}.jpg'
    subprocess.run([FF + '/ffmpeg', '-y', '-loglevel', 'error', '-i', f, '-map_metadata', '-1',
                    '-vf', 'scale=900:-2', '-q:v', '4', out], check=True, env={**os.environ, 'DYLD_LIBRARY_PATH': FF})
    imgs.append(out)
alts = cfg.get('alts') or []

def alt(i):
    return e(alts[i] if i < len(alts) else f"{cfg['title']} {i+1}장")

# 다른 카드 글 목록 (만든 순서)
cards = []
for p in sorted(glob.glob('posts/card-*.html')):
    s = open(p).read()
    t = re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)
    cards.append((os.path.basename(p)[:-5], re.sub(r'<[^>]+>', ' ', t).replace('  ', ' ').strip()))
if slug not in [c[0] for c in cards]:
    cards.append((slug, cfg['title']))

def series(cur):
    li = []
    for f, t in cards:
        li.append(f'          <li><strong>{e(t)}</strong> (지금 읽는 글)</li>' if f == cur else f'          <li><a href="{f}.html">{e(t)}</a></li>')
    return '<ul>\n' + '\n'.join(li) + '\n        </ul>'

deckimgs = '\n'.join(f'            <img src="../{p}" width="900" height="1125" alt="{alt(i)}"' + (' fetchpriority="high">' if i == 0 else ' loading="lazy">') for i, p in enumerate(imgs))
points = '\n'.join(f'          <li><span class="y">{i}</span><p>{e(t)}</p></li>' for i, t in enumerate(cfg.get('points', []), 1))
body = '\n'.join(f'      <p>{e(t)}</p>' for t in cfg.get('body', []))
tmpl = open('posts/05-bread.html').read()
head = tmpl.split('<!-- seo:start -->')[0]
head = re.sub(r'<title>.*?</title>', f"<title>{e(cfg['title'])} | 한끼한밤</title>", head, 1, re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(cfg['desc']), head, 1)
head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e(cfg['title']), head, 1)
head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(cfg['lead']), head, 1)
head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + 'https://hankkihanbam.github.io/' + imgs[0], head, 1)
foot = tmpl[tmpl.index('  <footer>'):]
foot = foot.replace('<script src="../assets/info.js" defer></script>', '<script src="../assets/info.js" defer></script>\n  <script src="../assets/deck.js" defer></script>')
foot = foot.replace('그림: 순례자의 한끼한밤 (AI로 그린 유화)', '그림: 순례자의 한끼한밤 (AI로 그린 유화, 글자는 직접)')

page = f'''{head}</head>
<body>
  <a class="skip" href="#main">본문으로 건너뛰기</a>
  <header class="top">
    <div class="wrap">
      <a class="brand" href="../"><img src="../images/profile.jpg" alt="">순례자의 한끼한밤</a>
      <nav class="nav" aria-label="주 메뉴">
        <a href="../#stories">모든 이야기</a>
        <a href="{NEWCH}" target="_blank" rel="noopener">유튜브</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="article-hero">
      <div class="wrap" data-enter>
        <div>
          <div class="tag">정보 카드</div>
          <h1>{e(cfg['title'])}</h1>
          <div class="meta">순례자의 한끼한밤 · {e(cfg.get('date', ''))} · 카드 {len(imgs)}장</div>
        </div>
        <div class="deck">
          <div class="deck-track" tabindex="0" aria-label="카드 {len(imgs)}장, 옆으로 넘겨 보기">
{deckimgs}
          </div>
          <div class="deck-nav">
            <button class="deck-btn deck-prev" type="button" aria-label="이전 카드">◀</button>
            <div class="deck-mid"><span class="deck-count">1 / {len(imgs)}</span><span class="deck-dots"></span></div>
            <button class="deck-btn deck-next" type="button" aria-label="다음 카드">▶</button>
          </div>
        </div>
      </div>
    </section>

    <article class="prose">
      <p class="lead">{e(cfg['lead'])}</p>
{body}

      <div class="ic">
        <p class="ic-head">한눈에 정리</p>
        <ol class="ic-steps">
{points}
        </ol>
      </div>

      <div class="cta-row"><a class="btn" href="{e(cfg['ig'])}" target="_blank" rel="noopener">인스타그램에서 보기 <span class="arr">→</span></a></div>

      <div class="box en">
        <h3>For pilgrims passing by</h3>
        <p>{e(cfg['en'])}</p>
      </div>

      <div class="box">
        <h3>이어서 읽기</h3>
        <ul></ul>
      </div>

      <p class="ending">🕯️ 오늘 밤 이야기는 여기까지.<br>{e(cfg.get('ending', '필요할 때 다시 볼 수 있게 저장해 두세요.'))}</p>
    </article>
  </main>

{foot}'''
open(f'posts/{slug}.html', 'w').write(page)

# 홈·글 연결은 tools/posts.json + build-site.py가 함 (2026-11-25 새 구성)
P = json.load(open('tools/posts.json'))
if not any(x['file'] == slug for x in P['posts']):
    import datetime
    P['posts'].insert(0, {"file": slug, "cat": cfg.get('cat', 'camino'), "kind": "card", "len": f"{len(imgs)}장",
        "date": cfg.get('day', datetime.date.today().isoformat()), "title": cfg['title'], "sub": cfg.get('summary', ''),
        "thumb": f"{slug}-1.jpg"})
    json.dump(P, open('tools/posts.json', 'w'), ensure_ascii=False, indent=2)
subprocess.run(['python3', 'tools/build-site.py'], check=True)
print('만듦:', f'posts/{slug}.html', len(imgs), '장')
