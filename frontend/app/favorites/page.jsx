"use client";

import React, { useState, useEffect } from "react";

function FavoritePage() {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    // Загружаем избранные товары (можно заменить на запрос к API)
    const storedFavorites = JSON.parse(localStorage.getItem("favorites")) || [];
    setFavorites(storedFavorites);
  }, []);

  if (favorites.length === 0) {
    return <p className="text-center mt-20 text-lg text-gray-600">Нет избранных товаров</p>;
  }

  return (
    <div className="max-w-7xl mx-auto mt-20">
      <h1 className="text-4xl font-bold text-gray-900 mb-10">Избранное</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {favorites.map((item) => (
          <div key={item.id} className="bg-white shadow-md rounded-lg p-4">
            <img
              src={item.image}
              alt={item.name}
              className="w-full h-48 object-cover rounded-md"
            />
            <h2 className="text-xl font-semibold text-gray-800 mt-4">{item.name}</h2>
            <p className="text-gray-600">{item.price} Br</p>
            <button
              className="mt-4 bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
              onClick={() => {
                const updatedFavorites = favorites.filter((fav) => fav.id !== item.id);
                setFavorites(updatedFavorites);
                localStorage.setItem("favorites", JSON.stringify(updatedFavorites));
              }}
            >
              Удалить из избранного
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FavoritePage;
