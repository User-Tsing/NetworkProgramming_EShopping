// 自动滚动到底部
function scrollToBottom() {
    const container = document.getElementById('messagesContainer');
    container.scrollTop = container.scrollHeight;
}

// 发送消息
function sendMessage(userId) {
    const input = document.getElementById('messageInput');
    const content = input.value.trim();
    if (!content) return;

    const formData = new FormData();
    formData.append('receiver_id', userId);
    formData.append('content', content);

    fetch('/send_message/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    }).then(response => {
        if (response.ok) {
            input.value = '';
            // 添加临时消息
            const container = document.getElementById('messagesContainer');
            const newMsg = document.createElement('div');
            newMsg.className = 'message sent';
            newMsg.innerHTML = `
                <div class="message-content">
                    <p>${content}</p>
                    <span class="timestamp">刚刚</span>
                </div>
            `;
            container.appendChild(newMsg);
            scrollToBottom();
        }
    });
}

// 轮询新消息
function pollMessages() {
    fetch(window.location.href)
        .then(response => response.text())
        .then(html => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            const newMessages = tempDiv.querySelectorAll('.message.received');
            const existingIds = new Set(
                Array.from(document.querySelectorAll('.message')).map(el => el.dataset.id)
            );
            
            newMessages.forEach(msg => {
                if (!existingIds.has(msg.dataset.id)) {
                    document.getElementById('messagesContainer').appendChild(msg.cloneNode(true));
                }
            });
        });
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    scrollToBottom();
    setInterval(pollMessages, 3000);  // 每3秒轮询
});

// CSRF Token获取
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}