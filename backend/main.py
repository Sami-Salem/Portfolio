"""
Professional Portfolio Backend - SEO Metadata Analyzer
FastAPI application for extracting and analyzing SEO metadata from URLs
"""
import uvicorn
import logging
import os
import re
import requests
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 1. Load environment variables correctly
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 2. Initialize FastAPI
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SEO Metadata Analyzer API",
    description="Extract and analyze SEO metadata with localization scoring",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    """Request model for URL analysis"""
    url: HttpUrl

class SEOMetadata(BaseModel):
    """Response model for SEO analysis"""
    url: str
    title: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[str]
    h1_tags: List[str]
    h2_tags: List[str]
    internal_links: int
    external_links: int
    images_count: int
    images_with_alt: int
    word_count: int
    lang_attribute: Optional[str]
    has_hreflang: bool
    og_tags: Dict[str, str]
    schema_markup: bool
    mobile_viewport: bool
    canonical_url: Optional[str]
    seo_score: int
    localization_score: int
    content_density: int
    technical_seo_score: int

class SEOAnalyzer:
    """Core SEO analysis engine"""
    
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.text_content = ""
        
    def fetch_page(self) -> bool:
        """Fetch and parse the webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; SEOAnalyzer/1.0)'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            self.text_content = self.soup.get_text(separator=' ', strip=True)
            return True
        except Exception as e:
            logger.error(f"Error fetching {self.url}: {str(e)}")
            return False
    
    def extract_title(self) -> Optional[str]:
        """Extract page title"""
        title_tag = self.soup.find('title')
        return title_tag.string.strip() if title_tag else None
    
    def extract_meta_description(self) -> Optional[str]:
        """Extract meta description"""
        meta = self.soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '').strip() if meta else None
    
    def extract_meta_keywords(self) -> Optional[str]:
        """Extract meta keywords"""
        meta = self.soup.find('meta', attrs={'name': 'keywords'})
        return meta.get('content', '').strip() if meta else None
    
    def extract_headings(self) -> tuple:
        """Extract H1 and H2 tags"""
        h1_tags = [h1.get_text(strip=True) for h1 in self.soup.find_all('h1')]
        h2_tags = [h2.get_text(strip=True) for h2 in self.soup.find_all('h2')]
        return h1_tags, h2_tags
    
    def analyze_links(self) -> tuple:
        """Analyze internal and external links"""
        domain = urlparse(self.url).netloc
        internal = external = 0
        
        for link in self.soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or domain in href:
                internal += 1
            elif href.startswith('http'):
                external += 1
        
        return internal, external
    
    def analyze_images(self) -> tuple:
        """Analyze image optimization"""
        images = self.soup.find_all('img')
        total = len(images)
        with_alt = len([img for img in images if img.get('alt')])
        return total, with_alt
    
    def extract_lang_attributes(self) -> tuple:
        """Extract language and hreflang data"""
        html_tag = self.soup.find('html')
        lang = html_tag.get('lang') if html_tag else None
        hreflang = bool(self.soup.find('link', rel='alternate', hreflang=True))
        return lang, hreflang
    
    def extract_og_tags(self) -> Dict[str, str]:
        """Extract Open Graph tags"""
        og_tags = {}
        for meta in self.soup.find_all('meta', property=re.compile(r'^og:')):
            prop = meta.get('property', '').replace('og:', '')
            content = meta.get('content', '')
            og_tags[prop] = content
        return og_tags
    
    def check_technical_seo(self) -> tuple:
        """Check technical SEO elements"""
        # Schema markup
        schema = bool(self.soup.find('script', type='application/ld+json'))
        
        # Mobile viewport
        viewport = bool(self.soup.find('meta', attrs={'name': 'viewport'}))
        
        # Canonical URL
        canonical = self.soup.find('link', rel='canonical')
        canonical_url = canonical.get('href') if canonical else None
        
        return schema, viewport, canonical_url
    
    def calculate_word_count(self) -> int:
        """Calculate word count from text content"""
        words = self.text_content.split()
        return len(words)
    
    def calculate_seo_score(self, metadata: dict) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 0
        
        # Title optimization (20 points)
        if metadata['title']:
            title_len = len(metadata['title'])
            if 30 <= title_len <= 60:
                score += 20
            elif title_len > 0:
                score += 10
        
        # Meta description (15 points)
        if metadata['meta_description']:
            desc_len = len(metadata['meta_description'])
            if 120 <= desc_len <= 160:
                score += 15
            elif desc_len > 0:
                score += 8
        
        # H1 tags (10 points)
        if len(metadata['h1_tags']) == 1:
            score += 10
        elif len(metadata['h1_tags']) > 0:
            score += 5
        
        # Images with alt text (10 points)
        if metadata['images_count'] > 0:
            alt_ratio = metadata['images_with_alt'] / metadata['images_count']
            score += int(10 * alt_ratio)
        
        # Content length (15 points)
        if metadata['word_count'] >= 300:
            score += 15
        elif metadata['word_count'] >= 150:
            score += 8
        
        # Technical SEO (30 points)
        if metadata['mobile_viewport']:
            score += 10
        if metadata['canonical_url']:
            score += 10
        if metadata['schema_markup']:
            score += 10
        
        return min(score, 100)
    
    def calculate_localization_score(self, metadata: dict) -> int:
        """Calculate localization quality score (0-100)"""
        score = 0
        
        # Language attribute (25 points)
        if metadata['lang_attribute']:
            score += 25
        
        # Hreflang implementation (25 points)
        if metadata['has_hreflang']:
            score += 25
        
        # Bilingual content indicators (30 points)
        text_lower = self.text_content.lower()
        if any(word in text_lower for word in ['arabic', 'عربي', 'bilingual', 'multilingual']):
            score += 15
        
        # Check for RTL support or Arabic content
        if self.soup.find(attrs={'dir': 'rtl'}) or bool(re.search(r'[\u0600-\u06FF]', self.text_content)):
            score += 15
        
        # OG locale tags (20 points)
        if 'locale' in metadata['og_tags']:
            score += 20
        
        return min(score, 100)
    
    def calculate_content_density(self, metadata: dict) -> int:
        """Calculate content density score (0-100)"""
        score = 0
        
        # Word count (40 points)
        wc = metadata['word_count']
        if wc >= 1000:
            score += 40
        elif wc >= 500:
            score += 30
        elif wc >= 200:
            score += 20
        
        # Heading structure (30 points)
        if len(metadata['h1_tags']) > 0 and len(metadata['h2_tags']) > 0:
            score += 30
        elif len(metadata['h1_tags']) > 0 or len(metadata['h2_tags']) > 0:
            score += 15
        
        # Internal linking (30 points)
        if metadata['internal_links'] >= 10:
            score += 30
        elif metadata['internal_links'] >= 5:
            score += 20
        elif metadata['internal_links'] > 0:
            score += 10
        
        return min(score, 100)
    
    def calculate_technical_seo_score(self, metadata: dict) -> int:
        """Calculate technical SEO score (0-100)"""
        score = 0
        
        if metadata['mobile_viewport']:
            score += 25
        if metadata['canonical_url']:
            score += 25
        if metadata['schema_markup']:
            score += 25
        if len(metadata['og_tags']) >= 3:
            score += 25
        
        return score
    
    def analyze(self) -> SEOMetadata:
        """Perform complete SEO analysis"""
        if not self.fetch_page():
            raise Exception("Failed to fetch page")
        
        # Extract all metadata
        h1_tags, h2_tags = self.extract_headings()
        internal_links, external_links = self.analyze_links()
        images_count, images_with_alt = self.analyze_images()
        lang_attr, has_hreflang = self.extract_lang_attributes()
        schema, viewport, canonical = self.check_technical_seo()
        
        metadata = {
            'url': self.url,
            'title': self.extract_title(),
            'meta_description': self.extract_meta_description(),
            'meta_keywords': self.extract_meta_keywords(),
            'h1_tags': h1_tags,
            'h2_tags': h2_tags,
            'internal_links': internal_links,
            'external_links': external_links,
            'images_count': images_count,
            'images_with_alt': images_with_alt,
            'word_count': self.calculate_word_count(),
            'lang_attribute': lang_attr,
            'has_hreflang': has_hreflang,
            'og_tags': self.extract_og_tags(),
            'schema_markup': schema,
            'mobile_viewport': viewport,
            'canonical_url': canonical,
        }
        
        # Calculate scores
        metadata['seo_score'] = self.calculate_seo_score(metadata)
        metadata['localization_score'] = self.calculate_localization_score(metadata)
        metadata['content_density'] = self.calculate_content_density(metadata)
        metadata['technical_seo_score'] = self.calculate_technical_seo_score(metadata)
        
        return SEOMetadata(**metadata)

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "SEO Metadata Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "POST - Analyze URL for SEO metadata",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/analyze", response_model=SEOMetadata)
async def analyze_url(request: URLRequest):
    """
    Analyze a URL for SEO metadata and scoring
    
    Args:
        request: URLRequest containing the URL to analyze
    
    Returns:
        SEOMetadata: Complete SEO analysis results
    """
    try:
        analyzer = SEOAnalyzer(str(request.url))
        results = analyzer.analyze()
        logger.info(f"Successfully analyzed: {request.url}")
        return results
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to analyze URL: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    