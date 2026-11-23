// 따라다니는 뒤로가기 버튼 (글 페이지 왼쪽 아래)
// 블로그 안에서 들어왔으면 이전 페이지로, 밖(검색·인스타 등)에서 바로 들어왔으면 홈으로
(function () {
  var a = document.createElement('a');
  a.className = 'backbtn';
  a.href = '../';
  a.setAttribute('aria-label', '뒤로 가기');
  a.innerHTML = '<span aria-hidden="true">←</span><b>뒤로</b>';
  a.addEventListener('click', function (e) {
    var fromHere = document.referrer && document.referrer.indexOf(location.origin) === 0;
    if (fromHere && history.length > 1) { e.preventDefault(); history.back(); }
  });
  document.body.appendChild(a);
})();
