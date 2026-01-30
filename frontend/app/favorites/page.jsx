"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

function FavoritePage() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [newSizeId, setNewSizeId] = useState(null);
  const [availableSizesMap, setAvailableSizesMap] = useState({});
  const [sneakersData, setSneakersData] = useState({});
  const [sizesData, setSizesData] = useState({});
  const [brandsData, setBrandsData] = useState({});
  const router = useRouter();

  // Функция для запроса к API с фиксированными заголовками
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

  // Функция для получения информации о бренде по ID
  const fetchBrandInfo = async (brandId) => {
    if (brandsData[brandId]) {
      return typeof brandsData[brandId] === 'object'
        ? brandsData[brandId]
        : { id: brandId, name: brandsData[brandId] };
    }

    try {
      const response = await fetch(`http://localhost:8006/api/v1/brands/${brandId}`);

      if (response.ok) {
        const data = await response.json();

        let brandData;
        if (typeof data === 'string') {
          brandData = { id: brandId, name: data };
        } else if (typeof data === 'object' && data !== null && data.name) {
          brandData = data;
        } else if (typeof data === 'object' && data !== null) {
          brandData = { ...data, id: brandId };
        } else {
          brandData = { id: brandId, name: String(data) };
        }

        setBrandsData(prev => ({ ...prev, [brandId]: brandData }));
        return brandData;
      }
      return { id: brandId, name: `Бренд ${brandId}` };
    } catch (error) {
      console.error("Ошибка загрузки информации о бренде:", error);
      return { id: brandId, name: `Бренд ${brandId}` };
    }
  };

  // Функция для получения информации о размере (ИСПРАВЛЕНА)
  const fetchSizeInfo = async (sizeId) => {
    if (sizesData[sizeId]) {
      return sizesData[sizeId];
    }

    try {
      const response = await fetch(`http://localhost:8006/api/v1/sizes/${sizeId}`);

      if (response.ok) {
        // Эндпоинт возвращает строку с размером
        const eu_size = await response.text();

        // Создаем объект с размером
        const sizeData = {
          id: sizeId,
          eu_size: eu_size.trim()
        };

        setSizesData(prev => ({ ...prev, [sizeId]: sizeData }));
        return sizeData;
      }
      return { id: sizeId, eu_size: `Размер ${sizeId}` };
    } catch (error) {
      console.error("Ошибка загрузки информации о размере:", error);
      return { id: sizeId, eu_size: `Размер ${sizeId}` };
    }
  };

  // Функция для получения информации о кроссовке
  const fetchSneakerInfo = async (sneakerId) => {
    if (sneakersData[sneakerId]) {
      return sneakersData[sneakerId];
    }

    try {
      const response = await fetch(`http://localhost:8006/api/v1/sneakers/${sneakerId}`);
      if (response.ok) {
        const data = await response.json();
        setSneakersData(prev => ({ ...prev, [sneakerId]: data }));

        // Загружаем информацию о бренде если есть
        if (data.brand_id) {
          fetchBrandInfo(data.brand_id);
        }

        return data;
      }
      return null;
    } catch (error) {
      console.error("Ошибка загрузки информации о кроссовке:", error);
      return null;
    }
  };

  // Загрузка всех данных о кроссовках и размерах из избранного
  const loadAllFavoriteData = async (favoriteItems) => {
    const sneakerIds = favoriteItems
      .map(item => item.sneaker_id || item.sneaker?.id)
      .filter(Boolean);

    const sizeIds = favoriteItems
      .map(item => item.size_id)
      .filter(Boolean);

    console.log("Загружаем данные для кроссовок:", sneakerIds);
    console.log("Загружаем данные для размеров:", sizeIds);

    // Загружаем данные для всех кроссовок параллельно
    const sneakerPromises = sneakerIds.map(sneakerId => fetchSneakerInfo(sneakerId));
    const sizePromises = sizeIds.map(sizeId => fetchSizeInfo(sizeId));

    await Promise.all([...sneakerPromises, ...sizePromises]);
  };

  // Получение данных о всех размерах кроссовка
  const fetchSneakerSizes = async (sneakerId) => {
    if (availableSizesMap[sneakerId]) {
      return availableSizesMap[sneakerId];
    }

    try {
      const response = await fetch(`http://localhost:8006/api/v1/sneakers/${sneakerId}`);
      if (response.ok) {
        const data = await response.json();
        const sizes = data.sizes || [];
        setAvailableSizesMap(prev => ({ ...prev, [sneakerId]: sizes }));
        return sizes;
      }
      return [];
    } catch (error) {
      console.error("Ошибка загрузки размеров:", error);
      return [];
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      setLoading(true);
      const res = await favoriteRequest("/api/v1/favorite/", {
        method: "GET",
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Ошибка сервера:", errorText);
        throw new Error(`Ошибка загрузки: ${res.status}`);
      }

      const data = await res.json();
      console.log("Получены избранные товары:", data);

      // Сохраняем избранное
      setFavorites(data || []);

      // Загружаем дополнительную информацию о кроссовках и размерах
      if (data && data.length > 0) {
        await loadAllFavoriteData(data);
      }

    } catch (err) {
      console.error("Ошибка при загрузке избранного:", err);
      setError("Не удалось загрузить избранные товары");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFavorite = async (favoriteSneakerId, e) => {
    e.stopPropagation();
    e.preventDefault();

    if (!confirm("Удалить товар из избранного?")) {
      return;
    }

    try {
      console.log("Удаляем из избранного ID:", favoriteSneakerId);

      const res = await favoriteRequest(`/api/v1/favorite/sneakers/${favoriteSneakerId}`, {
        method: "DELETE",
      });

      console.log("Статус ответа при удалении:", res.status);

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Текст ошибки:", errorText);

        try {
          const errorData = JSON.parse(errorText);
          console.error("JSON ошибки:", errorData);
          throw new Error(errorData.detail || `Ошибка при удалении товара: ${res.status}`);
        } catch {
          throw new Error(`Ошибка при удалении товара: ${res.status} - ${errorText}`);
        }
      }

      // Успешно удалено - обновляем список
      const deletedItem = favorites.find(fav => fav.id === favoriteSneakerId);
      setFavorites((prev) => prev.filter((fav) => fav.id !== favoriteSneakerId));

      // Очищаем кэш если нужно
      if (deletedItem) {
        const sneakerId = deletedItem.sneaker_id || deletedItem.sneaker?.id;
        const sizeId = deletedItem.size_id;

        // Проверяем, используется ли еще этот кроссовок в других избранных
        const isSneakerStillUsed = favorites.some(fav =>
          fav.id !== favoriteSneakerId &&
          (fav.sneaker_id === sneakerId || fav.sneaker?.id === sneakerId)
        );

        if (!isSneakerStillUsed && sneakerId) {
          setSneakersData(prev => {
            const newData = { ...prev };
            delete newData[sneakerId];
            return newData;
          });
        }

        // Проверяем, используется ли еще этот размер в других избранных
        const isSizeStillUsed = favorites.some(fav =>
          fav.id !== favoriteSneakerId && fav.size_id === sizeId
        );

        if (!isSizeStillUsed && sizeId) {
          setSizesData(prev => {
            const newData = { ...prev };
            delete newData[sizeId];
            return newData;
          });
        }
      }

      console.log("Товар успешно удален из избранного");

    } catch (err) {
      console.error("Ошибка при удалении:", err);
      alert(err.message || "Ошибка при удалении товара");
    }
  };

  const handleUpdateSize = async (favoriteSneakerId) => {
    if (!newSizeId) {
      alert("Пожалуйста, выберите размер");
      return;
    }

    try {
      console.log("Изменяем размер для записи ID:", favoriteSneakerId, "новый размер ID:", newSizeId);

      const res = await favoriteRequest(`/api/v1/favorite/sneakers/${favoriteSneakerId}`, {
        method: "PUT",
        body: JSON.stringify({
          size_id: newSizeId
        }),
      });

      console.log("Статус ответа при изменении размера:", res.status);

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Текст ошибки:", errorText);
        throw new Error("Ошибка при изменении размера");
      }

      // Загружаем информацию о новом размере
      await fetchSizeInfo(newSizeId);

      // Обновляем список избранного
      await fetchFavorites();
      setEditingItem(null);
      setNewSizeId(null);
      alert("Размер успешно изменен!");
    } catch (err) {
      console.error(err);
      alert("Ошибка при изменении размера");
    }
  };

  const handleStartEdit = async (item) => {
    setEditingItem(item.id);
    setNewSizeId(item.size_id);
    const sneakerId = item.sneaker_id || item.sneaker?.id;
    if (sneakerId) {
      await fetchSneakerSizes(sneakerId);
    }
  };

  const handleRefresh = () => {
    setError(null);
    fetchFavorites();
  };

  // Обработчик ошибок загрузки изображения
  const handleImageError = (e) => {
    e.target.style.display = 'none';
    const fallbackDiv = document.createElement('div');
    fallbackDiv.className = 'w-full h-full bg-gray-200 flex items-center justify-center';
    fallbackDiv.innerHTML = `
      <div class="text-center">
        <svg class="w-12 h-12 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p class="text-sm text-gray-500 mt-2">Нет изображения</p>
      </div>
    `;
    e.target.parentNode.appendChild(fallbackDiv);
    e.target.onerror = null;
  };

  // Получение информации о кроссовке для отображения
  const getSneakerInfo = (item) => {
    const sneakerId = item.sneaker_id || item.sneaker?.id;
    if (!sneakerId) return null;

    return sneakersData[sneakerId] || null;
  };

  // Получение информации о бренде для отображения
  const getBrandInfo = (item) => {
    const sneakerInfo = getSneakerInfo(item);
    if (sneakerInfo?.brand_id) {
      return brandsData[sneakerInfo.brand_id];
    }
    return null;
  };

  // Получение отображаемого размера
  const getDisplaySize = (item) => {
    const sizeId = item.size_id;
    if (!sizeId) return "Нет размера";

    const sizeData = sizesData[sizeId];
    if (sizeData) {
      return sizeData.eu_size || "Нет размера";
    }

    // Если данные о размере еще не загружены, загружаем их
    fetchSizeInfo(sizeId);
    return "Загрузка...";
  };

  // Получение отображаемого бренда
  const getDisplayBrand = (item) => {
    const brandInfo = getBrandInfo(item);
    if (brandInfo) {
      if (typeof brandInfo === 'string') {
        return brandInfo;
      } else if (typeof brandInfo === 'object') {
        return brandInfo.name || "Без бренда";
      }
    }

    const sneakerInfo = getSneakerInfo(item);
    if (sneakerInfo?.brand_id && !brandsData[sneakerInfo.brand_id]) {
      fetchBrandInfo(sneakerInfo.brand_id);
    }

    return "Загрузка...";
  };

  // Пустое состояние
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 pt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-20">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-64 mx-auto mb-6"></div>
              <div className="h-4 bg-gray-200 rounded w-48 mx-auto"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 pt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-20">
            <div className="inline-block p-8 bg-white rounded-2xl shadow-lg">
              <div className="text-red-500 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.282 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Произошла ошибка</h2>
              <p className="text-gray-600 mb-6">{error}</p>
              <button
                onClick={handleRefresh}
                className="inline-flex items-center px-6 py-3 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600 transition-colors"
              >
                Попробовать снова
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Пустое состояние - нет избранных товаров
  if (favorites.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 pt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-20">
            <div className="inline-block p-12 bg-white rounded-3xl shadow-xl">
              <div className="mb-8">
                <div className="w-24 h-24 text-gray-300 mx-auto">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-24 w-24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
              </div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Ваше избранное пусто</h1>
              <p className="text-xl text-gray-600 mb-8 max-w-md mx-auto">
                Сохраняйте понравившиеся товары, чтобы не потерять их. Нажмите на сердечко в карточке товара, чтобы добавить его сюда.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Есть избранные товары
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        {/* Заголовок */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Избранное
          </h1>
          <p className="text-lg text-gray-600">
            {favorites.length} {favorites.length === 1 ? 'товар' :
              favorites.length > 1 && favorites.length < 5 ? 'товара' : 'товаров'} в избранном
          </p>
        </div>

        {/* Сетка товаров */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8">
          {favorites.map((item) => {
            const isEditing = editingItem === item.id;
            const sneakerId = item.sneaker_id || item.sneaker?.id;
            const sneakerInfo = getSneakerInfo(item);
            const availableSizes = availableSizesMap[sneakerId] || [];
            const displaySize = getDisplaySize(item);
            const displayBrand = getDisplayBrand(item);

            // Данные для отображения
            const displayName = sneakerInfo?.name || item.name || "Неизвестная модель";
            const displayPrice = sneakerInfo?.price || item.price || "0";
            const displayImage = sneakerInfo?.image_url || item.image_url || "";

            return (
              <div
                key={item.id}
                className="group relative bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300"
              >
                {/* Кнопка удаления */}
                <button
                  onClick={(e) => handleDeleteFavorite(item.id, e)}
                  className="absolute top-4 right-4 z-10 w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-red-50 hover:text-red-600"
                  title="Удалить из избранного"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                </button>

                {/* Изображение */}
                <div
                  className="relative h-64 cursor-pointer overflow-hidden bg-gray-100"
                  onClick={() => {
                    if (sneakerId) {
                      sessionStorage.setItem("scrollPosition", window.scrollY);
                      router.push(`/details?sneakerId=${sneakerId}`);
                    }
                  }}
                >
                  {displayImage ? (
                    <img
                      src={`http://localhost:8005${displayImage}`}
                      alt={displayName}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                      onError={handleImageError}
                    />
                  ) : (
                    <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                      <div className="text-center">
                        <svg className="w-12 h-12 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <p className="text-sm text-gray-500 mt-2">Нет изображения</p>
                      </div>
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>

                {/* Информация о товаре */}
                <div className="p-6">
                  {/* Бренд и название */}
                  <div className="mb-4">
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-1">
                      {displayBrand}
                    </p>
                    <h3 className="text-xl font-semibold text-gray-900 line-clamp-2 min-h-[56px]">
                      {displayName}
                    </h3>
                  </div>

                  {/* Размер */}
                  <div className="mb-6">
                    {isEditing ? (
                      <div className="space-y-4">
                        <div>
                          <p className="text-sm text-gray-600 mb-2">
                            Текущий размер: <span className="font-bold">{displaySize}</span>
                          </p>
                          {availableSizes.length > 0 ? (
                            <>
                              <p className="text-sm text-gray-600 mb-3">Новый размер:</p>
                              <div className="flex flex-wrap gap-2 max-h-24 overflow-y-auto p-1">
                                {availableSizes.map((size) => (
                                  <button
                                    key={size.id}
                                    onClick={() => setNewSizeId(size.id)}
                                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                                      newSizeId === size.id
                                        ? "bg-yellow-500 text-white shadow-md"
                                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                    }`}
                                  >
                                    {size.eu_size}
                                  </button>
                                ))}
                              </div>
                              <div className="flex gap-2 mt-4">
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleUpdateSize(item.id);
                                  }}
                                  className="flex-1 bg-yellow-500 text-white py-2 rounded-lg font-semibold hover:bg-yellow-600 transition-colors disabled:opacity-50"
                                  disabled={!newSizeId || newSizeId === item.size_id}
                                >
                                  Сохранить
                                </button>
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setEditingItem(null);
                                    setNewSizeId(null);
                                  }}
                                  className="flex-1 bg-gray-100 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
                                >
                                  Отмена
                                </button>
                              </div>
                            </>
                          ) : (
                            <p className="text-sm text-gray-500 text-center py-2">Загрузка размеров...</p>
                          )}
                        </div>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="text-sm text-gray-600">Размер</p>
                            <p className="text-lg font-bold text-gray-900">{displaySize}</p>
                          </div>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleStartEdit(item);
                            }}
                            className="text-sm text-yellow-600 hover:text-yellow-700 font-medium underline"
                          >
                            Изменить
                          </button>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Цена и кнопка */}
                  <div className="border-t border-gray-100 pt-4">
                    <div className="flex justify-between items-center mb-4">
                      <div>
                        <p className="text-sm text-gray-600">Цена</p>
                        <p className="text-2xl font-bold text-gray-900">
                          {displayPrice} Br
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        if (sneakerId) {
                          sessionStorage.setItem("scrollPosition", window.scrollY);
                          router.push(`/details?sneakerId=${sneakerId}`);
                        }
                      }}
                      disabled={!sneakerId}
                      className={`w-full py-3 rounded-xl font-semibold transition-all hover:shadow-lg flex items-center justify-center gap-2 ${
                        sneakerId
                          ? "bg-yellow-500 text-white hover:bg-yellow-600"
                          : "bg-gray-300 text-gray-500 cursor-not-allowed"
                      }`}
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                      </svg>
                      <span>В корзину</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default FavoritePage;