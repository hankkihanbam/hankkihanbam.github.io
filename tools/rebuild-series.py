# '한끼한밤 이야기' 목록 상자를 tools/series.json 순서대로 모든 글에 다시 넣기
# 새 화 글을 만들면: series.json에 [파일이름, "N화", "제목"]을 화 순서 자리에 넣고 → python3 tools/rebuild-series.py
# ("글"은 새 채널에 영상이 없는 블로그 전용 글. 화 번호 글 뒤에 둠)
import json, re, os, glob
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = json.load(open('tools/series.json'))
names = {f for f, _, _ in S}
def box(cur):
    li = [f'          <li><strong>{n} · {t}</strong> (지금 읽는 글)</li>' if f == cur else f'          <li><a href="{f}.html">{n} · {t}</a></li>' for f, n, t in S]
    return '<ul>\n' + '\n'.join(li) + '\n        </ul>'
for f, n, t in S:
    p = f'posts/{f}.html'
    if not os.path.exists(p): print('없음', p); continue
    s = open(p).read()
    s, k = re.subn(r'(<h3>한끼한밤 이야기</h3>\s*)<ul>.*?</ul>', lambda m: m.group(1) + box(f), s, 1, re.S)
    s = re.sub(r'<div class="tag">(?:\d+화|글) · ', f'<div class="tag">{n} · ', s, 1)
    open(p, 'w').write(s); print(p, '목록 상자' if k else '목록 상자 없음')
