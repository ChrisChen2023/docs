(function () {
    function ensureToast() {
      let t = document.getElementById('feedback-toast');
      if (!t) { t = document.createElement('div'); t.id = 'feedback-toast'; document.body.appendChild(t); }
      return t;
    }
    function showToast(msg, kind) {
      const t = ensureToast();
      t.textContent = msg;
      t.classList.remove('positive','negative','visible');
      if (kind) t.classList.add(kind);
      requestAnimationFrame(() => t.classList.add('visible'));
      clearTimeout(showToast._t);
      showToast._t = setTimeout(() => t.classList.remove('visible'), 2200);
    }
    function bind(id, msg, kind) {
      const b = document.getElementById(id);
      if (!b || b.dataset.enhanced === '1') return;
      b.dataset.enhanced = '1';
      b.addEventListener('click', () => {
        b.classList.remove('feedback-clicked');
        void b.offsetWidth;
        b.classList.add('feedback-clicked');
        showToast(msg, kind);
      });
    }
    function attach() {
      bind('feedback-thumbs-up', '✅ 感谢反馈！很高兴这篇文档对你有帮助', 'positive');
      bind('feedback-thumbs-down', '📝 感谢反馈！请告诉我们如何改进', 'negative');
    }
    attach();
    new MutationObserver(attach).observe(document.body, { childList: true, subtree: true });
  })();
  