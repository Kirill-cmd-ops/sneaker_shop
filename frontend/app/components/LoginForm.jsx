"use client";
import { useState } from "react";
import Link from "next/link";

export default function LoginForm() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
  event.preventDefault();
  setMessage("");

  try {
    console.log("Отправляемые данные:", formData);

    const formBody = new URLSearchParams();
    formBody.append("username", formData.username);
    formBody.append("password", formData.password);
    formBody.append("grant_type", "password");

    const response = await fetch("http://localhost:8000/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formBody.toString(),
    });

    console.log("Ответ сервера:", response);

    if (response.status === 204) {
      setMessage("✅ Успешный вход! Перенаправляем...");
      setTimeout(() => {
        window.location.href = "/";
      }, 1000);
      return;
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    setMessage("✅ Вход выполнен успешно!");
    setTimeout(() => {
      window.location.href = "/";
    }, 1000);

  } catch (error) {
    console.error("Ошибка запроса:", error);
    setMessage(`❌ Ошибка: ${error.message}`);
  }
};


  return (
    <div className="flex justify-center items-center min-h-screen w-full">
      <div className="w-full max-w-xl p-10 bg-white border-4 border-yellow-500 shadow-lg rounded-lg text-black">
        <h2 className="text-3xl font-bold mb-8 text-center">Вход в аккаунт</h2>
        {message && <p className="text-red-500 mb-6 text-center">{message}</p>}
        <form onSubmit={handleSubmit} className="space-y-8">
          <input
            type="text"
            name="username"
            placeholder="Введите имя пользователя"
            value={formData.username}
            onChange={handleChange}
            required
            className={`w-full p-5 border rounded-lg text-xl ${formData.username ? "border-yellow-500" : "border-gray-300"}`}
          />
          <div className="relative w-full">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Введите пароль"
              value={formData.password}
              onChange={handleChange}
              required
              className={`w-full p-5 border rounded-lg text-xl ${formData.password ? "border-yellow-500" : "border-gray-300"}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-5 top-5"
            >
              <img
                src={showPassword ? "/eye_open.svg" : "/eye_close.svg"}
                alt="Показать/скрыть пароль"
                className="h-8 w-8 cursor-pointer transition duration-300 hover:opacity-70"
              />
            </button>
          </div>

          <button
            type="submit"
            className="w-full bg-yellow-500 text-black text-xl py-5 rounded-lg hover:bg-yellow-600 transition-all"
          >
            Войти
          </button>

          <p className="mt-4 text-center text-lg">
            Еще нет аккаунта?{" "}
            <Link href="/register" className="text-blue-500 underline hover:text-blue-700">
              Создать
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
