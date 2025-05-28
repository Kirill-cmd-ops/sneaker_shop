"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

function CartPage() {
  const [cartItems, setCartItems] = useState([]);
  const [toastMessage, setToastMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  // Функция для отображения toast‑уведомления
  const showToast = (message) => {
    setToastMessage(message);
    setTimeout(() => setToastMessage(""), 3000);
  };

  // Запрос списка товаров корзины при монтировании компонента
  useEffect(() => {
    async function fetchCart() {
      try {
        const res = await fetch("http://localhost:8000/api/v1/cart", {
          method: "GET",
          credentials: "include",
        });
        if (!res.ok) {
          throw new Error("Ошибка при загрузке корзины");
        }
        const data = await res.json();
        if (Array.isArray(data)) {
          setCartItems(data);
        } else if (data.items) {
          setCartItems(data.items);
        } else {
          setCartItems([]);
        }
      } catch (err) {
        setError(err.message || "Не удалось загрузить корзину");
      } finally {
        setLoading(false);
      }
    }
    fetchCart();
  }, []);

  // Обработчик добавления товара в избранное через /api/v1/favorite_add/
  const handleAddToFavorites = async (itemId, e) => {
    e?.stopPropagation();
    e?.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/v1/favorite_add/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sneaker_id: itemId }),
      });
      if (!res.ok) {
        throw new Error("Ошибка при добавлении товара в избранное");
      }
      showToast("Товар успешно добавлен в избранное!");
    } catch (err) {
      console.error(err);
      showToast("Ошибка при добавлении товара в избранное");
    }
  };

  // Обработчик удаления товара из корзины через /api/v1/cart_delete/{associationId}
  const handleRemoveItem = async (associationId, e) => {
    e?.stopPropagation();
    e?.preventDefault();
    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/cart_delete/${associationId}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );
      if (!res.ok) {
        throw new Error("Ошибка при удалении товара");
      }
      setCartItems((prev) =>
        prev.filter((item) => item.associationId !== associationId)
      );
      showToast("Товар удалён из корзины");
    } catch (err) {
      console.error(err);
      showToast("Ошибка при удалении товара из корзины");
    }
  };

  if (loading) return <p className="text-center mt-20">Загрузка...</p>;
  if (error)
    return <p className="text-center mt-20 text-red-600">{error}</p>;
  if (cartItems.length === 0)
    return (
      <p className="text-center mt-20 text-xl text-gray-500">
        Ваша корзина пуста
      </p>
    );

  return (
    <div className="max-w-7xl mx-auto mt-24 p-4">
      {/* Toast-уведомление */}
      {toastMessage && (
        <div className="fixed top-5 left-1/2 transform -translate-x-1/2 bg-yellow-500 text-black px-6 py-3 rounded-md shadow-lg z-50">
          {toastMessage}
        </div>
      )}
      <h1 className="text-4xl font-bold mb-6">Корзина</h1>
      <div className="flex gap-6 items-start">
        {/* Список товаров */}
        <div className="flex-grow space-y-6 -ml-4">
          {cartItems.map((item) => (
            <div
              key={item.id}
              className="flex flex-col md:flex-row items-center border-2 border-transparent rounded p-4 transition-transform duration-300 hover:scale-[1.03] hover:border-yellow-500"
            >
              {/* Изображение товара */}
              <div className="md:w-1/4">
                <img
                  src={`http://localhost:8000${item.image_url}`}
                  alt={item.name}
                  className="w-full h-auto object-cover rounded"
                />
              </div>
              {/* Информация о товаре */}
              <div className="mt-4 md:mt-0 md:ml-4 flex-grow">
                <h2 className="text-2xl font-bold">{item.name}</h2>
                <p className="text-xl text-gray-600">{item.price} Br</p>
                {/* Кнопки управления */}
                <div className="mt-2 flex space-x-4">
                  <button
                    onClick={(e) => handleAddToFavorites(item.id, e)}
                    className="p-2 bg-transparent"
                  >
                    <img
                      src="/heart.svg"
                      alt="Избранное"
                      className="w-6 h-6 filter grayscale"
                    />
                  </button>
                  <button
                    onClick={(e) => handleRemoveItem(item.associationId, e)}
                    className="p-2 bg-transparent"
                  >
                    <img
                      src="/trash.svg"
                      alt="Мусорка"
                      className="w-6 h-6 filter grayscale"
                    />
                  </button>
                </div>
              </div>
              {/* Кнопка "Купить" */}
              <div className="mt-4 md:mt-0 md:ml-4">
                <button
                  onClick={() => {}}
                  className="w-full text-lg font-bold bg-yellow-500 text-white px-6 py-3 rounded"
                >
                  Купить
                </button>
              </div>
            </div>
          ))}
        </div>
        {/* Кнопка "Заказать" справа, почти вверху */}
        <div>
          <button
            onClick={() => router.push("/checkout")}
            className="px-8 py-4 bg-yellow-500 text-white text-xl font-bold rounded transition-colors duration-300 hover:bg-yellow-600 active:bg-yellow-700"
          >
            Заказать
          </button>
        </div>
      </div>
    </div>
  );
}

export default CartPage;
