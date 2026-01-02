const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 30000;

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
      const response = await fetch(${this.baseURL}${endpoint}, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const data = await response.json();

      if (!response.ok) {
        throw new APIError(
          data.message || 'Request failed',
          response.status,
          data
        );
      }

      return data;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new APIError('Request timeout', 408, null);
      }

      if (error instanceof APIError) {
        throw error;
      }

      throw new APIError(
        'Network error. Please check your connection.',
        0,
        null
      );
    }
  }

  async analyzeSEO(url) {
    return this.request('/analyze', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async runPipeline(url) {
    return this.request('/pipeline', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  async healthCheck() {
    return this.request('/health');
  }
}

export const api = new APIClient();
export { APIError };

import React from 'react';
import LiveIntelligenceDashboard from './Dashboard';

function App() {
  return (
    <div className="portfolio-root">
      {/* --- YOUR PORTFOLIO SECTIONS START --- */}
      <section id="hero" className="p-10 bg-slate-900 text-white text-center">
        <h1 className="text-5xl font-bold">Sami's Portfolio</h1>
        <p className="mt-4 text-xl text-slate-400">Full-Stack Developer & SEO Specialist</p>
      </section>

      {/* --- YOUR SEO DASHBOARD SECTION --- */}
      <section id="seo-tool" className="py-10">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-2xl font-bold mb-6 text-slate-800">Featured Project: Live SEO Intelligence</h2>
          <LiveIntelligenceDashboard />
        </div>
      </section>

      {/* --- OTHER SECTIONS --- */}
      <section id="projects" className="p-10 bg-white">
        <h2 className="text-3xl font-bold">Other Projects</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
           <div className="p-4 border rounded">Project 1</div>
           <div className="p-4 border rounded">Project 2</div>
        </div>
      </section>
    </div>
  );
}

export default App;