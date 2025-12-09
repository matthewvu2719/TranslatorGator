// Translator Gator - Content Script
const API_URL = 'http://localhost:8000';

let isTranslating = false;
let translationMode = 'natural';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'translate') {
    translatePage(request.mode);
  } else if (request.action === 'clear') {
    clearTranslations();
  }
});

async function translatePage(mode = 'natural') {
  if (isTranslating) return;
  isTranslating = true;
  translationMode = mode;

  const images = document.querySelectorAll('img');
  console.log(`Found ${images.length} images on page`);

  for (const img of images) {
    if (isMangaImage(img)) {
      await translateImage(img);
    }
  }

  isTranslating = false;
}

function isMangaImage(img) {
  const src = img.src.toLowerCase();
  const minWidth = 400;
  const minHeight = 400;
  
  return (
    img.naturalWidth >= minWidth &&
    img.naturalHeight >= minHeight &&
    (src.includes('manga') || 
     src.includes('comic') || 
     src.includes('page') ||
     img.alt.toLowerCase().includes('manga'))
  );
}

async function translateImage(img) {
  try {
    const response = await fetch(`${API_URL}/translate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_url: img.src,
        mode: translationMode
      })
    });

    const data = await response.json();
    
    if (data.bubbles && data.bubbles.length > 0) {
      createOverlay(img, data.bubbles);
    }
  } catch (error) {
    console.error('Translation error:', error);
  }
}

function createOverlay(img, bubbles) {
  const container = img.parentElement;
  const overlay = document.createElement('div');
  overlay.className = 'translator-gator-overlay';
  
  overlay.style.position = 'absolute';
  overlay.style.top = img.offsetTop + 'px';
  overlay.style.left = img.offsetLeft + 'px';
  overlay.style.width = img.offsetWidth + 'px';
  overlay.style.height = img.offsetHeight + 'px';
  overlay.style.pointerEvents = 'none';

  bubbles.forEach(bubble => {
    const textBox = document.createElement('div');
    textBox.className = 'translation-text';
    textBox.textContent = bubble.translated_text;
    
    const scaleX = img.offsetWidth / img.naturalWidth;
    const scaleY = img.offsetHeight / img.naturalHeight;
    
    textBox.style.position = 'absolute';
    textBox.style.left = (bubble.x * scaleX) + 'px';
    textBox.style.top = (bubble.y * scaleY) + 'px';
    textBox.style.width = (bubble.width * scaleX) + 'px';
    textBox.style.height = (bubble.height * scaleY) + 'px';
    
    overlay.appendChild(textBox);
  });

  container.style.position = 'relative';
  container.appendChild(overlay);
}

function clearTranslations() {
  document.querySelectorAll('.translator-gator-overlay').forEach(el => el.remove());
}
