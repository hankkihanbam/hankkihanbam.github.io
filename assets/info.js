// 정보 카드: 화면에 들어오면 한 번만 켜짐(체크·화살표·연표), 숫자는 올라가며 세어짐
(function () {
  var cards = document.querySelectorAll('.ic');
  function count(el) {
    var to = +el.getAttribute('data-to'), from = +(el.getAttribute('data-from') || 0), t0 = null, unit = el.querySelector('small');
    var label = unit ? unit.outerHTML : '';
    function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1200); var v = Math.round(from + (to - from) * (1 - Math.pow(1 - p, 3)));
      el.innerHTML = v + label; if (p < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  if (!('IntersectionObserver' in window)) { cards.forEach(function (c) { c.classList.add('on'); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('on');
      e.target.querySelectorAll('[data-to]').forEach(count);
      io.unobserve(e.target);
    });
  }, { threshold: .35 });
  cards.forEach(function (c) { io.observe(c); });
})();
