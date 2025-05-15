"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

export default function SneakerDetails() {
  const searchParams = useSearchParams();
  const sneakerId = searchParams.get("sneakerId");

  const [sneaker, setSneaker] = useState(null);
  const [loading, setLoading] = useState(true);

  /** Загружаем информацию о кроссовке */
  useEffect(() => {
    if (!sneakerId) return;

    setLoading(true);
    fetch(`http://localhost:8000/api/v1/sneakers/?sneakerId=${sneakerId}`)
      .then((res) => res.json())
      .then((data) => {
        const sneakerData = data.items?.find((s) => s.id.toString() === sneakerId); // ✅ Берём кроссовок из `items`
        setSneaker(sneakerData || null);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Ошибка загрузки:", error);
        setLoading(false);
      });
  }, [sneakerId]);

  if (loading) {
    return <p className="text-xl text-gray-600">Загрузка...</p>;
  }

  if (!sneaker) {
    return <p className="text-xl text-red-500">Кроссовок не найден.</p>;
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-10">
      <h1 className="text-5xl font-bold text-neutral-600 mb-6">{sneaker.name}</h1>

      <img
        src={`http://localhost:8000${sneaker.image_url}`}
        alt={sneaker.name}
        className="w-[500px] h-[500px] object-cover rounded-md shadow-lg"
      />

      <p className="text-2xl text-gray-600 mt-4">{sneaker.description}</p>
      <p className="text-3xl font-bold text-black mt-2">{sneaker.price} Br</p>

      <button
        onClick={() => window.history.back()}
        className="mt-8 px-6 py-3 text-lg font-semibold text-black rounded-md border border-black bg-white hover:bg-neutral-200 transition-all"
      >
        Вернуться назад
      </button>
    </main>
  );
}
