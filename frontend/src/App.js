import React, { useState } from 'react';
import LiveIntelligenceDashboard from './Dashboard';
import { antenna } from 'lucide-react';

function App() {
  return (
    <div>
      <h1>My PORTFOLIO</h1>
      {/* 2. The Tag goes here, inside the return statement */
      <Antenna size={48} className="text-green-500" />
    </div>
  );
}
export default App;
import { 
  Github, Linkedin, Mail, ExternalLink, BookOpen, Search, 
  Languages, Brain, Cpu, Database, Award, Sparkles, ChevronLeft, ChevronRight 
} from 'lucide-react';

function App() {
  const [currentCert, setCurrentCert] = useState(0);

  const projects = [
    {
      title: "Manateq Qatar",
      type: "SEO Optimization",
      desc: "Delivered bidirectional translation and SEO content adaptation for regional enterprise audiences.",
      link: "https://manateq.qa",
      icon: <Search className="text-[#557C55]" />
    },
    {
      title: "Jordan Commercial Bank",
      type: "Financial Localization",
      desc: "Specialized English to Arabic translation for high-stakes banking and corporate content.",
      link: "https://www.jcbank.com.jo/en",
      icon: <Languages className="text-slate-600" />
    },
    {
      title: "CFI Academy",
      type: "Educational Content",
      desc: "Linguistic precision for trading courses focused on fundamental market analysis.",
      link: "https://cfi.trade/en/jo/academy/course/fundamental-analysis/understanding-fundamental-analysis",
      icon: <BookOpen className="text-[#557C55]" />
    }
  ];

  const certifications = [
    { title: "SEO Optimization", provider: "Sustainable Vision", date: "2024" },
    { title: "Data Analysis", provider: "Sustainable Vision", date: "2023" },
    { title: "Project Management", provider: "Sustainable Vision", date: "2023" },
    { title: "AI Agents for HR", provider: "Qafza Tech", date: "2025" }
  ];

  const interests = [
    "Applied AI", "Behavioral Psychology", "Medicine", "Film Analysis", "Data Visualization"
  ];

  const nextCert = () => setCurrentCert((prev) => (prev + 1) % certifications.length);
  const prevCert = () => setCurrentCert((prev) => (prev - 1 + certifications.length) % certifications.length);

  return (
    <div className="min-h-screen bg-[#FDFCFB] font-sans text-[#334155]">
      {/* 1. NAVIGATION BAR */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-[#E2E8F0] py-4 px-6">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <span className="text-xl font-bold tracking-tighter text-[#1E293B]">SAMI SALEM<span className="text-[#557C55]">.</span></span>
          <div className="flex items-center space-x-8">
            <a href="https://github.com/Sami-Salem" target="_blank" rel="noreferrer" className="text-slate-400 hover:text-[#1E293B] transition-transform hover:scale-110">
              <Github size={28} /> {/* Enlarged Icon */}
            </a>
            <a href="https://www.linkedin.com/in/sami-salem-98791a3a1" target="_blank" rel="noreferrer" className="text-slate-400 hover:text-[#0077B5] transition-transform hover:scale-110">
              <Linkedin size={28} /> {/* Enlarged Icon */}
            </a>
            <a href="mailto:samisalemj@outlook.com" className="bg-[#557C55] text-white px-6 py-2 rounded-full text-sm font-bold hover:bg-[#3E5C3E] transition shadow-md">
              CONTACT ME
            </a>
          </div>
        </div>
      </nav>

      {/* 2. PERSONAL INTRODUCTION */}
      <header className="pt-28 pb-10 px-6 bg-gradient-to-b from-white to-[#FDFCFB]">
        <div className="max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-[#F0F4F0] text-[#3E5C3E] px-3 py-1 rounded-md text-xs font-bold mb-6 tracking-wide">
            <Sparkles size={14} /> BUILDING DATA-DRIVEN SOLUTIONS
          </div>
          <h1 className="text-5xl font-bold text-[#1E293B] mb-6 leading-[1.1]">
            Bridging the gap between <br />
            <span className="text-[#557C55]">Digital Intelligence</span> & Human Context.
          </h1>
          <p className="text-lg text-slate-600 mb-8 max-w-2xl leading-relaxed">
            I am a Data & SEO Specialist with a medical background. I build automated SEO pipelines, manage Generative AI integrations, and deliver professional bilingual localization for various sectors.
          </p>
        </div>
      </header>

      {/* 3. INTERESTS (Moved here) */}
      <section className="pb-20 px-6 bg-[#FDFCFB]">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Core Interests & Curiosity</h2>
          <div className="flex flex-wrap gap-3">
            {interests.map((item, i) => (
              <span key={i} className="px-5 py-2 bg-white border border-[#E2E8F0] rounded-full text-xs font-semibold text-slate-600 shadow-sm hover:border-[#557C55] transition-colors">
                {item}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* 4. CORE EXPERTISE & TECH STACK */}
      <section className="py-20 px-6 bg-[#F8FAF8] border-y border-[#E2E8F0]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-sm font-black text-[#557C55] uppercase tracking-[0.2em] mb-12 text-center">Core Expertise</h2>
          <div className="grid md:grid-cols-3 gap-10">
            <div className="group bg-white p-8 rounded-2xl border border-transparent hover:border-[#F0F4F0] hover:shadow-sm transition-all">
              <div className="w-12 h-12 bg-[#F8FAF8] rounded-xl flex items-center justify-center mb-6 group-hover:bg-[#557C55] group-hover:text-white transition-all">
                <Cpu size={24} />
              </div>
              <h3 className="font-bold text-[#1E293B] mb-3">AI & ML Engineering</h3>
              <p className="text-sm text-slate-500 leading-relaxed">Scaling Generative AI models and fixing ML pipelines for automated content management.</p>
            </div>
            <div className="group bg-white p-8 rounded-2xl border border-transparent hover:border-[#F0F4F0] hover:shadow-sm transition-all">
              <div className="w-12 h-12 bg-[#F8FAF8] rounded-xl flex items-center justify-center mb-6 group-hover:bg-[#557C55] group-hover:text-white transition-all">
                <Database size={24} />
              </div>
              <h3 className="font-bold text-[#1E293B] mb-3">Data Intelligence</h3>
              <p className="text-sm text-slate-500 leading-relaxed">Expertise in data visualization and technical SEO optimization using Python-based data pipelines.</p>
            </div>
            <div className="group bg-white p-8 rounded-2xl border border-transparent hover:border-[#F0F4F0] hover:shadow-sm transition-all">
              <div className="w-12 h-12 bg-[#F8FAF8] rounded-xl flex items-center justify-center mb-6 group-hover:bg-[#557C55] group-hover:text-white transition-all">
                <Languages size={24} />
              </div>
              <h3 className="font-bold text-[#1E293B] mb-3">Global Localization</h3>
              <p className="text-sm text-slate-500 leading-relaxed">Premium Arabic/English translation for financial markets and complex educational content.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 5. PORTFOLIO GALLERY */}
      <section id="projects" className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-sm font-black text-[#557C55] uppercase tracking-[0.2em] mb-12">projects</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {projects.map((p, i) => (
              <div key={i} className="bg-[#FDFCFB] p-8 rounded-xl border border-[#E2E8F0] hover:shadow-md transition-shadow">
                <div className="mb-6">{p.icon}</div>
                <h4 className="text-xs font-bold text-[#557C55] uppercase mb-2 tracking-widest">{p.type}</h4>
                <h5 className="text-lg font-bold mb-3">{p.title}</h5>
                <p className="text-slate-500 text-sm leading-relaxed mb-6">{p.desc}</p>
                <a href={p.link} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-xs font-bold text-[#1E293B] hover:gap-3 transition-all underline decoration-[#557C55] underline-offset-4">VIEW PROJECT <ExternalLink size={12} /></a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 6. CERTIFICATION CAROUSEL */}
      <section className="py-24 px-6 bg-[#1E293B] text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-xs font-bold text-[#A3B18A] uppercase tracking-[0.3em] mb-12">Verified Certifications</h2>
          <div className="relative bg-white/5 backdrop-blur-sm p-12 rounded-3xl border border-white/10 overflow-hidden">
            <div className="animate-in fade-in slide-in-from-right duration-500" key={currentCert}>
              <Award className="mx-auto text-[#A3B18A] mb-6" size={48} />
              <h3 className="text-2xl font-bold mb-2">{certifications[currentCert].title}</h3>
              <p className="text-[#A3B18A] font-medium">{certifications[currentCert].provider}</p>
              <p className="text-slate-500 text-sm mt-4 italic">{certifications[currentCert].date}</p>
            </div>
            
            <button onClick={prevCert} className="absolute left-4 top-1/2 -translate-y-1/2 p-2 hover:bg-white/10 rounded-full transition-colors"><ChevronLeft /></button>
            <button onClick={nextCert} className="absolute right-4 top-1/2 -translate-y-1/2 p-2 hover:bg-white/10 rounded-full transition-colors"><ChevronRight /></button>
          </div>
          <div className="flex justify-center gap-2 mt-8">
            {certifications.map((_, i) => (
              <div key={i} className={`w-1.5 h-1.5 rounded-full transition-all ${currentCert === i ? 'bg-[#A3B18A] w-6' : 'bg-white/20'}`} />
            ))}
          </div>
        </div>
      </section>

      {/* 7. LIVE SEO ENGINE */}
      <section id="seo-tool" className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-sm font-black text-[#557C55] uppercase tracking-[0.2em] mb-12">Live Intelligence Hub</h2>
          <div className="rounded-2xl shadow-xl overflow-hidden border border-[#F1F5F9]">
             <LiveIntelligenceDashboard />
          </div>
        </div>
      </section>

      <footer className="py-12 bg-[#F8FAF8] border-t border-[#E2E8F0] text-center">
        <p className="text-slate-400 text-sm italic">"Precision in code, clarity in language."</p>
        <p className="text-slate-300 text-xs mt-4">© 2026 Sami Mohammad Salem Salem. Built with clinical precision.</p>
      </footer>
    </div>
  );
}

export default App;