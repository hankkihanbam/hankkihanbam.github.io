// 방문자 숫자 칸: 페이지를 열 때마다 1번 세고, 오늘·전체 숫자를 맨 아래에 보여 줌 (hitscounter.dev, 한국 시간 기준)
(function () {
  var foot = document.querySelector('footer .wrap');
  if (!foot) return;
  var box = document.createElement('span');
  box.className = 'visits';
  box.innerHTML = '<i>👣</i> 오늘 <b class="v-today">·</b> <span class="sep">|</span> 전체 <b class="v-total">·</b>';
  foot.appendChild(box);
  var url = 'https://hitscounter.dev/api/hit?url=hankkihanbam.github.io&output=json&tz=Asia%2FSeoul';
  fetch(url).then(function (r) { return r.json(); }).then(function (d) {
    box.querySelector('.v-today').textContent = (d.today_hits || 0).toLocaleString('ko-KR');
    box.querySelector('.v-total').textContent = (d.total_hits || 0).toLocaleString('ko-KR');
    box.classList.add('on');
  }).catch(function () { box.remove(); });
})();
