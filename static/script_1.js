document.addEventListener("DOMContentLoaded", function(){  // 监听界面
    const button_1 = document.getElementById("button_1");  // js通过id和.html交互

    button_1.addEventListener("click", function(){  // 监听：按钮按下对应函数
        //

        // 获取令牌
        const csrf_get = document.querySelector("[name=csrfmiddlewaretoken]").value;
        // const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch("/handle-request/", {  // POST请求
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_get  // Django 要求的 CSRF 令牌
            },
            body: JSON.stringify({ 
                text: userText
            })  // 发送 JSON 数据
        })
        .then(response => response.json())  // 等待回应
    })

    const button_2 = document.getElementById("button_2"); 
    button_2.addEventListener("click", function(){
        const csrf_get = document.querySelector("[name=csrfmiddlewaretoken]").value;
        fetch("/handle-request/", {  // POST请求
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_get  // Django 要求的 CSRF 令牌
            },
            body: JSON.stringify({ 
                text: userText
            })  // 发送 JSON 数据
        })
        .then(response => response.json())  // 等待回应
    })
})