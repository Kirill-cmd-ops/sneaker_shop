"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Получаем данные профиля с сервера.
    const fetchProfileData = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/profile", {
          method: "GET",
          credentials: "include",  // Обязательно передать cookie с JWT
          cache: "no-store",
        });

        if (!res.ok) {
          // Если не авторизован, можно перенаправить на страницу регистрации или логина.
          router.push("/register");
          return;
        }

        const data = await res.json();
        setProfile(data);
      } catch (error) {
        console.error("Ошибка получения профиля:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, [router]);

  if (loading) return <p>Загрузка...</p>;
  if (!profile) return <p>Не удалось получить профиль пользователя.</p>;

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">Профиль пользователя</h1>
      <div className="bg-white shadow rounded p-4">
        <p><strong>ID:</strong> {profile.id}</p>
        <p><strong>Имя:</strong> {profile.first_name}</p>
        <p><strong>Фамилия:</strong> {profile.last_name}</p>
        <p><strong>Email:</strong> {profile.email}</p>
      </div>
    </div>
  );
}
