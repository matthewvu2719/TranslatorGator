// Background service worker for Translator Gator

chrome.runtime.onInstalled.addListener(() => {
  console.log('Translator Gator installed!');
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.sendMessage(tab.id, { action: 'translate', mode: 'natural' });
});
