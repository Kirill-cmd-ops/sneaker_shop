"use client";
import React, { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

function DetailsContent() {
  const searchParams = useSearchParams();
  const sneakerId = searchParams.get("sneakerId");

  const [sneaker, setSneaker] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSize, setSelectedSize] = useState(null);
  const [selectedSizeId, setSelectedSizeId] = useState(null);
  const [toastMessage, setToastMessage] = useState("");

  // Функция для запроса к API корзины с фиксированными заголовками
  const cartRequest = async (url, options = {}) => {
    const headers = {
      'Content-Type': 'application/json',
      'X-User-Role': 'User',
      'X-User-Id': '2',
      ...(options.headers || {}),
    };

    const fetchOptions = {
      ...options,
      headers,
      credentials: 'include',
    };

    const fullUrl = url.startsWith('http')
      ? url
      : `http://localhost:8004${url.startsWith('/') ? '' : '/'}${url}`;

    return fetch(fullUrl, fetchOptions);
  };

  // Функция для запроса к API избранного с фиксированными заголовками
  const favoriteRequest = async (url, options = {}) => {
    const headers = {
      'Content-Type': 'application/json',
      'X-User-Role': 'User',
      'X-User-Id': '2',
      ...(options.headers || {}),
    };

    const fetchOptions = {
      ...options,
      headers,
      credentials: 'include',
    };

    const fullUrl = url.startsWith('http')
      ? url
      : `http://localhost:8003${url.startsWith('/') ? '' : '/'}${url}`;

    return fetch(fullUrl, fetchOptions);
  };

  useEffect(() => {
    if (!sneakerId) return;

    const fetchSneakerDetails = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://127.0.0.1:8006/api/v1/sneakers/${sneakerId}`);
        if (!response.ok) {
          throw new Error("Ошибка загрузки данных");
        }
        const data = await response.json();
        setSneaker(data);
      } catch (err) {
        console.error("Ошибка загрузки:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSneakerDetails();
  }, [sneakerId]);

  // Функция для показа toast-сообщения
  const showToastMessage = (message) => {
    setToastMessage(message);
    setTimeout(() => setToastMessage(""), 3000);
  };

  // Исправленный обработчик добавления в корзину
  const handleAddToCart = async () => {
    if (!selectedSizeId) {
      showToastMessage("Пожалуйста, выберите размер");
      return;
    }

    try {
      // Формируем данные в соответствии с CartSneakerCreate
      const requestData = {
        sneaker_id: parseInt(sneakerId),
        size_id: selectedSizeId
      };

      console.log("Отправка данных в корзину:", requestData);

      // Используем cartRequest
      const res = await cartRequest("/api/v1/cart/sneakers/", {
        method: "POST",
        body: JSON.stringify(requestData),
      });

      console.log("Ответ корзины:", res.status, res.statusText);

      if (res.ok || res.status === 201 || res.status === 200 || res.status === 204) {
        showToastMessage("Товар успешно добавлен в корзину!");
        return;
      }

      // Получаем детали ошибки
      let errorMessage = "Ошибка при добавлении товара в корзину";
      try {
        const errorData = await res.json();
        console.log("Детали ошибки:", errorData);

        // Форматируем сообщение об ошибке
        if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (Array.isArray(errorData)) {
          errorMessage = errorData.map(err => err.msg || err.loc?.join('.')).join(', ');
        } else if (typeof errorData === 'object') {
          errorMessage = JSON.stringify(errorData);
        }
      } catch (e) {
        errorMessage = await res.text().catch(() => `Ошибка ${res.status}: ${res.statusText}`);
      }
      throw new Error(errorMessage);

    } catch (error) {
      console.error("Ошибка при добавлении в корзину:", error);
      showToastMessage(error.message || "Ошибка при добавлении товара в корзину");
    }
  };

  const handleFavoriteClick = async () => {
    // Проверяем, выбран ли размер
    if (!selectedSizeId) {
      showToastMessage("Пожалуйста, выберите размер");
      return;
    }

    try {
      // Формируем данные для отправки
      const requestData = {
        sneaker_id: parseInt(sneakerId),
        size_id: selectedSizeId
      };

      console.log("Отправка данных в избранное:", requestData);

      // Используем функцию favoriteRequest
      const res = await favoriteRequest("/api/v1/favorite/sneakers/", {
        method: "POST",
        body: JSON.stringify(requestData),
      });

      console.log("Ответ сервера:", res.status, res.statusText);

      if (res.ok || res.status === 201 || res.status === 200 || res.status === 204) {
        showToastMessage("Товар добавлен в избранное!");
        return;
      }

      // Обработка ошибок
      let errorMessage = "Ошибка при добавлении товара в избранное";
      try {
        const errorData = await res.json();
        console.log("Детали ошибки избранного:", errorData);
        errorMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
      } catch (e) {
        errorMessage = await res.text().catch(() => `Ошибка ${res.status}: ${res.statusText}`);
      }
      throw new Error(errorMessage);

    } catch (error) {
      console.error("Ошибка при добавлении в избранное:", error);
      showToastMessage(error.message || "Ошибка при добавлении товара в избранное");
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="text-red-500">Ошибка: {error}</p>;
  if (!sneaker) return <p>Кроссовки не найдены.</p>;

  return (
    <div className="max-w-7xl mx-auto mt-40 flex gap-20 items-start">
      {/* Toast-уведомление */}
      {toastMessage && (
        <div className="fixed top-5 left-1/2 transform -translate-x-1/2 bg-yellow-500 text-black px-6 py-3 rounded-md shadow-lg z-50">
          {toastMessage}
        </div>
      )}

      <div className="w-3/5">
        <img
          src={`http://127.0.0.1:8005${sneaker.image_url}`}
          alt={sneaker.name}
          className="w-full h-[500px] object-cover rounded-md"
        />
        <p className="text-xl font-semibold text-gray-700 mt-6">Размеры в наличии:</p>
        <div className="mt-4 flex flex-wrap gap-3">
          {sneaker.sizes?.map((size) => (
            <button
              key={size.id}
              onClick={() => {
                setSelectedSize(size.eu_size);
                setSelectedSizeId(size.id);
                console.log("Выбран размер:", size.eu_size, "ID:", size.id);
              }}
              className={`px-6 py-2 rounded-md text-lg font-medium ${
                selectedSize === size.eu_size
                  ? "bg-yellow-500 text-black"
                  : "bg-gray-200 text-black"
              } transition-colors duration-200 hover:bg-yellow-500 hover:text-black`}
            >
              {size.eu_size}
            </button>
          )) || <span className="text-gray-400 text-lg">Размеры отсутствуют</span>}
        </div>
      </div>

      <div className="w-2/5 mt-6">
        <h1 className="text-6xl font-bold text-gray-900">
          {sneaker.brand?.name} {sneaker.name}
        </h1>
        <p className="text-2xl font-semibold text-gray-800 mt-4">
          {sneaker.gender || "Не указан"} кроссовки
        </p>
        <p className="text-2xl font-semibold text-gray-800 mt-4">
          Страна производства:{" "}
          <strong>{sneaker.country?.name || "Не указано"}</strong>
        </p>

        <p className="text-2xl font-bold text-gray-800 mt-6">Цвета:</p>
        <div className="flex flex-wrap gap-3 mt-2">
          {sneaker.colors?.map((color) => (
            <span
              key={color.id}
              className="px-5 py-2 bg-gray-300 rounded-md text-lg"
            >
              {color.name}
            </span>
          )) || <span className="text-gray-500 text-lg">Не указаны</span>}
        </div>

        <p className="text-2xl font-bold text-gray-800 mt-6">Материалы:</p>
        <div className="flex flex-wrap gap-3 mt-2">
          {sneaker.materials?.map((material) => (
            <span
              key={material.id}
              className="px-5 py-2 bg-gray-300 rounded-md text-lg"
            >
              {material.name}
            </span>
          )) || <span className="text-gray-500 text-lg">Не указаны</span>}
        </div>

        <p className="text-2xl font-bold text-gray-800 mt-6">Описание:</p>
        <p className="text-xl text-gray-700 mt-2">
          {sneaker.description || "Описание отсутствует."}
        </p>

        <p className="text-5xl font-bold text-black mt-8">{sneaker.price} Br</p>

        <div className="flex items-center gap-4 mt-6">
          <button
            onClick={handleAddToCart}
            className="px-6 py-3 rounded-md text-lg font-bold bg-gray-800 text-white hover:bg-gray-900 transition-colors duration-200 w-full"
          >
            В корзину
          </button>

          <button
            className="px-3 py-2 rounded-md bg-gray-200 hover:bg-gray-300 transition-colors duration-200"
            onClick={handleFavoriteClick}
          >
            <img src="/heart.svg" alt="Избранное" className="h-9 w-9" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default function DetailsPage() {
  return (
    <Suspense fallback={<p>Загрузка деталей...</p>}>
      <DetailsContent />
    </Suspense>
  );
}