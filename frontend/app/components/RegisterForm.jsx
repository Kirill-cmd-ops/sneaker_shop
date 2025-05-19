"use client";
import { useState } from "react";

export default function RegisterForm() {
  const [formData, setFormData] = useState({ first_name: "", last_name: "", email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setMessage("✅ Успешная регистрация! Проверьте почту.");
      } else {
        const errorData = await response.json();
        setMessage(`❌ Ошибка: ${errorData.detail}`);
      }
    } catch (error) {
      setMessage("❌ Ошибка сети, попробуйте позже.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
  <div className="max-w-xl p-10 bg-white border-4 border-yellow-500 shadow-lg rounded-lg text-black">
    <h2 className="text-3xl font-bold mb-8 text-center">Регистрация</h2>
    {message && <p className="text-red-500 mb-6 text-center">{message}</p>}
    <form onSubmit={handleSubmit} className="space-y-8">
      <input
        type="text"
        name="first_name"
        placeholder="Введите имя"
        value={formData.first_name}
        onChange={handleChange}
        required
        className={`w-full p-5 border rounded-lg text-xl ${formData.first_name ? "border-yellow-500" : "border-gray-300"}`}
      />
      <input
        type="text"
        name="last_name"
        placeholder="Введите фамилию"
        value={formData.last_name}
        onChange={handleChange}
        required
        className={`w-full p-5 border rounded-lg text-xl ${formData.last_name ? "border-yellow-500" : "border-gray-300"}`}
      />
      <input
        type="email"
        name="email"
        placeholder="Введите email"
        value={formData.email}
        onChange={handleChange}
        required
        className={`w-full p-5 border rounded-lg text-xl ${formData.email ? "border-yellow-500" : "border-gray-300"}`}
      />

      {/* Поле пароля с глазиком */}
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
        Зарегистрироваться
      </button>
    </form>
  </div>
</div>

  );
}
