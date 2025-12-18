function sendMessage() {
    const input = document.getElementById('user-input');
    const query = input.value;
    if(!query) return;

    addMessage(query, 'user-message');
    updateConsole(`Querying Threat Intelligence for: "${query}"...`);
    
    fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query: query})
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.response, 'assistant-message');
        updateConsole(`Response generated via ${data.model}`);
    });
    input.value = '';
}

function updateConsole(text) {
    const out = document.getElementById('console-out');
    out.innerHTML += `<br>> ${new Date().toLocaleTimeString()}: ${text}`;
    out.scrollTop = out.scrollHeight;
}

function addMessage(text, type) {
    const box = document.getElementById('chat-box');
    const div = document.createElement('div');
    div.className = `message ${type}`;
    
    let html = text;
    if(text.includes("[INTERNAL]")) html = `<span class="badge internal">VERIFIED POLICY</span> ` + text.replace("[INTERNAL]", "");
    if(text.includes("[GLOBAL]")) html = `<span class="badge global">GENERAL INFO</span> ` + text.replace("[GLOBAL]", "");
    
    div.innerHTML = html;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;

}
