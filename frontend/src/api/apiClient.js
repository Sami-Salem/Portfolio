const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const API_TIMEOUT = Number(process.env.REACT_APP_API_TIMEOUT) || 30000;

class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
  }
}

class APIClient {
  constructor(baseURL = API_URL) {
    this.baseURL = baseURL;
    this.timeout = API_TIMEOUT;
  }

  async request(endpoint, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      const text = await response.json();
      const data = text ? JSON.parse(text) : null;

      if (!response.ok) {
        throw new APIError(data?.message || 'Request failed', response.status, data);
      }

      return data;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new APIError('Request timeout', 408, null);
      }

      if (error instanceof APIError) throw error;

      throw new APIError('Network error. Please check your connection.', 0, null);
    }
  }

  analyzeSEO(url) {
    return this.request('/analyze', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  runPipeline(url) {
    return this.request('/pipeline', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  healthCheck() {
    return this.request('/health');
  }
}

export const api = new APIClient();
export { APIError };
