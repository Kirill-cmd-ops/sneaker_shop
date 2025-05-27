"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

function FavoritePage() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/favorite", {
          method: "GET",
          credentials: "include", // Отправляем cookie с JWT
        });
        if (!res.ok) {
          throw new Error("Ошибка при загрузке избранных товаров");
        }
        const data = await res.json();
        setFavorites(data);
      } catch (err) {
        setError(err.message || "Не удалось загрузить избранное");
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

  if (loading) {
    return <p className="text-center mt-20">Загрузка...</p>;
  }

  if (error) {
    return <p className="text-center mt-20 text-red-600">{error}</p>;
  }

  if (favorites.length === 0) {
    return (
      <p className="text-center mt-20 text-lg text-gray-600">
        Нет избранных товаров
      </p>
    );
  }

  return (
    <div className="max-w-7xl mx-auto mt-24">
      <h1 className="text-4xl font-bold text-gray-900 mb-10">Избранное</h1>

      {/* Карточки в виде сетки */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-10 mt-6 justify-center">
        {favorites.map((item) => (
          <a
            key={item.id}
            href={`/details?sneakerId=${item.id}`}
            className="group relative w-[400px] h-[500px] text-center rounded-lg shadow-md transition-transform duration-300 hover:scale-105 p-4 bg-white block hover:border-2 hover:border-yellow-500"
            onClick={() => sessionStorage.setItem("scrollPosition", window.scrollY)}
          >
            {/* Контейнер для изображения с позицией relative */}
            <div className="relative">
              <img
                src={`http://localhost:8000${item.image_url}`}
                alt={item.name}
                className="w-full h-[250px] object-cover rounded-md mx-auto transition-all duration-300"
              />
              {/* Inline SVG-иконка, желтого цвета, появляется в правом верхнем углу при наведении */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="absolute top-0 right-0 w-10 h-10 p-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-yellow-500"
              >
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                  2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09
                  3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0
                  3.78-3.4 6.86-8.55 11.54L12 21.35z" />
              </svg>
            </div>
            {/* Информация о товаре */}
            <h2 className="text-2xl text-gray-500 mt-3">
              {item.brand?.name || "Без бренда"}
            </h2>
            <h2 className="text-2xl text-gray-500 mt-2">{item.name}</h2>
            <p className="text-xl text-gray-600 mt-2">
              <span className="font-bold text-black">{item.price}</span> Br
            </p>
            {/* Кнопка "Купить" с желтым фоном, белым текстом,
                которая при наведении расширяется, и перенаправляет на страницу деталей */}
            <button
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                router.push(`/details?sneakerId=${item.id}`);
              }}
              className="w-40 mt-4 bg-yellow-500 text-white px-4 py-2 rounded-md transition-all duration-300 hover:w-full hover:bg-yellow-600"
            >
              В корзину
            </button>
          </a>
        ))}
      </div>
    </div>
  );
}

export default FavoritePage;
