"use client";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const SneakerDetails = () => {
  const searchParams = useSearchParams();
  const sneakerId = searchParams.get("sneakerId");

  const [sneaker, setSneaker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSize, setSelectedSize] = useState(null);
  const [addedToCart, setAddedToCart] = useState(false);

  useEffect(() => {
    if (!sneakerId) return;

    const fetchSneakerDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/sneaker/${sneakerId}`);
        if (!response.ok) throw new Error("Ошибка загрузки данных");

        const data = await response.json();
        setSneaker(data);
      } catch (error) {
        setError(error.message);
        console.error("Ошибка загрузки:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSneakerDetails();
  }, [sneakerId]);

  const handleAddToCart = () => {
    if (!selectedSize) return;

    setAddedToCart(true);
    setTimeout(() => setAddedToCart(false), 3000);
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="text-red-500">Ошибка: {error}</p>;
  if (!sneaker) return <p>Кроссовки не найдены.</p>;

  return (
    <div className="max-w-7xl mx-auto mt-40 flex gap-20 items-start">
      <div className="w-3/5">
        <img
          src={`http://127.0.0.1:8000${sneaker.image_url}`}
          alt={sneaker.name}
          className="w-full h-[500px] object-cover rounded-md"
        />

        <p className="text-xl font-semibold text-gray-700 mt-6">Размеры в наличии:</p>

        <div className="mt-4 flex flex-wrap gap-3">
          {sneaker.sizes?.map((size) => (
            <button
              key={size.id}
              onClick={() => setSelectedSize(size.eu_size)}
              className={`px-6 py-2 rounded-md text-lg font-medium ${
                selectedSize === size.eu_size ? "bg-yellow-500 text-black" : "bg-gray-200 text-black"
              } transition-colors duration-200 hover:bg-yellow-500 hover:text-black`}
            >
              {size.eu_size}
            </button>
          )) || <span className="text-gray-400 text-lg">Размеры отсутствуют</span>}
        </div>
      </div>

      <div className="w-2/5 mt-6">
        <h1 className="text-6xl font-bold text-gray-900">{sneaker.brand?.name} {sneaker.name}</h1>
        <p className="text-2xl font-semibold text-gray-800 mt-4">{sneaker.gender || "Не указан"} кроссовки</p>
        <p className="text-2xl font-semibold text-gray-800 mt-4">Страна производства: <strong>{sneaker.country?.name || "Не указано"}</strong></p>

        <p className="text-2xl font-bold text-gray-800 mt-6">Цвета:</p>
        <div className="flex flex-wrap gap-3 mt-2">
          {sneaker.colors?.map((color) => (
            <span key={color.id} className="px-5 py-2 bg-gray-300 rounded-md text-lg">{color.name}</span>
          )) || <span className="text-gray-500 text-lg">Не указаны</span>}
        </div>

        <p className="text-2xl font-bold text-gray-800 mt-6">Материалы:</p>
        <div className="flex flex-wrap gap-3 mt-2">
          {sneaker.materials?.map((material) => (
            <span key={material.id} className="px-5 py-2 bg-gray-300 rounded-md text-lg">{material.name}</span>
          )) || <span className="text-gray-500 text-lg">Не указаны</span>}
        </div>

        <p className="text-2xl font-bold text-gray-800 mt-6">Описание:</p>
        <p className="text-xl text-gray-700 mt-2">{sneaker.description || "Описание отсутствует."}</p>

        <p className="text-5xl font-bold text-black mt-8">{sneaker.price} Br</p>

        <button
          onClick={handleAddToCart}
          className={`w-full mt-6 px-6 py-3 rounded-md text-lg font-bold ${
            addedToCart ? "bg-yellow-500 text-black" : "bg-gray-800 text-white hover:bg-gray-900"
          } transition-colors duration-200`}
        >
          {selectedSize ? (addedToCart ? "Добавлено в корзину" : "В корзину") : "Выберите размер"}
        </button>
      </div>
    </div>
  );
};

export default SneakerDetails;
