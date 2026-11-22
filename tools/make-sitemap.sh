#!/bin/zsh
# 사이트맵 다시 만들기: 사이트 폴더에서 zsh tools/make-sitemap.sh
cd "${0:A:h}/.."
B=https://hankkihanbam.github.io
{
echo '<?xml version="1.0" encoding="UTF-8"?>'
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
for f in index.html posts/*.html; do
  d=$(git log -1 --format=%cs -- "$f" 2>/dev/null); [ -z "$d" ] && d=$(date +%F)
  u="$B/$f"; [ "$f" = index.html ] && u="$B/"
  echo "  <url><loc>$u</loc><lastmod>$d</lastmod></url>"
done
echo '</urlset>'
} > sitemap.xml
printf 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' "$B" > robots.txt
echo "사이트맵 $(grep -c '<url>' sitemap.xml)개 주소"

# 네이버용 RSS(새 글 알림) 만들기
python3 - <<'PY'
import re,glob,json,html,email.utils,datetime
B='https://hankkihanbam.github.io'; items=[]
for p in glob.glob('posts/*.html'):
    s=open(p).read(); m=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
    if not m: continue
    d=json.loads(m.group(1)); t=datetime.datetime.fromisoformat(d['datePublished'])
    items.append((t,d))
items.sort(key=lambda x:x[0],reverse=True)
e=lambda x:html.escape(x,quote=False)
out=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0"><channel>',
 f'<title>순례자의 한끼한밤</title><link>{B}/</link><description>순례자에게, 한 끼와 하룻밤을. 산티아고 순례길·포르투갈·음식의 역사 이야기</description><language>ko</language>']
for t,d in items:
    out.append(f'<item><title>{e(d["headline"])}</title><link>{d["mainEntityOfPage"]}</link><guid>{d["mainEntityOfPage"]}</guid><description>{e(d["description"])}</description><pubDate>{email.utils.format_datetime(t)}</pubDate></item>')
out.append('</channel></rss>')
open('feed.xml','w').write('\n'.join(out)+'\n'); print('RSS',len(items),'개 글')
PY
