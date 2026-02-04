"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

function ManagementPage() {
  const [userRole, setUserRole] = useState(null);
  const [userEmail, setUserEmail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    users: 0,
    orders: 0,
    products: 0,
    revenue: 0
  });
  const [activeSection, setActiveSection] = useState("overview");
  const router = useRouter();

  // Проверка роли пользователя
  useEffect(() => {
    checkUserRole();
  }, []);

  const checkUserRole = async () => {
    try {
      // Проверяем localStorage
      const savedRole = localStorage.getItem('userRole');
      const savedEmail = localStorage.getItem('userEmail');

      console.log("Проверка доступа:", { savedRole, savedEmail });

      // Проверяем, является ли пользователь админом
      if (savedEmail === "howertwik@gmail.com" || savedRole === "Admin") {
        setUserRole("Admin");
        setUserEmail(savedEmail);

        // Дополнительно проверяем через API
        try {
          const response = await fetch("http://localhost:8000/api/v1/auth/me", {
            method: "GET",
            credentials: "include",
          });

          if (response.ok) {
            const userData = await response.json();
            console.log("Данные пользователя из API:", userData);

            if (userData.email !== "howertwik@gmail.com") {
              throw new Error("Доступ запрещен");
            }
          } else {
            throw new Error("Ошибка проверки авторизации");
          }
        } catch (apiError) {
          console.log("API проверка не удалась, используем данные из localStorage");
        }

        // Загружаем статистику для админ-панели
        await fetchDashboardStats();
        setLoading(false);
      } else {
        // Если пользователь не админ, редирект на главную
        console.log("Пользователь не админ, редирект...");
        router.push('/');
      }

    } catch (err) {
      console.error("Ошибка при проверке роли:", err);
      setError("Ошибка доступа к панели управления");
      setLoading(false);
    }
  };

  const fetchDashboardStats = async () => {
    try {
      // Здесь будут реальные запросы к API
      // Сейчас используем заглушку
      const mockStats = {
        users: 1250,
        orders: 342,
        products: 156,
        revenue: 125430
      };

      setStats(mockStats);
    } catch (error) {
      console.error("Ошибка загрузки статистики:", error);
    }
  };

  // Обработчик выхода из админ-панели
  const handleLogout = async () => {
    try {
      // Выход через API
      await fetch("http://localhost:8000/api/v1/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (error) {
      console.log("Ошибка при выходе через API, продолжаем очистку локально");
    }

    // Очищаем localStorage
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('user');

    // Редирект на главную
    router.push('/');
  };

  // Обработчик перехода в раздел
  const handleNavigate = (section) => {
    setActiveSection(section);
  };

  // Рендер контента в зависимости от активного раздела
  const renderContent = () => {
    switch (activeSection) {
      case "overview":
        return <OverviewContent stats={stats} />;
      case "users":
        return <UsersContent />;
      case "products":
        return <ProductsContent />;
      case "orders":
        return <OrdersContent />;
      case "analytics":
        return <AnalyticsContent />;
      case "settings":
        return <SettingsContent />;
      default:
        return <OverviewContent stats={stats} />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 pt-24">
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
      <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 pt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-20">
            <div className="inline-block p-8 bg-white rounded-2xl shadow-lg">
              <div className="text-red-500 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.282 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Доступ запрещен</h2>
              <p className="text-gray-600 mb-6">{error}</p>
              <button
                onClick={() => router.push('/')}
                className="inline-flex items-center px-6 py-3 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600 transition-colors"
              >
                Вернуться на главную
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Шапка админ-панели */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">Панель управления</h1>
              <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                Администратор
              </span>
              <span className="text-sm text-gray-500">({userEmail})</span>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/')}
                className="text-gray-600 hover:text-gray-900 font-medium"
              >
                На сайт
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Выйти
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Боковая панель навигации */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-xl shadow-sm p-6 sticky top-24">
              <nav className="space-y-2">
                <NavItem
                  icon="📊"
                  label="Обзор"
                  isActive={activeSection === "overview"}
                  onClick={() => handleNavigate("overview")}
                />
                <NavItem
                  icon="👥"
                  label="Пользователи"
                  isActive={activeSection === "users"}
                  onClick={() => handleNavigate("users")}
                />
                <NavItem
                  icon="👟"
                  label="Товары"
                  isActive={activeSection === "products"}
                  onClick={() => handleNavigate("products")}
                />
                <NavItem
                  icon="📦"
                  label="Заказы"
                  isActive={activeSection === "orders"}
                  onClick={() => handleNavigate("orders")}
                />
                <NavItem
                  icon="📈"
                  label="Аналитика"
                  isActive={activeSection === "analytics"}
                  onClick={() => handleNavigate("analytics")}
                />
                <NavItem
                  icon="⚙️"
                  label="Настройки"
                  isActive={activeSection === "settings"}
                  onClick={() => handleNavigate("settings")}
                />
              </nav>

              <div className="mt-8 pt-6 border-t border-gray-100">
                <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-3">
                  Быстрые действия
                </h3>
                <div className="space-y-2">
                  <QuickAction
                    icon="➕"
                    label="Добавить товар"
                    onClick={() => handleNavigate("products")}
                  />
                  <QuickAction
                    icon="📨"
                    label="Отправить уведомление"
                    onClick={() => alert("Функция в разработке")}
                  />
                  <QuickAction
                    icon="📊"
                    label="Скачать отчет"
                    onClick={() => alert("Функция в разработке")}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Основной контент */}
          <div className="lg:w-3/4">
            <div className="bg-white rounded-xl shadow-sm p-6">
              {renderContent()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Компонент пункта навигации
function NavItem({ icon, label, isActive, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
        isActive
          ? "bg-yellow-50 text-yellow-700 border border-yellow-200"
          : "text-gray-700 hover:bg-gray-50 hover:text-gray-900"
      }`}
    >
      <span className="text-xl">{icon}</span>
      <span className="font-medium">{label}</span>
    </button>
  );
}

// Компонент быстрого действия
function QuickAction({ icon, label, onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-all"
    >
      <span className="text-lg">{icon}</span>
      <span className="text-sm font-medium">{label}</span>
    </button>
  );
}

// Компонент контента для раздела "Обзор"
function OverviewContent({ stats }) {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Обзор системы</h2>
        <p className="text-gray-600">Статистика и ключевые показатели</p>
      </div>

      {/* Карточки статистики */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Пользователи"
          value={stats.users}
          change="+12%"
          icon="👥"
          color="blue"
        />
        <StatCard
          title="Заказы"
          value={stats.orders}
          change="+8%"
          icon="📦"
          color="green"
        />
        <StatCard
          title="Товары"
          value={stats.products}
          change="+5%"
          icon="👟"
          color="purple"
        />
        <StatCard
          title="Выручка"
          value={`${stats.revenue.toLocaleString()} Br`}
          change="+15%"
          icon="💰"
          color="yellow"
        />
      </div>

      {/* Недавние действия */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Последние действия</h3>
        <div className="bg-gray-50 rounded-lg p-6">
          <div className="space-y-4">
            <ActivityItem
              user="Иван Петров"
              action="сделал заказ"
              item="Nike Air Force 1"
              time="10 минут назад"
            />
            <ActivityItem
              user="Анна Сидорова"
              action="добавила в избранное"
              item="Adidas Ultraboost"
              time="25 минут назад"
            />
            <ActivityItem
              user="Сергей Иванов"
              action="зарегистрировался"
              item="новый пользователь"
              time="1 час назад"
            />
          </div>
        </div>
      </div>

      {/* Быстрые ссылки */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Быстрые ссылки</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <QuickLink
            title="Управление товарами"
            description="Добавление, редактирование и удаление товаров"
            href="#"
            icon="👟"
          />
          <QuickLink
            title="Просмотр заказов"
            description="Обработка и отслеживание заказов"
            href="#"
            icon="📦"
          />
          <QuickLink
            title="Аналитика продаж"
            description="Графики и отчеты по продажам"
            href="#"
            icon="📈"
          />
          <QuickLink
            title="Настройки сайта"
            description="Изменение настроек и контента"
            href="#"
            icon="⚙️"
          />
        </div>
      </div>
    </div>
  );
}

// Компонент карточки статистики
function StatCard({ title, value, change, icon, color }) {
  const colorClasses = {
    blue: "bg-blue-50 text-blue-700",
    green: "bg-green-50 text-green-700",
    purple: "bg-purple-50 text-purple-700",
    yellow: "bg-yellow-50 text-yellow-700"
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <div className="flex items-center justify-between mb-4">
        <span className="text-3xl">{icon}</span>
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${colorClasses[color]}`}>
          {change}
        </span>
      </div>
      <h3 className="text-2xl font-bold text-gray-900 mb-1">{value}</h3>
      <p className="text-sm text-gray-600">{title}</p>
    </div>
  );
}

// Компонент элемента активности
function ActivityItem({ user, action, item, time }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-gray-200 last:border-0">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
          <span className="text-lg">👤</span>
        </div>
        <div>
          <p className="font-medium text-gray-900">
            <span className="font-semibold">{user}</span> {action} <span className="text-yellow-600">{item}</span>
          </p>
        </div>
      </div>
      <span className="text-sm text-gray-500">{time}</span>
    </div>
  );
}

// Компонент быстрой ссылки
function QuickLink({ title, description, href, icon }) {
  return (
    <a
      href={href}
      className="block p-6 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors border border-gray-200"
    >
      <div className="flex items-center space-x-4">
        <span className="text-2xl">{icon}</span>
        <div>
          <h4 className="font-semibold text-gray-900 mb-1">{title}</h4>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
      </div>
    </a>
  );
}

// Компонент контента для раздела "Пользователи"
function UsersContent() {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Управление пользователями</h2>
        <p className="text-gray-600">Просмотр и управление пользователями системы</p>
      </div>
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-6.197a6 6 0 01-6 6m6-6a6 6 0 00-6-6m6 6H3" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Раздел в разработке</h3>
        <p className="text-gray-600">Функционал управления пользователями будет доступен в ближайшее время</p>
      </div>
    </div>
  );
}

// Компонент контента для раздела "Товары"
function ProductsContent() {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Управление товарами</h2>
        <p className="text-gray-600">Добавление, редактирование и удаление товаров</p>
      </div>
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Раздел в разработке</h3>
        <p className="text-gray-600">Функционал управления товарами будет доступен в ближайшее время</p>
      </div>
    </div>
  );
}

// Компонент контента для раздела "Заказы"
function OrdersContent() {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Управление заказами</h2>
        <p className="text-gray-600">Просмотр и обработка заказов</p>
      </div>
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Раздел в разработке</h3>
        <p className="text-gray-600">Функционал управления заказами будет доступен в ближайшее время</p>
      </div>
    </div>
  );
}

// Компонент контента для раздела "Аналитика"
function AnalyticsContent() {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Аналитика и отчеты</h2>
        <p className="text-gray-600">Статистика продаж и анализ данных</p>
      </div>
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Раздел в разработке</h3>
        <p className="text-gray-600">Функционал аналитики будет доступен в ближайшее время</p>
      </div>
    </div>
  );
}

// Компонент контента для раздела "Настройки"
function SettingsContent() {
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Настройки системы</h2>
        <p className="text-gray-600">Настройки сайта и параметров системы</p>
      </div>
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Раздел в разработке</h3>
        <p className="text-gray-600">Функционал настроек будет доступен в ближайшее время</p>
      </div>
    </div>
  );
}

export default ManagementPage;