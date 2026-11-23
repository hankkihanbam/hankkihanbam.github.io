// 정보 카드(인스타 캐러셀) 넘겨 보기: 손가락으로 밀거나 ◀ ▶ 버튼, 키보드 화살표
document.querySelectorAll('.deck').forEach(function (deck) {
  var track = deck.querySelector('.deck-track');
  var slides = track.children, n = slides.length;
  var prev = deck.querySelector('.deck-prev'), next = deck.querySelector('.deck-next');
  var count = deck.querySelector('.deck-count'), dots = deck.querySelector('.deck-dots');
  for (var i = 0; i < n; i++) dots.appendChild(document.createElement('i'));
  function cur() { return Math.round(track.scrollLeft / track.clientWidth); }
  function go(i) { track.scrollTo({ left: Math.max(0, Math.min(n - 1, i)) * track.clientWidth, behavior: 'smooth' }); }
  function paint() {
    var i = cur();
    count.textContent = (i + 1) + ' / ' + n;
    prev.disabled = i <= 0; next.disabled = i >= n - 1;
    [].forEach.call(dots.children, function (d, k) { d.className = k === i ? 'on' : ''; });
  }
  prev.addEventListener('click', function () { go(cur() - 1); });
  next.addEventListener('click', function () { go(cur() + 1); });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(cur() + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur() - 1); }
  });
  var t; track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(paint, 60); }, { passive: true });
  addEventListener('resize', paint);
  paint();
});
