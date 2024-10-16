chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "save") {
    chrome.storage.local.set({ 'weixinContent': request.content }, function() {
      chrome.runtime.sendMessage({ action: "contentSaved" });
    });
  }
});