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
