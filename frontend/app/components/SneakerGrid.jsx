"use client";
import { useEffect, useState } from "react";

const SneakerGrid = ({ data, cols }) => {
  useEffect(() => {
    const savedPosition = sessionStorage.getItem("scrollPosition");
    if (savedPosition) {
      window.scrollTo(0, Number(savedPosition)); // ✅ Восстанавливаем скролл
    }
  }, []);

  if (!data || !data.items) return <p>Товары не найдены.</p>;

  return (
    <div className={`grid ${cols} gap-x-6 gap-y-10 mt-6 justify-center`}>
      {data.items.map(({ id, name, price, brand, image_url }) => (
        <a
          key={id}
          href={`/details?sneakerId=${id}`} // ✅ Ссылка на страницу деталей
          className="relative w-[400px] h-[500px] text-center rounded-lg shadow-md transition-transform duration-300 hover:scale-105 p-4 bg-white block"
          onClick={() => sessionStorage.setItem("scrollPosition", window.scrollY)} // ✅ Сохраняем позицию скролла
        >
          <img
            src={`http://127.0.0.1:8000${image_url}`}
            alt={name}
            className="w-full h-[250px] object-cover rounded-md mx-auto transition-all duration-300"
          />

          <h2 className="text-2xl text-gray-500 mt-3">{brand?.name || "Без бренда"}</h2>
          <h2 className="text-2xl text-gray-500 mt-2">{name}</h2>
          <p className="text-xl text-gray-600 mt-2">
            <span className="font-bold text-black">{price}</span> Br
          </p>
        </a>
      ))}
    </div>
  );
};

export default SneakerGrid;
