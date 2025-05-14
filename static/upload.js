document.addEventListener('DOMContentLoaded', () => {
    // 检查登录状态
    // checkAuthStatus();

    // 图片预览
    document.getElementById('image').addEventListener('change', function(e) {
        const preview = document.getElementById('imagePreview');
        preview.innerHTML = '';
        if (this.files && this.files[0]) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(this.files[0]);
            preview.appendChild(img);
        }
    });

    const csrftoken = getCookie('csrftoken');

    // 表单提交处理
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('title', document.getElementById('title').value);
        formData.append('simple_description', document.getElementById('simple_description').value);
        formData.append('description', document.getElementById('description').value);
        formData.append('from_location', document.getElementById('from_location').value);
        formData.append('goods_price', document.getElementById('goods_price').value);
        formData.append('origin_price', document.getElementById('origin_price').value);
        formData.append('goods_rest_num', document.getElementById('goods_rest_num').value);
        formData.append('image', document.getElementById('image').files[0]);

        try {
            const response = await fetch('/upload_goods/', {
                method: 'POST',
                headers: {
                    // 'Authorization': `Bearer ${localStorage.getItem('token')}` // 假设使用Token认证
                    'X-CSRFToken': csrftoken,
                },
                body: formData
            });

            const result = await response.json();
            if (response.ok) {
                alert('商品上传成功！');
                window.location.href = '/'; // 跳转到首页
            } else {
                alert(`上传失败：${result.error}`);
            }
        } catch (error) {
            alert('网络错误，请重试');
        }
    });
});

// 检查登录状态函数
function checkAuthStatus() {
    const authDiv = document.getElementById('auth-status');
    if (!localStorage.getItem('token')) {
        authDiv.innerHTML = '<p>请先<a href="/login/">登录</a>后再发布商品</p>';
        document.getElementById('uploadForm').style.display = 'none';
    }
}


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

