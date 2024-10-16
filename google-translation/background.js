chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "translateWithGoogle",
    title: "使用谷歌进行翻译",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "translateWithGoogle") {
    const selectedText = encodeURIComponent(info.selectionText);
    const url = `https://translate.google.com/?sl=auto&tl=en&text=${selectedText}&op=translate`;
    chrome.tabs.create({ url: url });
  }
});