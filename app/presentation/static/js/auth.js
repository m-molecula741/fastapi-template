/**
 * Обработка аутентификации пользователя
 */

// Базовый URL для API
const API_BASE_URL = '/api';

// Функция для регистрации пользователя
async function registerUser() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // Сброс предыдущих ошибок
    resetFormErrors();
    
    // Валидация формы
    if (!email || !password || !confirmPassword) {
        showFlashMessage('Пожалуйста, заполните все поля', 'danger');
        return;
    }
    
    if (password !== confirmPassword) {
        document.getElementById('confirm-password').classList.add('is-invalid');
        document.getElementById('confirm-password-feedback').textContent = 'Пароли не совпадают';
        return;
    }
    
    try {
        const response = await axios.post(`${API_BASE_URL}/users/register`, {
            email: email,
            password: password
        });
        
        if (response.status === 201) {
            // Успешная регистрация
            showFlashMessage('Регистрация успешна! Теперь вы можете войти в систему.', 'success');
            
            // Перенаправление на страницу входа через 2 секунды
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 2000);
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Функция для входа пользователя
async function loginUser() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Сброс предыдущих ошибок
    resetFormErrors();
    
    // Валидация формы
    if (!email || !password) {
        showFlashMessage('Пожалуйста, заполните все поля', 'danger');
        return;
    }
    
    try {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, {
            email: email,
            password: password
        });
        
        if (response.status === 200 && response.data) {
            // Сохранение токенов
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            
            // Установка токена в заголовки для всех последующих запросов
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
            
            // Успешный вход
            showFlashMessage('Вход выполнен успешно!', 'success');
            
            // Перенаправление на страницу профиля
            setTimeout(() => {
                window.location.href = '/users/profile';
            }, 1000);
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Функция для выхода пользователя
async function logoutUser() {
    try {
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
            // Вызов API для выхода
            await axios.delete(`${API_BASE_URL}/private/auth/logout`, {
                headers: {
                    'Cookie': `refresh_token=${refreshToken}`
                }
            });
        }
        
        // Очистка локального хранилища
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // Удаление токена из заголовков
        delete axios.defaults.headers.common['Authorization'];
        
        // Перенаправление на главную страницу
        window.location.href = '/';
    } catch (error) {
        console.error('Ошибка при выходе:', error);
        // Даже если произошла ошибка, всё равно выходим
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    }
}

// Функция для обновления токена
async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
        // Если нет refresh токена, перенаправляем на страницу входа
        window.location.href = '/auth/login';
        return null;
    }
    
    try {
        const response = await axios.patch(`${API_BASE_URL}/auth/refresh`, {}, {
            headers: {
                'Cookie': `refresh_token=${refreshToken}`
            }
        });
        
        if (response.status === 200 && response.data) {
            // Обновление токенов
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            
            // Обновление заголовка авторизации
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
            
            return response.data.access_token;
        }
    } catch (error) {
        console.error('Ошибка при обновлении токена:', error);
        // При ошибке обновления токена, выходим из системы
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth/login';
        return null;
    }
}

// Функция для загрузки профиля пользователя
async function loadUserProfile() {
    try {
        const token = localStorage.getItem('access_token');
        
        if (!token) {
            // Если нет токена, перенаправляем на страницу входа
            window.location.href = '/auth/login';
            return;
        }
        
        // Установка токена в заголовки
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        const response = await axios.get(`${API_BASE_URL}/private/users/me`);
        
        if (response.status === 200 && response.data) {
            // Отображение информации о пользователе
            document.getElementById('user-email').textContent = response.data.email;
            
            // Статус аккаунта
            const statusElement = document.getElementById('account-status');
            if (response.data.is_active) {
                statusElement.innerHTML = '<span class="status-badge status-active">Активен</span>';
            } else {
                statusElement.innerHTML = '<span class="status-badge status-inactive">Неактивен</span>';
            }
            
            // Дата регистрации (предполагаем, что она приходит с бэкенда)
            if (response.data.created_at) {
                const registerDate = new Date(response.data.created_at);
                document.getElementById('register-date').textContent = registerDate.toLocaleDateString();
            } else {
                document.getElementById('register-date').textContent = 'Недоступно';
            }
        }
    } catch (error) {
        if (error.response && error.response.status === 401) {
            // Если токен истек, пробуем обновить
            const newToken = await refreshToken();
            if (newToken) {
                // Если токен обновлен успешно, повторяем запрос
                loadUserProfile();
            }
        } else {
            handleApiError(error);
        }
    }
}

// Вспомогательные функции

// Показать сообщение пользователю
function showFlashMessage(message, type = 'info') {
    const flashContainer = document.getElementById('flash-messages');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    flashContainer.appendChild(alertDiv);
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => {
            flashContainer.removeChild(alertDiv);
        }, 500);
    }, 5000);
}

// Сброс ошибок формы
function resetFormErrors() {
    const invalidInputs = document.querySelectorAll('.is-invalid');
    invalidInputs.forEach(input => {
        input.classList.remove('is-invalid');
    });
    
    const feedbacks = document.querySelectorAll('.invalid-feedback');
    feedbacks.forEach(feedback => {
        feedback.textContent = '';
    });
}

// Обработка ошибок API
function handleApiError(error) {
    if (error.response) {
        // Если сервер вернул ошибку с данными
        if (error.response.data && error.response.data.detail) {
            if (typeof error.response.data.detail === 'string') {
                showFlashMessage(error.response.data.detail, 'danger');
            } else if (Array.isArray(error.response.data.detail)) {
                // Обработка ошибок валидации полей формы
                error.response.data.detail.forEach(err => {
                    if (err.loc && err.loc.length > 1) {
                        const fieldName = err.loc[1];
                        const fieldElement = document.getElementById(fieldName);
                        const feedbackElement = document.getElementById(`${fieldName}-feedback`);
                        
                        if (fieldElement && feedbackElement) {
                            fieldElement.classList.add('is-invalid');
                            feedbackElement.textContent = err.msg;
                        } else {
                            showFlashMessage(`Ошибка поля ${fieldName}: ${err.msg}`, 'danger');
                        }
                    } else {
                        showFlashMessage(err.msg, 'danger');
                    }
                });
            }
        } else {
            showFlashMessage(`Ошибка: ${error.response.status} ${error.response.statusText}`, 'danger');
        }
    } else if (error.request) {
        // Если запрос был сделан, но нет ответа
        showFlashMessage('Нет ответа от сервера. Пожалуйста, проверьте ваше интернет-соединение.', 'danger');
    } else {
        // Другие ошибки
        showFlashMessage(`Произошла ошибка: ${error.message}`, 'danger');
    }
} 