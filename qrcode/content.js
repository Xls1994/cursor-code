(function() {
  // 创建二维码容器
  const qrContainer = document.createElement('div');
  qrContainer.id = 'qr-container';
  document.body.appendChild(qrContainer);

  // 创建logo容器
  const logoContainer = document.createElement('div');
  logoContainer.id = 'logo-container';
  qrContainer.appendChild(logoContainer);

  // 创建二维码元素
  const qrCode = document.createElement('div');
  qrCode.id = 'qr-code';
  qrCode.style.display = 'none';
  qrContainer.appendChild(qrCode);

  // 创建网站名称元素
  const siteName = document.createElement('div');
  siteName.id = 'site-name';
  siteName.textContent = new URL(window.location.href).hostname;
  siteName.style.display = 'none';
  qrContainer.appendChild(siteName);

  // 创建页面标题元素
  const pageTitle = document.createElement('div');
  pageTitle.id = 'page-title';
  pageTitle.textContent = document.title.length > 10 ? document.title.substring(0, 10) + '...' : document.title;
  pageTitle.style.display = 'none';
  qrContainer.appendChild(pageTitle);

  // 生成二维码
  new QRCode(qrCode, {
    text: window.location.href,
    width: 256,
    height: 256,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.H
  });

  // 获取网页logo
  const logoUrl = getLogo();
  if (logoUrl) {
    addLogoToContainer(logoUrl);
  }

  function getLogo() {
    const icons = document.querySelectorAll('link[rel*="icon"]');
    return icons.length ? icons[icons.length - 1].href : null;
  }

  function addLogoToContainer(logoUrl) {
    const logo = document.createElement('img');
    logo.src = logoUrl;
    logo.id = 'qr-logo';
    logo.onclick = toggleQRCode;
    logoContainer.appendChild(logo);
  }

  function toggleQRCode() {
    const isVisible = qrCode.style.display === 'block';
    qrCode.style.display = isVisible ? 'none' : 'block';
    siteName.style.display = isVisible ? 'none' : 'block';
    pageTitle.style.display = isVisible ? 'none' : 'block';
    logoContainer.style.position = isVisible ? 'static' : 'absolute';
  }
})();
