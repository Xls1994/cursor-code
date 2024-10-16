document.getElementById('extractButton').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: extractContent
  });
});

function extractContent() {
  const content = document.querySelector('#js_content');
  if (content) {
    const text = content.innerText;
    chrome.runtime.sendMessage({ action: "save", content: text });
  } else {
    alert('无法找到文章内容');
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "contentSaved") {
    chrome.storage.local.get(['weixinContent'], function(result) {
      const blob = new Blob([result.weixinContent], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      chrome.downloads.download({
        url: url,
        filename: 'weixin.txt',
        saveAs: false
      }, function() {
        URL.revokeObjectURL(url);
      });
    });
  }
});