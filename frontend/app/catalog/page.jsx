"use client";
import { useState, useEffect } from "react";
import SneakerGrid from "../components/SneakerGrid";

export default function CatalogPage() {
      const [sneakers, setSneakers] = useState([]);
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
      fetchSneakers("http://localhost:8000/api/v1/sneakers/?page=1&limit=30&order=asc", setSneakers),
    ]).then(() => setLoading(false));
  }, []);

  return (
    <main className="flex flex-col items-start justify-start min-h-screen bg-white text-black p-6">
      <button className="px-9 py-4 bg-yellow-500 text-black font-semibold rounded-full transition-all duration-300 hover:bg-yellow-600 hover:shadow-lg hover:brightness-75 self-start mt-[100px]">
        Фильтры
      </button>
      <SneakerGrid sneakers={sneakers} cols="grid-cols-5" />
    </main>
  );
}


