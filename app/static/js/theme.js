// 主题管理
(function() {
    // 在DOM加载前应用主题，避免闪烁
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    
    // DOM加载完成后设置按钮状态
    document.addEventListener('DOMContentLoaded', function() {
        // 获取当前主题或设置默认主题（深色模式）
        let currentTheme = localStorage.getItem('theme') || 'dark';
        
        // 更新按钮状态
        updateThemeButton(currentTheme);
        
        // 主题切换按钮点击事件
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', function() {
                // 切换主题
                currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
                
                // 保存主题设置到本地存储
                localStorage.setItem('theme', currentTheme);
                
                // 应用主题
                applyTheme(currentTheme);
            });
        }
    });
})();

// 应用主题函数
function applyTheme(theme) {
    // 更新HTML标签的data-bs-theme属性
    document.documentElement.setAttribute('data-bs-theme', theme);
    
    // 更新主题切换按钮状态
    updateThemeButton(theme);
}

// 更新主题切换按钮状态
function updateThemeButton(theme) {
    // 更新主题切换按钮图标
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    
    if (themeIcon && themeText) {
        if (theme === 'dark') {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            themeText.textContent = '切换到明亮模式';
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            themeText.textContent = '切换到深色模式';
        }
    }
} 