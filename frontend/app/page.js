"use client";
import { useState, useEffect } from "react";
import SneakerGrid from "./components/SneakerGrid";

export default function Home() {
  const [newsneakers, setNewSneakers] = useState([]);
  const [nikesneakers, setNikeSneakers] = useState([]);
  const [pumasneakers, setPumaSneakers] = useState([]);
  const [vanssneakers, setVansSneakers] = useState([]);
  const [adidassneakers, setAdidasSneakers] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchSneakers = async (url, setter) => {
    try {
      const res = await fetch(url);
      const data = await res.json();
      setter(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
    }
  };

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchSneakers("http://localhost:8000/api/v1/sneakers/?page=1&limit=10&sort_by=created_at&order=desc", setNewSneakers),
      fetchSneakers("http://localhost:8000/api/v1/sneakers/?page=1&limit=8&brand_name=nike&order=asc", setNikeSneakers),
      fetchSneakers("http://localhost:8000/api/v1/sneakers/?page=1&limit=8&brand_name=puma&order=asc", setPumaSneakers),
      fetchSneakers("http://localhost:8000/api/v1/sneakers/?page=1&limit=8&brand_name=vans&order=asc", setVansSneakers),
      fetchSneakers("http://localhost:8000/api/v1/sneakers/?page=1&limit=8&brand_name=adidas&order=asc", setAdidasSneakers),
    ]).then(() => setLoading(false));
  }, []);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black">
      {loading ? (
        <p className="text-xl text-gray-600">Загрузка...</p>
      ) : (
        <>
          <div className="relative w-full my-6 group">
            <img src="/home_banner.jpg" alt="Каталог кроссовок" className="w-full object-cover shadow-md" />
          </div>

          <h1 className="text-4xl font-bold text-neutral-600 mt-7 mb-6">Новинки</h1>
          <SneakerGrid sneakers={newsneakers} cols="grid-cols-5" />

          <button className="mt-8 mb-[200px] px-8 py-3 text-lg font-semibold text-black rounded-full border-2 border-black bg-white hover:bg-neutral-200 transition-colors duration-300">
            Показать больше
          </button>

          <div className="w-full flex flex-col gap-16 items-start pl-[100px] mb-[150px]">
            {[
              { src: "/home_banner_nike.jpg", brand: "Nike", sneakers: nikesneakers },
              { src: "/home_banner_puma.jpg", brand: "Puma", sneakers: pumasneakers },
              { src: "/home_banner_vans.jpg", brand: "Vans", sneakers: vanssneakers },
              { src: "/home_banner_adidas.jpg", brand: "Adidas", sneakers: adidassneakers },
            ].map(({ src, brand, sneakers }) => (
              <div key={brand} className="flex w-full gap-12 items-start mb-[100px]">

                <div className="relative w-[600px] h-[900px]">
                  <img src={src} alt={`Каталог кроссовок ${brand}`} className="w-full h-full object-cover shadow-md" />
                  <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </div>

                <div className="flex-1 flex flex-col">
                  <h1 className="text-5xl font-bold text-black mb-6">{brand}</h1>
                  <SneakerGrid sneakers={sneakers} cols="grid-cols-4" />
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </main>
  );
}
