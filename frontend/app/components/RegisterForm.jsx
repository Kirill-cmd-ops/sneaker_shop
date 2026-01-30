"use client";
import { useState } from "react";
import Link from "next/link";

export default function RegisterForm() {
  const [formData, setFormData] = useState({ 
    first_name: "", 
    last_name: "", 
    email: "", 
    password: "",
    confirm_password: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");

    // Валидация паролей на фронтенде
    if (formData.password !== formData.confirm_password) {
      setIsSuccess(false);
      setMessage("❌ Ошибка: Пароли не совпадают");
      return;
    }

    // Проверка минимальной длины пароля
    if (formData.password.length < 8) {
      setIsSuccess(false);
      setMessage("❌ Ошибка: Пароль должен содержать минимум 8 символов");
      return;
    }

    try {
      // Подготавливаем данные для отправки
      const requestData = {
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirm_password,
        first_name: formData.first_name,
        last_name: formData.last_name,
        is_active: true,
        is_superuser: false,
        is_verified: false,
      };

      console.log("Отправка запроса регистрации:", requestData);
      
      // Функция для отправки запроса с fallback на разные порты
      const makeRequest = async (url) => {
        try {
          const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
            credentials: "include",
          });
          return { response, error: null };
        } catch (error) {
          return { response: null, error };
        }
      };

      // Пробуем сначала через Kong (8000), если не работает - напрямую через auth_service (8002)
      let result = await makeRequest("http://localhost:8000/api/v1/auth/register");
      if (result.error) {
        console.log("Kong (8000) недоступен, пробуем прямой доступ к auth_service (8002)");
        result = await makeRequest("http://localhost:8002/api/v1/auth/register");
      }

      if (result.error) {
        throw new Error("Не удалось подключиться к серверу. Проверьте, что сервисы запущены.");
      }

      const response = result.response;

      console.log("Ответ сервера:", response.status, response.statusText);

      if (response.ok || response.status === 201) {
        setIsSuccess(true);
        setMessage("✅ Успешная регистрация! Перенаправляем на страницу входа...");
        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      } else {
        setIsSuccess(false);
        let errorText = "Ошибка регистрации";
        try {
          const errorData = await response.json();
          errorText = errorData.detail || errorData.message || JSON.stringify(errorData);
        } catch (e) {
          errorText = await response.text().catch(() => `Ошибка ${response.status}: ${response.statusText}`);
        }
        setMessage(`❌ Ошибка: ${errorText}`);
      }
    } catch (error) {
      console.error("Ошибка запроса:", error);
      setIsSuccess(false);
      const errorMessage = error.message || "Ошибка сети";
      setMessage(`❌ Ошибка: ${errorMessage}. Проверьте консоль браузера для деталей.`);
    }
  };

  return (
    <div className="flex justify-center items-center">
      <div className="w-[420px] p-8 bg-white border-4 border-yellow-500 shadow-lg rounded-lg text-black">
        <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>
        {message && (
          <p className={`mb-4 text-center text-base ${isSuccess ? "text-green-600" : "text-red-500"}`}>
            {message}
          </p>
        )}
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="text"
            name="first_name"
            placeholder="Введите имя"
            value={formData.first_name}
            onChange={handleChange}
            required
            className={`w-full p-4 border rounded-lg text-lg ${formData.first_name ? "border-yellow-500" : "border-gray-300"}`}
          />
          <input
            type="text"
            name="last_name"
            placeholder="Введите фамилию"
            value={formData.last_name}
            onChange={handleChange}
            required
            className={`w-full p-4 border rounded-lg text-lg ${formData.last_name ? "border-yellow-500" : "border-gray-300"}`}
          />
          <input
            type="email"
            name="email"
            placeholder="Введите email"
            value={formData.email}
            onChange={handleChange}
            required
            className={`w-full p-4 border rounded-lg text-lg ${formData.email ? "border-yellow-500" : "border-gray-300"}`}
          />

          {/* Поле пароля с глазиком */}
          <div className="relative w-full">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Введите пароль (минимум 8 символов)"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={8}
              className={`w-full p-4 border rounded-lg text-lg ${formData.password ? "border-yellow-500" : "border-gray-300"}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-4 top-4"
            >
              <img
                src={showPassword ? "/eye_open.svg" : "/eye_close.svg"}
                alt="Показать/скрыть пароль"
                className="h-6 w-6 cursor-pointer transition duration-300 hover:opacity-70"
              />
            </button>
          </div>

          {/* Поле подтверждения пароля с глазиком */}
          <div className="relative w-full">
            <input
              type={showConfirmPassword ? "text" : "password"}
              name="confirm_password"
              placeholder="Подтвердите пароль"
              value={formData.confirm_password}
              onChange={handleChange}
              required
              minLength={8}
              className={`w-full p-4 border rounded-lg text-lg ${
                formData.confirm_password
                  ? formData.password === formData.confirm_password
                    ? "border-green-500"
                    : "border-red-500"
                  : "border-gray-300"
              }`}
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-4 top-4"
            >
              <img
                src={showConfirmPassword ? "/eye_open.svg" : "/eye_close.svg"}
                alt="Показать/скрыть пароль"
                className="h-6 w-6 cursor-pointer transition duration-300 hover:opacity-70"
              />
            </button>
            {formData.confirm_password && formData.password !== formData.confirm_password && (
              <p className="text-red-500 text-xs mt-1">Пароли не совпадают</p>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-yellow-500 text-black text-lg py-4 rounded-lg hover:bg-yellow-600 transition-all"
          >
            Зарегистрироваться
          </button>

          {/* Кнопка "Вход" */}
          <p className="mt-3 text-center text-base">
            Уже есть аккаунт?{" "}
            <Link href="/login" className="text-blue-500 underline hover:text-blue-700">
              Войти
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}