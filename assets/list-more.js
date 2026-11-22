// 홈 이야기 목록: data-limit 개수보다 많으면 나머지는 접어 두고 "더 보기" 버튼을 단다
document.querySelectorAll('.list[data-limit]').forEach(function (list) {
  var limit = +list.dataset.limit, rows = list.querySelectorAll('.row');
  if (rows.length <= limit) return;
  for (var i = limit; i < rows.length; i++) rows[i].hidden = true;
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'more';
  btn.textContent = '더 보기 (' + (rows.length - limit) + '편) ↓';
  btn.addEventListener('click', function () {
    var open = btn.classList.toggle('open');
    for (var i = limit; i < rows.length; i++) rows[i].hidden = !open;
    btn.textContent = open ? '접기 ↑' : '더 보기 (' + (rows.length - limit) + '편) ↓';
  });
  list.after(btn);
});
