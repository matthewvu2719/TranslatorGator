document.getElementById('translate').addEventListener('click', async () => {
  const mode = document.getElementById('mode').value;
  const status = document.getElementById('status');
  
  status.textContent = 'Translating...';
  status.className = 'status';
  
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, { 
    action: 'translate',
    mode: mode
  });
  
  setTimeout(() => {
    status.textContent = 'Translation complete!';
    status.className = 'status success';
  }, 1000);
});

document.getElementById('clear').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, { 
    action: 'clear'
  });
  
  const status = document.getElementById('status');
  status.textContent = 'Cleared!';
  status.className = 'status success';
});
