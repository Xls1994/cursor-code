let translationPopup = null;
let translationTimeout = null;

document.addEventListener('mouseup', (event) => {
  const selectedText = window.getSelection().toString().trim();
  if (selectedText) {
    chrome.runtime.sendMessage({ action: "translate", text: selectedText }, (response) => {
      if (response.translation) {
        showTranslation(response.translation, event.clientX, event.clientY);
      }
    });
  }
});

document.addEventListener('mousedown', () => {
  hideTranslation();
});

function showTranslation(text, x, y) {
  hideTranslation();

  translationPopup = document.createElement('div');
  translationPopup.style.position = 'fixed';
  translationPopup.style.left = `${x}px`;
  translationPopup.style.top = `${y}px`;
  translationPopup.style.backgroundColor = 'white';
  translationPopup.style.border = '1px solid black';
  translationPopup.style.padding = '5px';
  translationPopup.style.borderRadius = '3px';
  translationPopup.style.zIndex = '10000';
  translationPopup.textContent = text;

  document.body.appendChild(translationPopup);

  translationTimeout = setTimeout(hideTranslation, 3000);
}

function hideTranslation() {
  if (translationPopup) {
    translationPopup.remove();
    translationPopup = null;
  }
  if (translationTimeout) {
    clearTimeout(translationTimeout);
    translationTimeout = null;
  }
}