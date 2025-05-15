"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

export default function SneakerDetails() {
  const searchParams = useSearchParams();
  const sneakerId = searchParams.get("sneakerId");

  const [sneaker, setSneaker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1); // ✅ Добавлено состояние для количества

  /** Загружаем информацию о кроссовке */
  useEffect(() => {
    if (!sneakerId) return;

    setLoading(true);
    fetch(`http://localhost:8000/api/v1/sneakers/?sneakerId=${sneakerId}`)
      .then((res) => res.json())
      .then((data) => {
        const sneakerData = data.items?.find((s) => s.id.toString() === sneakerId);
        setSneaker(sneakerData || null);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Ошибка загрузки:", error);
        setLoading(false);
      });
  }, [sneakerId]);

  /** Уменьшение количества */
  const decreaseQuantity = () => {
    if (quantity > 1) setQuantity(quantity - 1);
  };

  /** Увеличение количества */
  const increaseQuantity = () => {
    setQuantity(quantity + 1);
  };

  if (loading) {
    return <p className="text-xl text-gray-600">Загрузка...</p>;
  }

  if (!sneaker) {
    return <p className="text-xl text-red-500">Кроссовок не найден.</p>;
  }

  return (
    <main className="relative flex flex-col min-h-screen bg-white text-black p-10">
      {/* Заголовок товара */}
      <h1 className="text-5xl font-bold text-neutral-600 mb-6">{sneaker.name}</h1>

      <div className="flex">
        {/* ✅ Изображение стало шире и закреплено слева */}
        <div className="absolute top-10 left-10">
          <img
            src={`http://localhost:8000${sneaker.image_url}`}
            alt={sneaker.name}
            className="w-[600px] h-auto object-cover rounded-md shadow-lg"
          />
        </div>

        {/* Описание товара */}
        <div className="flex-1 pl-[650px]">
            <p className="text-2xl text-gray-600 mt-4">{sneaker.name}</p>
          <p className="text-2xl text-gray-600 mt-4">{sneaker.description}</p>
          <p className="text-3xl font-bold text-black mt-2">{sneaker.price} Br</p>

          {/* ✅ Бренд и пол */}
          <p className="text-xl text-gray-500 mt-4">
            <span className="font-semibold text-black">Бренд:</span> {sneaker.brand.name}
          </p>
          <p className="text-xl text-gray-500 mt-2">
            <span className="font-semibold text-black">Пол:</span> {sneaker.gender}
          </p>

<p className="text-xl text-gray-500 mt-2">
  <span className="font-semibold text-black">Размеры:</span>{" "}
  {Array.isArray(sneaker.sizes) && sneaker.sizes.length > 0
    ? sneaker.sizes.map((s) => s.value).join(", ")
    : "Нет в наличии"}
</p>



          {/* ✅ Блок выбора количества */}
          <div className="flex items-center gap-6 mt-8">
            <button
              onClick={decreaseQuantity}
              className="w-12 h-12 text-2xl font-bold border-2 border-yellow-500 bg-white hover:bg-yellow-500 hover:text-white rounded-md transition-all"
            >
              -
            </button>
            <span className="text-3xl font-bold w-12 text-center">{quantity}</span>
            <button
              onClick={increaseQuantity}
              className="w-12 h-12 text-2xl font-bold border-2 border-yellow-500 bg-white hover:bg-yellow-500 hover:text-white rounded-md transition-all"
            >
              +
            </button>
          </div>

          {/* ✅ Кнопка "В корзину" */}
          <button
            className="mt-8 px-6 py-3 text-lg font-semibold text-black rounded-md border-2 border-yellow-500 bg-white hover:bg-yellow-500 hover:text-white transition-all"
          >
            В корзину
          </button>
        </div>
      </div>
    </main>
  );
}
