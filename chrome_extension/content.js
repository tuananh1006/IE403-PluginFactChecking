function getSelectedText(){
    return window.getSelection().toString();
}


chrome.runtime.onMessage.addListener((request,sender,sendResponse)=>{
    if (request.action === 'updateApiKey'){
        chrome.storage.sync.set({geminiApiKey:request.apiKey},()=>{
            sendResponse({success:true});
        });
    }
    if (request.action === 'checkText'){
        const text = getSelectedText();
        if(text){
            checkText(text);
        }
    }
});
chrome.runtime.onMessage.addListener((msg) => {
    if (msg.action === "scrollToText") {
      const targetText = msg.text.trim();
      const paragraphs = document.querySelectorAll("p");
  
      for (const p of paragraphs) {
        if (p.textContent.includes(targetText)) {
          // Scroll đến đoạn cần tìm
          p.scrollIntoView({ behavior: "smooth", block: "center" });
  
          // Highlight đoạn khớp
          const html = p.innerHTML;
          const highlighted = html.replace(
            targetText,
            `<span style="background-color: yellow; font-weight: bold;">${targetText}</span>`
          );
          p.innerHTML = highlighted;
  
          break;
        }
      }
    }
  });
  
  
  
  
  