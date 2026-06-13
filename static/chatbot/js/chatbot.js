// d:/portfolio/static/chatbot/js/chatbot.js
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('chatbot-toggle');
  const widget = document.getElementById('chatbot-widget');
  const sendBtn = document.getElementById('chatbot-send');
  const input = document.getElementById('chatbot-input');
  const messages = document.getElementById('chatbot-messages');

  const addMessage = (text, sender) => {
    const div = document.createElement('div');
    div.className = sender;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  };

  toggleBtn.addEventListener('click', () => {
    widget.classList.toggle('hidden');
    if (!widget.classList.contains('hidden')) {
      input.focus();
    }
  });

  const postMessage = async (msg) => {
    try {
      const resp = await fetch('/chatbot/api/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '' },
        body: JSON.stringify({ message: msg })
      });
      const data = await resp.json();
      return data.answer || 'Sorry, I could not understand.';
    } catch (e) {
      return 'Error contacting the bot.';
    }
  };

  const handleSend = async () => {
    const msg = input.value.trim();
    if (!msg) return;
    addMessage(msg, 'user');
    input.value = '';
    const answer = await postMessage(msg);
    addMessage(answer, 'bot');
  };

  sendBtn.addEventListener('click', handleSend);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleSend();
  });
});
