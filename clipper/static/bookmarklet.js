function relativeToAbsolute(url) {
  if (/^(https?|file|ftps?|mailto|javascript|data):/i.test(url)) return url;

  if (url.startsWith('//')) return `${location.protocol}${url}`;

  if (url.startsWith('/')) return `${location.origin}${url}`;

  if (url.startsWith('./')) return `${location.origin}${location.pathname}${url.slice(2)}`;

  if (/^\s*$/.test(url)) return '';

  return `${location.origin}${location.pathname}${url}`;
}

function replaceUrls(element) {
  element.querySelectorAll('a').forEach((a) => {
    a.href = relativeToAbsolute(a.href);
  });
  element.querySelectorAll('img').forEach((img) => {
    img.src = relativeToAbsolute(img.src);
  });
}

(function () {
  const selection = window.getSelection();
  const range = selection.getRangeAt(0);
  const clonedSelection = range.cloneContents();
  const root = document.createElement('div');
  root.appendChild(clonedSelection);

  replaceUrls(root);

  const url = `http://127.0.0.1:8000/add/?title=${encodeURIComponent(document.title)}&url=${encodeURIComponent(document.location.href)}&content=${encodeURIComponent(root.outerHTML)}`;
  window.open(url);
})();
