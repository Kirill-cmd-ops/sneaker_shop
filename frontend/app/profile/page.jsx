"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
      const fetchProfileData = async () => {
        try {
          // Функция для отправки запроса с fallback на разные порты
          const makeRequest = async (url) => {
            try {
              const response = await fetch(url, {
                method: "GET",
                credentials: "include",
                headers: {
                  "Content-Type": "application/json",
                },
              });
              return { response, error: null };
            } catch (error) {
              return { response: null, error };
            }
          };

          // Пробуем сначала через Kong (8000), если не работает - напрямую через auth_service (8002)
          let result = await makeRequest("http://localhost:8000/api/v1/auth/me");
          if (result.error) {
            console.log("Kong (8000) недоступен, пробуем прямой доступ к auth_service (8002)");
            result = await makeRequest("http://localhost:8002/api/v1/auth/me");
          }

          if (result.error) {
            throw new Error("Не удалось подключиться к серверу. Проверьте, что сервисы запущены.");
          }

          const res = result.response;

        if (!res.ok) {
          if (res.status === 401) {
            setError("Вы не авторизованы. Пожалуйста, войдите в систему.");
            setTimeout(() => {
              router.push("/login");
            }, 2000);
            return;
          }
          throw new Error("Ошибка получения профиля");
        }

        const data = await res.json();
        setProfile(data);
      } catch (error) {
        console.error("Ошибка получения профиля:", error);
        setError("Не удалось загрузить профиль. Пожалуйста, попробуйте позже.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, [router]);

  if (loading) {
    return (
      <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-10">
        <p className="text-xl text-gray-600">Загрузка профиля...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-10">
        <div className="max-w-xl p-10 bg-white border-4 border-red-500 shadow-lg rounded-lg text-center">
          <p className="text-red-500 text-xl mb-4">{error}</p>
          <Link href="/login" className="text-blue-500 underline hover:text-blue-700">
            Перейти на страницу входа
          </Link>
        </div>
      </main>
    );
  }

  if (!profile) {
    return (
      <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-10">
        <p className="text-xl text-gray-600">Не удалось получить профиль пользователя.</p>
        <Link href="/login" className="mt-4 text-blue-500 underline hover:text-blue-700">
          Войти
        </Link>
      </main>
    );
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-10">
      <div className="max-w-2xl w-full p-10 bg-white border-4 border-yellow-500 shadow-lg rounded-lg">
        <h1 className="text-4xl font-bold mb-8 text-center text-neutral-600">Профиль пользователя</h1>
        
        <div className="space-y-6">
          <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-500 mb-1">ID пользователя</p>
            <p className="text-xl font-semibold text-gray-800">{profile.id}</p>
          </div>

          <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-500 mb-1">Имя</p>
            <p className="text-xl font-semibold text-gray-800">{profile.first_name || "Не указано"}</p>
          </div>

          <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-500 mb-1">Фамилия</p>
            <p className="text-xl font-semibold text-gray-800">{profile.last_name || "Не указано"}</p>
          </div>

          <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-500 mb-1">Email</p>
            <p className="text-xl font-semibold text-gray-800">{profile.email || "Не указано"}</p>
          </div>

          {profile.is_verified !== undefined && (
            <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-500 mb-1">Статус верификации</p>
              <p className={`text-xl font-semibold ${profile.is_verified ? "text-green-600" : "text-yellow-600"}`}>
                {profile.is_verified ? "✓ Подтвержден" : "⚠ Не подтвержден"}
              </p>
            </div>
          )}

          <div className="flex gap-4 mt-8">
            <Link
              href="/"
              className="flex-1 bg-gray-200 text-gray-700 text-center py-3 rounded-lg hover:bg-gray-300 transition-all font-semibold"
            >
              На главную
            </Link>
            <Link
              href="/catalog"
              className="flex-1 bg-yellow-500 text-black text-center py-3 rounded-lg hover:bg-yellow-600 transition-all font-semibold"
            >
              В каталог
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
