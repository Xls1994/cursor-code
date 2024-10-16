chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "translate") {
    fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(request.text)}&langpair=zh|en`)
      .then(response => response.json())
      .then(data => {
        sendResponse({ translation: data.responseData.translatedText });
      })
      .catch(error => {
        console.error("翻译错误:", error);
        sendResponse({ translation: "翻译失败" });
      });
    return true; // 保持消息通道开放
  }
});