"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [sneakers, setSneakers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/sneakers/?page=1&limit=10&sort_by=created_at&order=desc")
      .then((res) => res.json())
      .then((data) => setSneakers(data))
      .catch((error) => console.error("Ошибка загрузки данных:", error))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black">
      {loading ? null : (
        <>
<div className="relative w-full my-6 group">
  <img
    src="/home_banner.jpg"
    alt="Каталог кроссовок"
    className="w-full object-cover rounded-lg shadow-md"
  />
  {/* Затемняющий слой */}
  <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg"></div>
</div>




          <h1 className="text-4xl font-bold text-neutral-600 mt-7 mb-6">Новинки</h1>

          <div className="grid grid-cols-5 gap-4 mt-6">
            {sneakers.map(({ id, name, price, brand, gender, image_url }) => (
              <div key={id} className="p-4 rounded-md shadow-md text-center">
                <img
                  src={`http://localhost:8000${image_url}`}
                  alt={name}
                  className="w-70 h-70 object-cover mx-auto"
                />
                <h2 className="text-xl font-semibold mt-2">{name}</h2>
                <p className="text-lg text-gray-600">Цена: {price} руб.</p>
                <p className="text-md text-gray-500">Бренд: {brand.name}</p>
                <p className="text-sm font-medium mt-1 text-blue-600">{gender}</p>
              </div>
            ))}
          </div>

          <button
            className="mt-8 px-8 py-3 text-lg font-semibold text-black rounded-full border-2 border-black
                       bg-white hover:bg-neutral-200 transition-colors duration-300"
          >
            Показать больше
          </button>
        </>
      )}
    </main>
  );
}
