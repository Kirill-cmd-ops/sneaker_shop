"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const SneakerGrid = ({ data, cols, cardHeight = "500px", imageHeight = "250px", fullWidth = false }) => {
  const [toast, setToast] = useState("");
  const [showSizeModal, setShowSizeModal] = useState(false);
  const [selectedSneaker, setSelectedSneaker] = useState(null);
  const [selectedSizeId, setSelectedSizeId] = useState(null);
  const [sneakerSizes, setSneakerSizes] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const savedPosition = sessionStorage.getItem("scrollPosition");
    if (savedPosition) {
      window.scrollTo(0, Number(savedPosition));
    }
  }, []);

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

  // Функция для получения размеров кроссовка
  const fetchSneakerSizes = async (sneakerId) => {
    try {
      const response = await fetch(`http://localhost:8006/api/v1/sneakers/${sneakerId}`);
      if (response.ok) {
        const data = await response.json();
        return data.sizes || [];
      }
      return [];
    } catch (error) {
      console.error("Ошибка загрузки размеров:", error);
      return [];
    }
  };

  // Функция для отображения toast-сообщения
  const showToast = (message, type = "info") => {
    setToast({ message, type });
    setTimeout(() => {
      setToast("");
    }, 3000);
  };

  // Функция добавления в избранное
  const addToFavorite = async (sneakerId, sizeId) => {
    try {
      const res = await favoriteRequest("/api/v1/favorite/sneakers/", {
        method: "POST",
        body: JSON.stringify({
          sneaker_id: sneakerId,
          size_id: sizeId
        }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const errorMessage = errorData.detail || "Ошибка при добавлении товара в избранное";
        throw new Error(errorMessage);
      }

      showToast("Товар успешно добавлен в избранное!", "success");
      return true;
    } catch (error) {
      console.error("Ошибка добавления в избранное:", error);
      showToast(error.message || "Ошибка при добавлении товара в избранное", "error");
      return false;
    }
  };

  // Обработчик клика на кнопку "В избранное"
  const handleAddToFavorite = async (e, sneakerId, sneakerName) => {
    e.stopPropagation();
    e.preventDefault();

    // Получаем размеры кроссовка
    const sizes = await fetchSneakerSizes(sneakerId);
    if (sizes.length === 0) {
      showToast("У данного товара нет доступных размеров", "error");
      return;
    }

    // Если только один размер - добавляем сразу
    if (sizes.length === 1) {
      const success = await addToFavorite(sneakerId, sizes[0].id);
      if (success) {
        // Можно добавить анимацию или изменение состояния кнопки
      }
    } else {
      // Если несколько размеров - показываем модальное окно
      setSelectedSneaker({ id: sneakerId, name: sneakerName });
      setSneakerSizes(sizes);
      setShowSizeModal(true);
      setSelectedSizeId(null);
    }
  };

  // Обработчик выбора размера в модальном окне
  const handleSizeSelect = (sizeId) => {
    setSelectedSizeId(sizeId);
  };

  // Обработчик подтверждения добавления в избранное
  const handleConfirmFavorite = async () => {
    if (!selectedSizeId) {
      showToast("Пожалуйста, выберите размер", "error");
      return;
    }

    const success = await addToFavorite(selectedSneaker.id, selectedSizeId);
    if (success) {
      setShowSizeModal(false);
      setSelectedSizeId(null);
      setSelectedSneaker(null);
    }
  };

  if (!data || !data.items)
    return <p className="text-center mt-10">Товары не найдены.</p>;

  return (
    <>
      {/* Toast-уведомление */}
      {toast && (
        <div className={`fixed top-4 left-1/2 transform -translate-x-1/2 px-4 py-2 rounded-md shadow-lg z-50 transition-all duration-300 ${
          toast.type === "error"
            ? "bg-red-500 text-white"
            : "bg-yellow-500 text-black"
        }`}>
          {toast.message}
        </div>
      )}

      {/* Сетка товаров */}
      <div className={`grid ${cols} gap-6 mt-6 ${fullWidth ? 'w-full' : 'justify-center w-full max-w-[1920px]'}`}>
        {data.items.map(({ id, name, price, brand, image_url }) => (
          <a
            key={id}
            href={`/details?sneakerId=${id}`}
            className="relative w-full text-center rounded-lg shadow-md transition-transform duration-300 hover:scale-105 p-4 bg-white block hover:border-2 hover:border-yellow-500"
            style={{ height: cardHeight }}
            onClick={() =>
              sessionStorage.setItem("scrollPosition", window.scrollY)
            }
          >
            <div className="group relative">
              <img
                src={`http://127.0.0.1:8005${image_url}`}
                alt={name}
                className="w-full object-cover rounded-md mx-auto transition-all duration-300"
                style={{ height: imageHeight }}
              />
              <div className="absolute inset-0 bg-white bg-opacity-30 flex flex-col items-center justify-center gap-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                {/* Кнопка "В корзину" */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    sessionStorage.setItem("scrollPosition", window.scrollY);
                    router.push(`/details?sneakerId=${id}`);
                  }}
                  className="w-40 bg-white border border-yellow-500 text-yellow-500 px-4 py-2 rounded-md transition-colors duration-300 hover:bg-yellow-500 hover:text-white font-medium"
                >
                  В корзину
                </button>

                {/* Кнопка "В избранное" */}
                <button
                  onClick={(e) => handleAddToFavorite(e, id, name)}
                  className="w-40 bg-white border border-yellow-500 text-yellow-500 px-4 py-2 rounded-md transition-colors duration-300 hover:bg-yellow-500 hover:text-white font-medium"
                >
                  В избранное
                </button>
              </div>
            </div>

            {/* Информация о товаре */}
            <div className="mt-4">
              <h2 className="text-lg text-gray-500 mb-1">
                {brand?.name || "Без бренда"}
              </h2>
              <h2 className="text-xl font-semibold text-gray-800 mb-2 line-clamp-2 min-h-[56px]">
                {name}
              </h2>
              <p className="text-xl text-gray-900">
                <span className="font-bold">{price} Br</span>
              </p>
            </div>
          </a>
        ))}
      </div>

      {/* Модальное окно для выбора размера */}
      {showSizeModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-md z-[100] flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full z-[110] shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-2xl font-bold text-gray-900">Выберите размер</h3>
              <button
                onClick={() => {
                  setShowSizeModal(false);
                  setSelectedSizeId(null);
                  setSelectedSneaker(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <p className="text-gray-600 mb-6 text-lg">{selectedSneaker?.name}</p>

            <div className="grid grid-cols-4 gap-3 mb-6">
              {sneakerSizes.map((size) => (
                <button
                  key={size.id}
                  onClick={() => handleSizeSelect(size.id)}
                  className={`px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
                    selectedSizeId === size.id
                      ? "bg-yellow-500 text-white transform scale-105 shadow-md"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-sm"
                  }`}
                >
                  {size.eu_size}
                </button>
              ))}
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleConfirmFavorite}
                disabled={!selectedSizeId}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-colors ${
                  selectedSizeId
                    ? "bg-yellow-500 text-white hover:bg-yellow-600"
                    : "bg-gray-300 text-gray-500 cursor-not-allowed"
                }`}
              >
                Добавить в избранное
              </button>
              <button
                onClick={() => {
                  setShowSizeModal(false);
                  setSelectedSizeId(null);
                  setSelectedSneaker(null);
                }}
                className="flex-1 bg-gray-100 text-gray-700 px-4 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
              >
                Отмена
              </button>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-200 text-center">
              <p className="text-sm text-gray-500">
                Товар будет добавлен в ваше избранное
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default SneakerGrid;