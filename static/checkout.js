// checkout.js

const csrftoken = getCookie('csrftoken');

function confirmPayment() {
    const selectedIds = window.location.search
        .split('=')[1]
        .split(',')
        .map(Number);

    const notes = {};
    selectedIds.forEach(id => {
        const noteInput = document.getElementById(`note_${id}`);
        notes[id] = noteInput ? noteInput.value : '';
    });

    fetch('/confirm-payment/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ items: selectedIds, notes: notes })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('支付成功！订单号：' + data.order_id);
            window.location.href = '/main/';
        }
        else{
            alert('出现错误')
        }
    });
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
