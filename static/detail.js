// static/detail.js
// const csrftoken = getCookie('csrftoken');
document.getElementById('addToCartForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // const formData = new FormData(this);
    const form = e.target;
    // const productId = document.getElementById('addToCartForm').dataset.productId; // 通过HTML属性获取
    const productId = form.dataset.productId; 
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/add-to-cart/${productId}/`, {  // 使用反引号
        method: 'POST',
        headers: {
            // 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // 直接获取CSRF Token
            'X-CSRFToken': csrfToken,
        },
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('cart-message');
        if (data.success) {
            messageDiv.innerHTML = `<p style="color:green">${data.message}</p>`; // 使用反引号
        } else {
            messageDiv.innerHTML = `<p style="color:red">${data.error}</p>`; // 使用反引号
        }
    });
});


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

// 评价表单验证
document.querySelector('.review-form form').addEventListener('submit', function(e) {
    const rating = parseInt(this.querySelector('[name="rating"]').value);
    const comment = this.querySelector('[name="comment"]').value.trim();
    
    if (rating < 1 || rating > 5) {
        alert('请选择1-5星评分');
        e.preventDefault();
    }
    
    if (comment.length < 10) {
        alert('评价内容至少需要10个字');
        e.preventDefault();
    }
});
