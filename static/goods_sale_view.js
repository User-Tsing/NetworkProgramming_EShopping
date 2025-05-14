let currentEditingGoodsId = null;

function openEditGoodsModal(goodsId) {
    currentEditingGoodsId = goodsId;
    const modal = document.getElementById('goodsEditModal');
    modal.style.display = 'block';
    console.log(1);

    // 获取商品当前数据并填充表单
    fetch(`/detail_json/${goodsId}/`)
        .then(response => response.json())
        .then(data => {
            // console.log(data.origin_price);
            document.getElementById('editTitle').value = data.title;
            document.getElementById('editSimpleDesc').value = data.simple_description;
            document.getElementById('editDesc').value = data.description;
            document.getElementById('editPrice').value = data.goods_price;
            document.getElementById('editOriginalPrice').value = data.origin_price;
            document.getElementById('editStock').value = data.goods_rest_num;
            document.getElementById('editLocation').value = data.from_location;
            modal.style.display = 'block';
        });
}

function closeGoodsModal() {
    document.getElementById('goodsEditModal').style.display = 'none';
}

// 下架商品
function delistGoods(goodsId) {
    if (confirm('确定要下架该商品吗？')) {
        fetch(`/update_goods/${goodsId}/`, {  // 注意结尾斜杠
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded', // 明确内容类型
            },
            body: new URLSearchParams({  // 使用正确格式
                'stock': 0
            })
        }).then(() => location.reload());
    }
}

// 提交修改
document.getElementById('goodsEditForm').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log(1);
    const formData = new FormData(this);
    
    fetch(`/update_goods/${currentEditingGoodsId}/`, {  // 确保结尾斜杠
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // 添加CSRF令牌
        },
        body: formData
    }).then(() => location.reload());
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
}  // cookie是必需的