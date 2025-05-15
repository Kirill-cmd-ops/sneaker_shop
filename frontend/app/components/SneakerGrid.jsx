"use client";
import { useEffect, useState } from "react";

const SneakerGrid = ({ data, cols }) => {
  if (!data || !data.items) return <p>Товары не найдены.</p>;

  return (
    <div className={`grid ${cols} gap-x-6 gap-y-10 mt-6 justify-center`}>
      {data.items.map(({ id, name, price, brand, image_url, country, colors, materials }) => (
        <a
          key={id}
          href={`/details?sneakerId=${id}`} // ✅ Ссылка на страницу деталей
          className="w-[400px] h-[500px] text-center rounded-lg shadow-md transition-transform duration-300 hover:scale-105 p-4 bg-white block"
        >
          <img
            src={`http://127.0.0.1:8000${image_url}`}
            alt={name}
            className="w-full h-[250px] object-cover rounded-md mx-auto"
          />
          <h2 className="text-2xl text-gray-500 mt-3">{brand?.name || "Без бренда"}</h2>
          <h2 className="text-2xl text-gray-500 mt-2">{name}</h2>
          <p className="text-xl text-gray-600 mt-2">
            <span className="font-bold text-black">{price}</span> Br
          </p>

          {/* Страна производства */}
          <p className="text-lg text-gray-600 mt-2">
            Страна производства: <strong>{country?.name || "Не указано"}</strong>
          </p>

          {/* Цвета кроссовок */}
          <p className="text-lg text-gray-600 mt-2">Доступные цвета:</p>
          <div className="flex flex-wrap gap-2 mt-2">
            {colors?.map((color) => (
              <span key={color.id} className="px-3 py-1 bg-gray-200 rounded-md">
                {color.name}
              </span>
            )) || <span className="text-gray-400">Не указаны</span>}
          </div>

          {/* Материалы кроссовок */}
          <p className="text-lg text-gray-600 mt-2">Материалы:</p>
          <div className="flex flex-wrap gap-2 mt-2">
            {materials?.map((material) => (
              <span key={material.id} className="px-3 py-1 bg-gray-200 rounded-md">
                {material.name}
              </span>
            )) || <span className="text-gray-400">Не указаны</span>}
          </div>
        </a>
      ))}
    </div>
  );
};

export default SneakerGrid;
