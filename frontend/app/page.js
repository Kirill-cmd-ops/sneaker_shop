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
              className="w-full object-cove shadow-md"
            />
            <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>

          <h1 className="text-4xl font-bold text-neutral-600 mt-7 mb-6">Новинки</h1>


<div className="grid grid-cols-5 gap-6 mt-6">
  {sneakers.map(({ id, name, price, brand, gender, image_url }) => (
    <div key={id} className="w-[450px] h-[500px] text-center transition-transform duration-300 hover:scale-105">
      {/* Добавили плавное увеличение */}
      <img
        src={`http://localhost:8000${image_url}`}
        alt={name}
        className="w-120 h-80 object-cover mx-auto"
      />
      <h2 className="text-3xl text-gray-500 mt-3">{brand.name}</h2>
      <h2 className="text-3xl text-gray-500 mt-2">{name}</h2>

      <p className="text-3xl text-gray-600 mt-2">
        <span className="font-bold text-black">{price}</span> Br
      </p>
    </div>
  ))}
</div>



          {/* Кнопка */}
          <button
            className="mt-8 mb-[200px] px-8 py-3 text-lg font-semibold text-black rounded-full border-2 border-black
                       bg-white hover:bg-neutral-200 transition-colors duration-300"
          >
            Показать больше
          </button>

<div className="w-full flex flex-col gap-20 pl-[100px] mb-[200px]">
  <div className="relative w-[600px] h-[900px] group">
    <img src="/home_banner_nike.jpg" alt="Каталог кроссовок" className="w-full h-full object-cover  shadow-md" />
    <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300 "></div>
  </div>

  <div className="relative w-[600px] h-[900px] group">
    <img src="/home_banner_puma.jpg" alt="Каталог кроссовок" className="w-full h-full object-cover  shadow-md" />
    <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  </div>

  <div className="relative w-[600px] h-[900px] group">
    <img src="/home_banner_vans.jpg" alt="Каталог кроссовок" className="w-full h-full object-cover shadow-md" />
    <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  </div>

  <div className="relative w-[600px] h-[900px] group">
    <img src="/home_banner_adidas.jpg" alt="Каталог кроссовок" className="w-full h-full object-cover shadow-md" />
    <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  </div>
</div>

        </>
      )}
    </main>
  );
}
