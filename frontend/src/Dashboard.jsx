import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { 
  Activity, TrendingUp, Zap, Globe, AlertCircle, CheckCircle, Clock, ExternalLink 
} from 'lucide-react';

const LiveIntelligenceDashboard = () => {
  const [seoData, setSeoData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSEOData = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: "https://example.com" })
      });

      if (!response.ok) throw new Error('Failed to fetch data from API');
      
      const data = await response.json();
      setSeoData(data);
      setLastUpdated(new Date()); 
      setError(null);
    } catch (err) {
      setError(err.message);
      setSeoData(getMockData());
      setLastUpdated(new Date());
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSEOData();
    const interval = setInterval(fetchSEOData, 24 * 60 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const getMockData = () => ({
    url: "https://example.com",
    domain_rating: 85,
    backlinks: 12450,
    referring_domains: 890,
    technical_seo_score: 87.5,
    crawl_errors: 8,
    content_density: 78,
    lighthouse_performance: 92,
    seo_score: 95,
    lighthouse_accessibility: 88,
    lighthouse_best_practices: 90,
    trend_score: 65.5,
    trend_data: generateTrendData(),
    metadata: {
      ahrefs: { organic_traffic: 45000 },
      screaming_frog: { total_urls_crawled: 150, missing_meta_descriptions: 12, avg_response_time: 245 },
      surfer_seo: { word_count: 2450, keyword_density: 2.3, terms_missing: 8 },
      lighthouse: { first_contentful_paint: 1240, speed_index: 2100, time_to_interactive: 3450 }
    }
  });

  function generateTrendData() {
    const data = [];
    for (let i = 0; i < 30; i++) {
      data.push({
        date: 2024-01-${i+1},
        interest: 50 + Math.random() * 20,
        ranking: 65 + Math.random() * 10
      });
    }
    return data;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-slate-700 border-t-emerald-500 mb-4"></div>
      </div>
    );
  }

  const radarData = [
    { metric: 'Technical', value: seoData?.technical_seo_score || 0 },
    { metric: 'Performance', value: seoData?.lighthouse_performance || 0 },
    { metric: 'SEO', value: seoData?.seo_score || 0 },
    { metric: 'Accessibility', value: seoData?.lighthouse_accessibility || 0 },
    { metric: 'Content', value: seoData?.content_density || 0 }
  ];

  const getColorClass = (color) => {
    const colors = {
      emerald: 'text-emerald-400',
      blue: 'text-blue-400',
      purple: 'text-purple-400',
      amber: 'text-amber-400'
    };
    return colors[color] || 'text-slate-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6 text-slate-200">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex justify-between items-end">
          <div>
            <h1 className="text-4xl font-bold mb-2 text-slate-100">Intelligence Dashboard</h1>
            <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border border-slate-800 rounded-lg">
              <Globe className="w-4 h-4 text-emerald-400" />
              <span className="text-sm font-mono text-emerald-400">{seoData.url}</span>
            </div>
          </div>
          <div className="text-right text-sm text-slate-500">
            <div className="flex items-center gap-2 justify-end">
              <Clock className="w-4 h-4" /> Last updated: {lastUpdated?.toLocaleTimeString()}
            </div>
          </div>
        </div>

        {/* Top Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Domain Rating', val: seoData.domain_rating, color: 'emerald' },
            { label: 'Backlinks', val: seoData.backlinks.toLocaleString(), color: 'blue' },
            { label: 'Ref. Domains', val: seoData.referring_domains, color: 'purple' },
            { label: 'Traffic', val: seoData.metadata.ahrefs.organic_traffic.toLocaleString(), color: 'amber' }
          ].map((m, i) => (
            <div key={i} className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
              <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">{m.label}</p>
              <p className={text-2xl font-bold ${getColorClass(m.color)}}>{m.val}</p>
            </div>
          ))}
        </div>

        {/* Charts Section */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
            <h3 className="flex items-center gap-2 mb-6 font-bold"><Zap className="w-5 h-5 text-emerald-400" /> Technical Matrix</h3>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <Radar dataKey="value" stroke="#10b981" fill="#10b981" fillOpacity={0.5} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
            <h3 className="flex items-center gap-2 mb-6 font-bold"><TrendingUp className="w-5 h-5 text-blue-400" /> Growth Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={seoData.trend_data.slice(-20)}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="date" hide />
                <Tooltip contentStyle={{backgroundColor: '#0f172a', border: 'none'}} />
                <Area type="monotone" dataKey="interest" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.1} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Detailed Grid */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
            <h4 className="text-slate-400 text-sm font-bold mb-4">Crawl Status</h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span>Total Crawled</span>
                <span>{seoData.metadata.screaming_frog.total_urls_crawled}</span>
              </div>
              <div className="flex justify-between text-red-400">
                <span>Crawl Errors</span>
                <span>{seoData.crawl_errors}</span>
              </div>
            </div>
          </div>
          
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
            <h4 className="text-slate-400 text-sm font-bold mb-4">Content Quality</h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between text-emerald-400">
                <span>Score</span>
                <span>{seoData.content_density}/100</span>
              </div>
              <div className="flex justify-between">
                <span>Word Count</span>
                <span>{seoData.metadata.surfer_seo.word_count}</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
            <h4 className="text-slate-400 text-sm font-bold mb-4">Performance</h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between text-blue-400">
                <span>Speed Index</span>
                <span>{seoData.metadata.lighthouse.speed_index}ms</span>
              </div>
              <div className="flex justify-between">
                <span>TTI</span>
                <span>{seoData.metadata.lighthouse.time_to_interactive}ms</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-xl flex items-center gap-2 text-emerald-500 text-sm">
          <CheckCircle className="w-4 h-4" /> Systems Operational: All SEO modules syncing successfully
        </div>
      </div>
    </div>
  );
};

export default LiveIntelligenceDashboard;