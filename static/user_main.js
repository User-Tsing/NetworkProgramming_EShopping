// 防抖处理（避免频繁请求）
let debounceTimer;
const csrftoken = getCookie('csrftoken')
function calculateTotal() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    // 获取所有选中的ID
    const selectedIds = Array.from(
      document.querySelectorAll('input[name="selected_items"]:checked')
    ).map(checkbox => checkbox.value);

    // 发送请求
    fetch('/main/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ selected_ids: selectedIds })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.getElementById('total-amount').textContent = data.total.toFixed(2);
      }
    });
  }, 300); // 300ms防抖间隔
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

// 打开编辑模态窗口
function openEditModal(type) {
    const modal = document.getElementById('editModal');
    const sections = document.querySelectorAll('.edit-section');
    
    sections.forEach(section => section.classList.remove('active'));
    document.getElementById(`${type}Edit`).classList.add('active');
    modal.style.display = 'block';
}

// 关闭模态窗口
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

// 表单提交处理
document.getElementById('editForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    fetch('/update_profile/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // 刷新页面显示新数据
        } else {
            alert(data.error || '更新失败');
        }
    });
});

// 点击外部关闭模态窗口
window.onclick = function(e) {
    const modal = document.getElementById('editModal');
    if (e.target === modal) {
        modal.style.display = 'none';
    }
}

document.querySelector('input[name="avatar"]').addEventListener('change', function(e) {
    const reader = new FileReader();
    reader.onload = function() {
        document.querySelector('.user-avatar').src = reader.result;
    }
    reader.readAsDataURL(e.target.files[0]);
});






document.addEventListener('DOMContentLoaded', function() {
    // 删除操作
    function redirectToCheckout(event) {
        event.preventDefault(); // 阻止默认表单提交

        const selectedIds = Array.from(
            document.querySelectorAll('input[name="selected_items"]:checked')
        ).map(checkbox => checkbox.value);

        if (selectedIds.length === 0) {
            alert('请选择要结算的商品');
            return;
        }

        // 修正参数名为items
        window.location.href = `/checkout/?items=${selectedIds.join(',')}`;
    }

    function deleteCartItem(itemId) {
        const csrftoken = getCookie('csrftoken');
        if (confirm('确定要删除该商品吗？')) {
            fetch(`/delete_cart_item/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload(); // 刷新页面
                } else {
                    alert(data.error);
                }
            });
        }
    }

    function deleteSelectedItems() {
        const csrftoken = getCookie('csrftoken');
        const selectedIds = Array.from(
            document.querySelectorAll('input[name="selected_items"]:checked')
        ).map(checkbox => checkbox.value);

        if (selectedIds.length === 0) {
            alert('请选择要删除的商品');
            return;
        }

        if (confirm('确定要删除选中的商品吗？')) {
            fetch('/delete_selected_cart_items/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({ selected_ids: selectedIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload(); // 刷新页面
                } else {
                    alert(data.error);
                }
            });
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
})



