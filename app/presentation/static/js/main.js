/**
 * Основной JavaScript файл
 */

// Обработка состояния авторизации
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    
    // Обработка события выхода
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logoutUser();
        });
    }
});

// Проверка статуса авторизации и обновление UI
function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    
    // Элементы навигации
    const loginNavItem = document.getElementById('login-nav-item');
    const registerNavItem = document.getElementById('register-nav-item');
    const profileNavItem = document.getElementById('profile-nav-item');
    const logoutNavItem = document.getElementById('logout-nav-item');
    
    if (token) {
        // Пользователь авторизован
        if (loginNavItem) loginNavItem.classList.add('d-none');
        if (registerNavItem) registerNavItem.classList.add('d-none');
        if (profileNavItem) profileNavItem.classList.remove('d-none');
        if (logoutNavItem) logoutNavItem.classList.remove('d-none');
        
        // Установка токена для всех запросов Axios
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        // Пользователь не авторизован
        if (loginNavItem) loginNavItem.classList.remove('d-none');
        if (registerNavItem) registerNavItem.classList.remove('d-none');
        if (profileNavItem) profileNavItem.classList.add('d-none');
        if (logoutNavItem) logoutNavItem.classList.add('d-none');
        
        // Удаление токена из заголовков
        delete axios.defaults.headers.common['Authorization'];
        
        // Если находимся на защищенной странице, перенаправляем на страницу входа
        const currentPath = window.location.pathname;
        if (currentPath.startsWith('/users/')) {
            window.location.href = '/auth/login';
        }
    }
}

// Перехватчик для обработки 401 ошибок и обновления токена
axios.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;
        
        // Если ошибка 401 и запрос еще не повторялся
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            try {
                // Пытаемся обновить токен
                const newToken = await refreshToken();
                
                if (newToken) {
                    // Если успешно обновили токен, повторяем запрос
                    originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                    return axios(originalRequest);
                } else {
                    // Если не удалось обновить, перенаправляем на страницу входа
                    window.location.href = '/auth/login';
                    return Promise.reject(error);
                }
            } catch (refreshError) {
                // Если произошла ошибка при обновлении токена
                window.location.href = '/auth/login';
                return Promise.reject(refreshError);
            }
        }
        
        return Promise.reject(error);
    }
); 