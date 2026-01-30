"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

function CartPage() {
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [newSizeId, setNewSizeId] = useState(null);
  const [availableSizesMap, setAvailableSizesMap] = useState({});
  const [sneakersData, setSneakersData] = useState({});
  const [sizesData, setSizesData] = useState({});
  const [brandsData, setBrandsData] = useState({});
  const [toastMessage, setToastMessage] = useState("");
  const [updatingItems, setUpdatingItems] = useState({});
  const router = useRouter();

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

    console.log('Cart запрос:', { url: fullUrl, method: options.method || 'GET' });
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

  // Функция для получения информации о бренде по ID
  const fetchBrandInfo = async (brandId) => {
    if (brandsData[brandId]) {
      console.log("Бренд уже загружен:", brandId, brandsData[brandId]);
      return typeof brandsData[brandId] === 'object'
        ? brandsData[brandId]
        : { id: brandId, name: brandsData[brandId] };
    }

    try {
      console.log("Загружаем бренд по ID:", brandId);
      const response = await fetch(`http://localhost:8006/api/v1/brands/${brandId}`);

      if (response.ok) {
        const data = await response.json();
        console.log("Бренд получен:", data, "тип:", typeof data);

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
      console.error("Не удалось загрузить бренд:", brandId);
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
      console.log("Загружаем размер по ID:", sizeId);
      const response = await fetch(`http://localhost:8006/api/v1/sizes/${sizeId}`);

      if (response.ok) {
        // Эндпоинт возвращает строку с размером (например: "42")
        const eu_size = await response.text();
        console.log("Размер получен:", eu_size, "тип:", typeof eu_size);

        // Создаем объект с размером
        const sizeData = {
          id: sizeId,
          eu_size: eu_size.trim()
        };

        setSizesData(prev => ({ ...prev, [sizeId]: sizeData }));
        return sizeData;
      }
      console.error("Не удалось загрузить размер:", sizeId);
      return { id: sizeId, eu_size: `Размер ${sizeId}` };
    } catch (error) {
      console.error("Ошибка загрузки информации о размере:", error);
      return { id: sizeId, eu_size: `Размер ${sizeId}` };
    }
  };

  // Загрузка всех данных о брендах и размерах из корзины
  const loadAllCartData = async (cartItems) => {
    if (!cartItems || !Array.isArray(cartItems)) return;

    const brandIds = [...new Set(cartItems
      .map(item => item.brand_id)
      .filter(Boolean))];

    const sizeIds = [...new Set(cartItems
      .map(item => item.size_id)
      .filter(Boolean))];

    console.log("Загружаем бренды для корзины:", brandIds);
    console.log("Загружаем размеры для корзины:", sizeIds);

    const brandPromises = brandIds.map(brandId => fetchBrandInfo(brandId));
    const sizePromises = sizeIds.map(sizeId => fetchSizeInfo(sizeId));

    await Promise.allSettled([...brandPromises, ...sizePromises]);
  };

  // Функция для отображения toast-уведомления
  const showToast = (message) => {
    setToastMessage(message);
    setTimeout(() => setToastMessage(""), 3000);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const res = await cartRequest("/api/v1/cart/", {
        method: "GET",
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Ошибка сервера корзины:", errorText);
        throw new Error(`Ошибка загрузки корзины: ${res.status}`);
      }

      const data = await res.json();
      console.log("Получены данные корзины:", data);

      setCartData(data);

      if (data) {
        const cartItems = getCartItems(data);
        console.log("Извлеченные товары корзины:", cartItems);

        if (cartItems.length > 0) {
          await loadAllCartData(cartItems);
        }
      }

    } catch (err) {
      console.error("Ошибка при загрузке корзины:", err);
      setError("Не удалось загрузить корзину");
    } finally {
      setLoading(false);
    }
  };

  // Получение списка товаров в корзине
  const getCartItems = (data = cartData) => {
    if (!data) return [];

    console.log("Парсим данные корзины для извлечения items:", data);

    if (data["Кроссовки"] && typeof data["Кроссовки"] === 'object') {
      const cartObject = data["Кроссовки"];
      console.log("Содержимое Кроссовки:", cartObject);

      if (cartObject.sneaker_associations && Array.isArray(cartObject.sneaker_associations)) {
        console.log("Нашли sneaker_associations массив:", cartObject.sneaker_associations);

        return cartObject.sneaker_associations.map(item => {
          const associationId = item.id;
          const sneakerData = item.sneaker || {};

          console.log("Элемент sneaker_associations:", {
            associationId,
            sneakerData,
            size_id: item.size_id,
            quantity: item.quantity
          });

          return {
            association_id: associationId,
            size_id: item.size_id,
            quantity: item.quantity || 1,
            cart_id: item.cart_id,
            name: sneakerData.name,
            price: sneakerData.price,
            brand_id: sneakerData.brand_id,
            image_url: sneakerData.image_url,
            sneaker_id: sneakerData.id,
            created_at: sneakerData.created_at,
            id: associationId,
            cart_sneaker_id: associationId
          };
        });
      }

      if (cartObject.sneakers && Array.isArray(cartObject.sneakers)) {
        console.log("Нашли sneakers массив:", cartObject.sneakers);
        return cartObject.sneakers.map(item => {
          const cartSneakerId = item.id || item.cart_sneaker_id;
          console.log("Элемент sneakers:", item, "cartSneakerId:", cartSneakerId);
          return {
            ...item,
            association_id: item.id,
            cart_sneaker_id: cartSneakerId,
            quantity: item.quantity || 1
          };
        });
      }
    }

    if (Array.isArray(data)) {
      console.log("Данные это массив:", data);
      return data.map(item => ({
        ...item,
        association_id: item.id,
        cart_sneaker_id: item.id || item.cart_sneaker_id,
        quantity: item.quantity || 1
      }));
    }

    if (data.items && Array.isArray(data.items)) {
      console.log("Нашли items массив:", data.items);
      return data.items.map(item => ({
        ...item,
        association_id: item.id,
        cart_sneaker_id: item.id || item.cart_sneaker_id,
        quantity: item.quantity || 1
      }));
    }

    console.log("Не удалось извлечь товары из данных корзины");
    return [];
  };

  // Получение информации о товаре для отображения
  const getDisplayInfo = (item) => {
    if (!item) return {
      name: "Неизвестная модель",
      brand: "Без бренда",
      price: "0",
      image: "",
      size: "Нет данных",
      sneakerId: null,
      sizeId: null,
      quantity: 1,
      totalPrice: 0,
      associationId: null,
      cartSneakerId: null
    };

    let brandName = "Без бренда";
    const brandId = item.brand_id;

    if (brandId) {
      const brandData = brandsData[brandId];

      if (brandData) {
        if (typeof brandData === 'string') {
          brandName = brandData;
        } else if (typeof brandData === 'object' && brandData !== null) {
          brandName = brandData.name || brandData.title || "Без бренда";
        }
      } else {
        fetchBrandInfo(brandId);
        brandName = `Загрузка... (ID: ${brandId})`;
      }
    }

    const sizeId = item.size_id;
    let displaySize = "Нет данных";

    if (sizeId) {
      const sizeData = sizesData[sizeId];
      if (sizeData) {
        // Теперь sizeData содержит eu_size из ответа сервера
        displaySize = sizeData.eu_size || `Размер ${sizeId}`;
      } else {
        // Если данные о размере еще не загружены, загружаем их
        fetchSizeInfo(sizeId);
        displaySize = `Загрузка...`;
      }
    } else if (item.size) {
      displaySize = item.size;
    }

    const associationId = item.association_id || item.id;
    const cartSneakerId = item.cart_sneaker_id || associationId;

    const quantity = item.quantity || 1;
    const price = item.price || 0;

    let imageUrl = "";
    if (item.image_url) {
      imageUrl = item.image_url;
    }

    return {
      name: item.name || "Неизвестная модель",
      brand: brandName,
      price: price,
      image: imageUrl,
      size: displaySize,
      sneakerId: item.sneaker_id,
      sizeId: sizeId,
      quantity: quantity,
      totalPrice: price * quantity,
      associationId: associationId,
      cartSneakerId: cartSneakerId
    };
  };

  // Получение общей цены корзины
  const getCartTotal = () => {
    if (!cartData) return 0;

    if (typeof cartData === 'object') {
      if (cartData["Цена корзины: "] !== undefined) {
        const totalPriceText = cartData["Цена корзины: "];
        if (typeof totalPriceText === 'number') return totalPriceText;
        if (typeof totalPriceText === 'string') {
          const match = totalPriceText.match(/[\d.]+/);
          return match ? parseFloat(match[0]) : 0;
        }
      }

      if (cartData.total_price !== undefined) {
        return cartData.total_price;
      }

      if (cartData.total !== undefined) {
        return cartData.total;
      }
    }

    const cartItems = getCartItems();
    if (cartItems.length > 0) {
      return cartItems.reduce((total, item) => {
        const price = item.price || 0;
        const quantity = item.quantity || 1;
        return total + (price * quantity);
      }, 0);
    }

    return 0;
  };

  // Проверка на пустую корзину
  const isCartEmpty = () => {
    const items = getCartItems();
    return !items || items.length === 0;
  };

  // Обработчик изменения количества товара
  const handleUpdateQuantity = async (associationId, action, e) => {
    e?.stopPropagation();
    e?.preventDefault();

    if (!associationId) {
      showToast("Не удалось изменить количество: отсутствует ID ассоциации");
      return;
    }

    // Блокируем кнопку на время обновления
    setUpdatingItems(prev => ({ ...prev, [associationId]: true }));

    try {
      console.log("Изменяем количество товара:", { associationId, action });

      // Формируем URL с параметром action
      const url = `/api/v1/cart/sneakers/${associationId}?action=${action}`;

      // Отправляем запрос на изменение количества
      const res = await cartRequest(url, {
        method: "PATCH",
      });

      console.log("Статус ответа при изменении количества:", res.status);

      if (res.status === 200 || res.status === 204) {
        // Обновляем данные корзины
        await fetchCart();

        // Показываем сообщение об успехе
        if (action === 1) {
          showToast("Количество увеличено на 1");
        } else {
          // Проверяем, если количество стало 0, товар удаляется
          const cartItems = getCartItems();
          const currentItem = cartItems.find(item => item.association_id === associationId);
          if (currentItem && currentItem.quantity === 1) {
            showToast("Товар удален из корзины");
          } else {
            showToast("Количество уменьшено на 1");
          }
        }
        return;
      }

      const errorText = await res.text();
      console.error("Текст ошибки:", errorText);

      // Если уменьшаем до 0 и товар удаляется
      if (action === 0 && res.status === 404) {
        await fetchCart();
        showToast("Товар удален из корзины");
        return;
      }

      throw new Error(`Ошибка при изменении количества: ${res.status} - ${errorText}`);

    } catch (err) {
      console.error("Ошибка при изменении количества:", err);
      showToast(err.message || "Ошибка при изменении количества товара");
    } finally {
      // Разблокируем кнопку
      setUpdatingItems(prev => ({ ...prev, [associationId]: false }));
    }
  };

  // Обработчик добавления в избранное
  const handleAddToFavorites = async (sneakerId, sizeId, e) => {
    e?.stopPropagation();
    e?.preventDefault();

    if (!sneakerId || !sizeId) {
      showToast("Не удалось добавить в избранное: отсутствуют данные");
      return;
    }

    try {
      const res = await favoriteRequest("/api/v1/favorite/sneakers/", {
        method: "POST",
        body: JSON.stringify({
          sneaker_id: sneakerId,
          size_id: sizeId
        }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Ошибка добавления в избранное:", errorText);
        throw new Error("Ошибка при добавлении товара в избранное");
      }

      showToast("Товар успешно добавлен в избранное!");
    } catch (err) {
      console.error(err);
      showToast(err.message || "Ошибка при добавлении товара в избранное");
    }
  };

  // Обработчик удаления товара из корзины
  const handleRemoveItem = async (associationId, e) => {
    e?.stopPropagation();
    e?.preventDefault();

    if (!associationId) {
      showToast("Не удалось удалить товар: отсутствует ID ассоциации");
      return;
    }

    if (!confirm("Удалить товар из корзины?")) {
      return;
    }

    try {
      console.log("Удаляем из корзины association_id:", associationId);

      const res = await cartRequest(`/api/v1/cart/sneakers/${associationId}`, {
        method: "DELETE",
      });

      console.log("Статус ответа при удалении из корзины:", res.status);

      if (res.status === 204 || res.status === 200) {
        await fetchCart();
        showToast("Товар удалён из корзины");
        return;
      }

      const errorText = await res.text();
      console.error("Текст ошибки:", errorText);

      throw new Error(`Ошибка при удалении товара: ${res.status} - ${errorText}`);

    } catch (err) {
      console.error("Ошибка при удалении:", err);
      showToast(err.message || "Ошибка при удалении товара из корзины");
    }
  };

  const handleRefresh = () => {
    setError(null);
    fetchCart();
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

  const cartItems = getCartItems();
  const cartTotal = getCartTotal();
  const isEmpty = isCartEmpty();

  console.log("Состояние корзины:", {
    cartItemsCount: cartItems.length,
    cartTotal,
    isEmpty,
    cartItems: cartItems.map(item => ({
      name: item.name,
      association_id: item.association_id,
      sneaker_id: item.sneaker_id,
      brand_id: item.brand_id,
      size_id: item.size_id,
      quantity: item.quantity
    }))
  });

  // Пустое состояние - корзина пуста
  if (isEmpty) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 pt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-20">
            <div className="inline-block p-12 bg-white rounded-3xl shadow-xl">
              <div className="mb-8">
                <div className="w-24 h-24 text-gray-300 mx-auto">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-24 w-24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>
              </div>
              <h1 className="text-4xl font-bold text-gray-900 mb-4">Ваша корзина пуста</h1>
              <p className="text-xl text-gray-600 mb-8 max-w-md mx-auto">
                Добавьте товары в корзину, чтобы сделать заказ. Нажмите на кнопку "В корзину" в карточке товара, чтобы добавить его сюда.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        {/* Заголовок */}
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Корзина
          </h1>
          <p className="text-lg text-gray-600">
            {cartItems.length} {cartItems.length === 1 ? 'товар' :
              cartItems.length > 1 && cartItems.length < 5 ? 'товара' : 'товаров'} на сумму {cartTotal} Br
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Список товаров */}
          <div className="lg:w-2/3">
            <div className="grid grid-cols-1 gap-6 md:gap-8">
              {Array.isArray(cartItems) && cartItems.map((item) => {
                if (!item || typeof item !== 'object') return null;

                const displayInfo = getDisplayInfo(item);

                if (!displayInfo.associationId) {
                  console.warn("У элемента корзины нет associationId:", item);
                  return null;
                }

                const isUpdating = updatingItems[displayInfo.associationId] || false;

                return (
                  <div
                    key={displayInfo.associationId}
                    className="group relative bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300"
                  >
                    {/* Кнопка удаления */}
                    <button
                      onClick={(e) => handleRemoveItem(displayInfo.associationId, e)}
                      className="absolute top-4 right-4 z-10 w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-red-50 hover:text-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
                      title="Удалить из корзины"
                      disabled={isUpdating}
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
                      </svg>
                    </button>

                    {/* Изображение и информация */}
                    <div className="flex flex-col md:flex-row">
                      <div
                        className="relative h-64 md:h-48 md:w-1/3 cursor-pointer overflow-hidden bg-gray-100"
                        onClick={() => {
                          if (displayInfo.sneakerId) {
                            sessionStorage.setItem("scrollPosition", window.scrollY);
                            router.push(`/details?sneakerId=${displayInfo.sneakerId}`);
                          }
                        }}
                      >
                        {displayInfo.image ? (
                          <img
                            src={`http://localhost:8005${displayInfo.image}`}
                            alt={displayInfo.name}
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
                      </div>

                      {/* Информация о товаре */}
                      <div className="p-6 flex-grow">
                        <div className="mb-4">
                          <p className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-1">
                            {displayInfo.brand}
                          </p>
                          <h3 className="text-xl font-semibold text-gray-900 line-clamp-2">
                            {displayInfo.name}
                          </h3>
                        </div>

                        <div className="space-y-4">
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="text-sm text-gray-600">Размер</p>
                              <p className="text-lg font-bold text-gray-900">{displayInfo.size}</p>
                            </div>
                            <div>
                              <p className="text-sm text-gray-600 mb-2">Количество</p>
                              <div className="flex items-center gap-3">
                                <button
                                  onClick={(e) => handleUpdateQuantity(displayInfo.associationId, 0, e)}
                                  className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center hover:bg-gray-300 transition-colors text-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed"
                                  disabled={isUpdating || displayInfo.quantity <= 1}
                                  title="Уменьшить количество"
                                >
                                  {isUpdating ? "..." : "-"}
                                </button>
                                <span className="text-xl font-bold text-gray-900 min-w-[40px] text-center">
                                  {displayInfo.quantity}
                                </span>
                                <button
                                  onClick={(e) => handleUpdateQuantity(displayInfo.associationId, 1, e)}
                                  className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center hover:bg-gray-300 transition-colors text-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed"
                                  disabled={isUpdating}
                                  title="Увеличить количество"
                                >
                                  {isUpdating ? "..." : "+"}
                                </button>
                              </div>
                            </div>
                          </div>

                          <div className="text-right">
                            <p className="text-sm text-gray-600">Цена</p>
                            <p className="text-2xl font-bold text-gray-900">
                              {displayInfo.totalPrice} Br
                            </p>
                            <p className="text-sm text-gray-500">
                              {displayInfo.price} Br × {displayInfo.quantity}
                            </p>
                          </div>
                        </div>

                        {/* Кнопки действий */}
                        <div className="flex gap-3 mt-6 pt-4 border-t border-gray-100">
                          <button
                            onClick={(e) => handleAddToFavorites(displayInfo.sneakerId, displayInfo.sizeId, e)}
                            className="flex-1 flex items-center justify-center gap-2 bg-gray-100 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={isUpdating}
                          >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                            </svg>
                            В избранное
                          </button>
                          <button
                            onClick={(e) => {
                              e.preventDefault();
                              if (displayInfo.sneakerId) {
                                sessionStorage.setItem("scrollPosition", window.scrollY);
                                router.push(`/details?sneakerId=${displayInfo.sneakerId}`);
                              }
                            }}
                            className="flex-1 bg-yellow-500 text-white py-2 rounded-lg font-semibold hover:bg-yellow-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            disabled={isUpdating}
                          >
                            Подробнее
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Боковая панель с итогами */}
          <div className="lg:w-1/3">
            <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-24">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Итого</h2>

              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-gray-600">Товары ({cartItems.length})</span>
                  <span className="font-semibold">{cartTotal} Br</span>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <div className="flex justify-between text-lg font-bold">
                    <span>Общая сумма</span>
                    <span>{cartTotal} Br</span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => router.push('/checkout')}
                className="w-full mt-8 bg-yellow-500 text-white py-3 rounded-xl font-semibold hover:bg-yellow-600 transition-all hover:shadow-lg flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Оформить заказ
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Toast уведомление */}
      {toastMessage && (
        <div className="fixed bottom-4 right-4 bg-gray-900 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in-up">
          {toastMessage}
        </div>
      )}
    </div>
  );
}

export default CartPage;