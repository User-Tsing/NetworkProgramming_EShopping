


document.addEventListener('DOMContentLoaded', function() {
    // 可以添加交互效果
    // 轮播图初始化
    const slides = document.querySelectorAll('.slide');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    let currentIndex = 0;
    let autoPlayInterval;

    // 创建指示器
    slides.forEach((_, index) => {
        const indicator = document.createElement('div');
        indicator.classList.add('indicator');
        if (index === 0) indicator.classList.add('active');
        indicator.addEventListener('click', () => goToSlide(index));
        indicatorsContainer.appendChild(indicator);
    });

    // 切换逻辑
    function goToSlide(index) {
        slides[currentIndex].classList.remove('active');
        indicatorsContainer.children[currentIndex].classList.remove('active');
        
        currentIndex = (index + slides.length) % slides.length;
        
        slides[currentIndex].classList.add('active');
        indicatorsContainer.children[currentIndex].classList.add('active');
    }

    // 自动播放
    function startAutoPlay() {
        autoPlayInterval = setInterval(() => {
            goToSlide(currentIndex + 1);
        }, 5000); // 5秒切换
    }

    // 手动控制
    document.querySelector('.carousel-prev').addEventListener('click', () => {
        clearInterval(autoPlayInterval);
        goToSlide(currentIndex - 1);
        startAutoPlay();
    });

    document.querySelector('.carousel-next').addEventListener('click', () => {
        clearInterval(autoPlayInterval);
        goToSlide(currentIndex + 1);
        startAutoPlay();
    });

    // 悬停暂停
    document.querySelector('.carousel-container').addEventListener('mouseenter', () => {
        clearInterval(autoPlayInterval);
    });

    document.querySelector('.carousel-container').addEventListener('mouseleave', () => {
        startAutoPlay();
    });

    // 监听页面可见性变化
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            startAutoPlay();
        } else {
            clearInterval(autoPlayInterval);
        }
    });

    // 页面显示时启动自动播放
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            // 如果页面是从缓存中恢复的
            initCarousel();
            setupManualControls();
            startAutoPlay();
        }
    });

    // 页面隐藏时清除定时器
    window.addEventListener('pagehide', function() {
        clearInterval(autoPlayInterval);
    });

    // 启动自动播放
    startAutoPlay();

    document.querySelectorAll('.content-item').forEach(item => {
        item.addEventListener('click', () => {
            item.style.transform = 'scale(1.02)';
            setTimeout(() => {
                item.style.transform = 'scale(1)';
            }, 200);
        });
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




// document.addEventListener('DOMContentLoaded', function() {
//     //
// });