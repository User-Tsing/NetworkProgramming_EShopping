// login.js
document.getElementById('loginForm').addEventListener('submit', function(e) {  // 用法：获取ID（html里的form id），添加监听（html这个form里的type，可以理解为槽函数）
    e.preventDefault();
    
    const formData = new FormData(this);  // 获取：表单
    const csrftoken = getCookie('csrftoken');  // 获取：令牌
    
    fetch('/login/', {  // 发送函数
        method: 'POST',  // POST类型
        headers: {
            'X-CSRFToken': csrftoken,
        },  // 头文件：令牌
        body: formData  // 发送内容：表单
    })
    .then(response => response.json())  // 等待回应
    .then(data => {
        if (data.success) {  // 解码信息：Success字典内容正确
            window.location.href = data.redirect;  // 界面切换到返回网址
        } else {
            document.getElementById('errorMessage').textContent = data.error;  // 解码信息：Success字典内容不正确：错误信息返回（.html里有id的都可以取出）
        }
    });
});

// Django CSRF token helper

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
