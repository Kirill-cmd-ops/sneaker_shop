"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginForm() {
  const router = useRouter();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Проверяем, авторизован ли пользователь при загрузке
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/me", {
        method: "GET",
        credentials: "include",
      });

      if (response.ok) {
        const userData = await response.json();
        console.log("Пользователь уже авторизован:", userData);

        // Проверяем, админ ли это (проверяем по username или email)
        const isAdmin = userData.email === "howertwik@gmail.com" ||
                       userData.username === "howertwik@gmail.com" ||
                       userData.email === "admin" ||
                       userData.username === "admin";

        if (isAdmin) {
          console.log("Пользователь админ, редирект на /managements");
          // Сохраняем данные для страницы управления
          localStorage.setItem("userRole", "Admin");
          localStorage.setItem("userId", userData.id || "2");
          localStorage.setItem("userEmail", userData.email || userData.username);
          localStorage.setItem("user", JSON.stringify({
            username: userData.username,
            email: userData.email,
            isAuthenticated: true,
            isAdmin: true
          }));

          router.push("/managements");
        } else {
          router.push("/");
        }
      }
    } catch (error) {
      // Игнорируем ошибки проверки авторизации
    }
  };

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");
    setIsLoading(true);

    try {
      const formBody = new URLSearchParams();
      formBody.append("username", formData.username);
      formBody.append("password", formData.password);
      formBody.append("grant_type", "password");

      console.log("Отправка запроса авторизации для:", formData.username);

      // Функция для отправки запроса с fallback на разные порты
      const makeRequest = async (url) => {
        try {
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "Accept": "application/json"
            },
            body: formBody.toString(),
            credentials: "include",
          });
          return { response, error: null };
        } catch (error) {
          return { response: null, error };
        }
      };

      // Пробуем сначала через Kong (8000), если не работает - напрямую через auth_service (8002)
      let result = await makeRequest("http://localhost:8000/api/v1/auth/login");
      if (result.error || !result.response) {
        console.log("Kong (8000) недоступен, пробуем прямой доступ к auth_service (8002)");
        result = await makeRequest("http://localhost:8002/api/v1/auth/login");
      }

      if (result.error || !result.response) {
        throw new Error("Не удалось подключиться к серверу. Проверьте, что сервисы запущены.");
      }

      const response = result.response;
      console.log("Ответ сервера:", response.status, response.statusText);

      if (response.ok || response.status === 204) {
        // Проверяем, что куки установились
        await new Promise(resolve => setTimeout(resolve, 200)); // Увеличиваем задержку

        // Проверяем авторизацию через эндпоинт /me
        try {
          const meResponse = await fetch("http://localhost:8000/api/v1/auth/me", {
            method: "GET",
            credentials: "include",
          });

          if (meResponse.ok) {
            const userData = await meResponse.json();
            console.log("Пользователь авторизован, данные:", userData);

            // Проверяем, является ли пользователь админом
            const isAdminUser = formData.username === "howertwik@gmail.com" ||
                              formData.username === "admin" ||
                              userData.email === "howertwik@gmail.com" ||
                              userData.username === "howertwik@gmail.com";

            console.log("isAdminUser:", isAdminUser, "username:", formData.username);

            // Сохраняем информацию о пользователе в localStorage для фронтенда
            localStorage.setItem("user", JSON.stringify({
              username: userData.username || formData.username,
              email: userData.email || formData.username,
              isAuthenticated: true,
              isAdmin: isAdminUser
            }));

            // Сохраняем данные для страницы управления
            if (isAdminUser) {
              localStorage.setItem("userRole", "Admin");
              localStorage.setItem("userId", userData.id || "2");
              localStorage.setItem("userEmail", userData.email || formData.username);

              console.log("Сохранены данные админа в localStorage");
            }
          } else {
            console.log("Не удалось получить данные через /me, но авторизация успешна");
            // Если /me не работает, все равно проверяем username
            const isAdminUser = formData.username === "howertwik@gmail.com" || formData.username === "admin";

            localStorage.setItem("user", JSON.stringify({
              username: formData.username,
              email: formData.username,
              isAuthenticated: true,
              isAdmin: isAdminUser
            }));

            if (isAdminUser) {
              localStorage.setItem("userRole", "Admin");
              localStorage.setItem("userId", "2");
              localStorage.setItem("userEmail", formData.username);
            }
          }
        } catch (meError) {
          console.log("Ошибка при запросе /me:", meError);
          // Если /me не работает, проверяем по username
          const isAdminUser = formData.username === "howertwik@gmail.com" || formData.username === "admin";

          localStorage.setItem("user", JSON.stringify({
            username: formData.username,
            email: formData.username,
            isAuthenticated: true,
            isAdmin: isAdminUser
          }));

          if (isAdminUser) {
            localStorage.setItem("userRole", "Admin");
            localStorage.setItem("userId", "2");
            localStorage.setItem("userEmail", formData.username);
          }
        }

        setIsSuccess(true);

        // Проверяем, является ли пользователь админом
        const isAdminUser = formData.username === "howertwik@gmail.com" || formData.username === "admin";

        console.log("Перенаправление. isAdminUser:", isAdminUser);

        if (isAdminUser) {
          setMessage("✅ Успешный вход! Перенаправляем в панель управления...");

          // Даем больше времени для сохранения данных
          setTimeout(() => {
            console.log("Редирект на /managements");
            router.push("/managements");
          }, 1000);
        } else {
          setMessage("✅ Успешный вход! Перенаправляем на главную...");

          setTimeout(() => {
            router.push("/");
          }, 1000);
        }
        return;
      }

      if (!response.ok) {
        setIsSuccess(false);
        let errorText = "Ошибка авторизации";
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
      setMessage(`❌ Ошибка: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen w-full">
      <div className="w-full max-w-xl p-10 bg-white border-4 border-yellow-500 shadow-lg rounded-lg text-black">
        <h2 className="text-3xl font-bold mb-8 text-center">Вход в аккаунт</h2>
        {message && (
          <p className={`mb-6 text-center text-lg ${isSuccess ? "text-green-600" : "text-red-500"}`}>
            {message}
          </p>
        )}
        <form onSubmit={handleSubmit} className="space-y-8">
          <input
            type="text"
            name="username"
            placeholder="Введите email (howertwik@gmail.com для админа)"
            value={formData.username}
            onChange={handleChange}
            required
            disabled={isLoading}
            className={`w-full p-5 border rounded-lg text-xl ${formData.username ? "border-yellow-500" : "border-gray-300"} ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
          />
          <div className="relative w-full">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Введите пароль (Qwerty12@ для админа)"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={isLoading}
              className={`w-full p-5 border rounded-lg text-xl ${formData.password ? "border-yellow-500" : "border-gray-300"} ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-5 top-5"
              disabled={isLoading}
            >
              <img
                src={showPassword ? "/eye_open.svg" : "/eye_close.svg"}
                alt="Показать/скрыть пароль"
                className={`h-8 w-8 cursor-pointer transition duration-300 hover:opacity-70 ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
              />
            </button>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full text-xl py-5 rounded-lg transition-all ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-yellow-500 hover:bg-yellow-600"}`}
          >
            {isLoading ? "⏳ Входим..." : "Войти"}
          </button>

          <p className="mt-4 text-center text-lg">
            Еще нет аккаунта?{" "}
            <Link
              href="/register"
              className={`text-blue-500 underline hover:text-blue-700 ${isLoading ? "pointer-events-none opacity-50" : ""}`}
            >
              Создать
            </Link>
          </p>

          {/* Подсказка для тестирования */}
          <div className="mt-6 p-4 bg-gray-100 rounded-lg">
            <p className="text-sm text-gray-600 mb-2">Для тестирования:</p>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Админ: <span className="font-semibold">howertwik@gmail.com</span> / <span className="font-semibold">Qwerty12@</span></li>
              <li className="text-xs text-gray-500">(откроется панель управления)</li>
              <li>• Обычный пользователь: любой другой email</li>
              <li className="text-xs text-gray-500">(откроется главная страница)</li>
            </ul>
          </div>
        </form>
      </div>
    </div>
  );
}