// 色彩主题管理
(function() {
    // 在DOM加载前应用色彩主题，避免闪烁
    const savedColorTheme = localStorage.getItem('colorTheme') || 'blue';
    document.documentElement.setAttribute('data-bs-theme-color', savedColorTheme);
    
    // DOM加载完成后设置按钮状态
    document.addEventListener('DOMContentLoaded', function() {
        // 获取当前色彩主题或设置默认主题（蓝色系）
        let currentColorTheme = localStorage.getItem('colorTheme') || 'blue';
        
        // 更新下拉菜单选中状态
        updateColorThemeMenu(currentColorTheme);
        
        // 色彩主题切换事件
        const colorThemeButtons = document.querySelectorAll('.color-theme-option');
        if (colorThemeButtons.length > 0) {
            colorThemeButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    // 获取选择的主题
                    const selectedTheme = this.getAttribute('data-theme');
                    
                    // 保存色彩主题设置到本地存储
                    localStorage.setItem('colorTheme', selectedTheme);
                    
                    // 应用色彩主题
                    applyColorTheme(selectedTheme);
                });
            });
        }
    });
})();

// 应用色彩主题函数
function applyColorTheme(theme) {
    // 更新HTML标签的data-bs-theme-color属性
    document.documentElement.setAttribute('data-bs-theme-color', theme);
    
    // 更新下拉菜单选中状态
    updateColorThemeMenu(theme);
}

// 更新色彩主题菜单状态
function updateColorThemeMenu(theme) {
    // 移除所有选项的选中状态
    document.querySelectorAll('.color-theme-option').forEach(item => {
        item.classList.remove('active');
        item.querySelector('i').classList.remove('fa-check');
    });
    
    // 设置当前主题的选中状态
    const activeItem = document.querySelector(`.color-theme-option[data-theme="${theme}"]`);
    if (activeItem) {
        activeItem.classList.add('active');
        const icon = activeItem.querySelector('i');
        if (icon) {
            icon.classList.add('fa-check');
        }
    }
    
    // 更新下拉菜单按钮文本
    const dropdownButton = document.getElementById('colorThemeButton');
    if (dropdownButton) {
        let themeName = '蓝色系';
        switch(theme) {
            case 'purple':
                themeName = '紫色系';
                break;
            case 'gray':
                themeName = '灰色系';
                break;
            case 'green':
                themeName = '绿色系';
                break;
        }
        dropdownButton.querySelector('.theme-name').textContent = themeName;
    }
} 