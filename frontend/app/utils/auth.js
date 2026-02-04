// Утилита для проверки авторизации и работы с API
export async function checkAuth() {
  try {
    // Пробуем сначала через Kong (8000), если не работает - напрямую через auth_service (8002)
    const makeRequest = async (url) => {
      try {
        const response = await fetch(url, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
        return { response, error: null };
      } catch (error) {
        return { response: null, error };
      }
    };

    let result = await makeRequest("http://localhost:8000/api/v1/auth/me");
    if (result.error) {
      result = await makeRequest("http://localhost:8002/api/v1/auth/me");
    }

    if (result.error || !result.response.ok) {
      return { isAuthenticated: false, user: null };
    }

    const user = await result.response.json();
    return { isAuthenticated: true, user };
  } catch (error) {
    return { isAuthenticated: false, user: null };
  }
}

// Утилита для запросов к favorite_service с fallback
export async function favoriteRequest(url, options = {}) {
  const makeRequest = async (baseUrl) => {
    try {
      const response = await fetch(`${baseUrl}${url}`, {
        ...options,
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });
      return { response, error: null };
    } catch (error) {
      return { response: null, error };
    }
  };

  // Пробуем сначала через Kong (8000), если не работает - напрямую через favorite_service (8003)
  let result = await makeRequest("http://localhost:8000");
  if (result.error) {
    result = await makeRequest("http://localhost:8003");
  }

  if (result.error) {
    throw new Error("Не удалось подключиться к серверу избранного");
  }

  return result.response;
}
