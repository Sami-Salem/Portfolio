"""
Batch SEO Analyzer - Analyze multiple URLs and generate comparison report
Perfect for demonstrating data extraction and analysis capabilities
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from typing import List, Dict
import time
from urllib.parse import urlparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class BatchSEOAnalyzer:
    """Batch analyzer for multiple URLs with comparative analytics"""
    
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.results = []
        
    def analyze_single_url(self, url: str) -> Dict:
        """Analyze a single URL and return metrics"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; SEOBatchAnalyzer/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.string.strip() if title else None
            title_length = len(title_text) if title_text else 0
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            meta_desc_text = meta_desc.get('content', '').strip() if meta_desc else None
            desc_length = len(meta_desc_text) if meta_desc_text else 0
            
            # Count elements
            h1_count = len(soup.find_all('h1'))
            h2_count = len(soup.find_all('h2'))
            h3_count = len(soup.find_all('h3'))
            
            # Link analysis
            all_links = soup.find_all('a', href=True)
            domain = urlparse(url).netloc
            internal_links = sum(1 for link in all_links 
                               if link['href'].startswith('/') or domain in link['href'])
            external_links = len(all_links) - internal_links
            
            # Image analysis
            images = soup.find_all('img')
            total_images = len(images)
            images_with_alt = sum(1 for img in images if img.get('alt'))
            alt_ratio = (images_with_alt / total_images * 100) if total_images > 0 else 0
            
            # Content analysis
            text_content = soup.get_text(separator=' ', strip=True)
            word_count = len(text_content.split())
            
            # Technical SEO
            has_viewport = bool(soup.find('meta', attrs={'name': 'viewport'}))
            has_canonical = bool(soup.find('link', rel='canonical'))
            has_hreflang = bool(soup.find('link', rel='alternate', hreflang=True))
            has_schema = bool(soup.find('script', type='application/ld+json'))
            
            # Language detection
            html_tag = soup.find('html')
            lang_attr = html_tag.get('lang') if html_tag else None
            
            # Check for bilingual indicators
            has_arabic = bool(soup.find(attrs={'dir': 'rtl'}))
            has_lang_switcher = bool(soup.find('a', href=lambda x: x and ('/ar/' in x or '/en/' in x)))
            
            # OpenGraph tags
            og_tags = {}
            for meta in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
                prop = meta.get('property', '').replace('og:', '')
                content = meta.get('content', '')
                og_tags[prop] = content
            
            # Calculate scores
            seo_score = self._calculate_seo_score({
                'title_length': title_length,
                'desc_length': desc_length,
                'h1_count': h1_count,
                'alt_ratio': alt_ratio,
                'word_count': word_count,
                'has_viewport': has_viewport,
                'has_canonical': has_canonical,
                'has_schema': has_schema
            })
            
            localization_score = self._calculate_localization_score({
                'lang_attr': lang_attr,
                'has_hreflang': has_hreflang,
                'has_arabic': has_arabic,
                'has_lang_switcher': has_lang_switcher,
                'og_locale': 'locale' in og_tags
            })
            
            return {
                'url': url,
                'domain': domain,
                'timestamp': datetime.now().isoformat(),
                'title': title_text,
                'title_length': title_length,
                'meta_description': meta_desc_text,
                'desc_length': desc_length,
                'h1_count': h1_count,
                'h2_count': h2_count,
                'h3_count': h3_count,
                'internal_links': internal_links,
                'external_links': external_links,
                'total_images': total_images,
                'images_with_alt': images_with_alt,
                'alt_ratio': round(alt_ratio, 2),
                'word_count': word_count,
                'has_viewport': has_viewport,
                'has_canonical': has_canonical,
                'has_hreflang': has_hreflang,
                'has_schema': has_schema,
                'lang_attribute': lang_attr,
                'has_arabic_support': has_arabic,
                'has_lang_switcher': has_lang_switcher,
                'og_tags_count': len(og_tags),
                'seo_score': seo_score,
                'localization_score': localization_score,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error_message': str(e)
            }
    
    def _calculate_seo_score(self, metrics: Dict) -> int:
        """Calculate SEO score based on metrics"""
        score = 0
        
        # Title optimization (20 points)
        title_len = metrics['title_length']
        if 30 <= title_len <= 60:
            score += 20
        elif title_len > 0:
            score += 10
        
        # Meta description (15 points)
        desc_len = metrics['desc_length']
        if 120 <= desc_len <= 160:
            score += 15
        elif desc_len > 0:
            score += 8
        
        # H1 tags (10 points)
        if metrics['h1_count'] == 1:
            score += 10
        elif metrics['h1_count'] > 0:
            score += 5
        
        # Alt text (10 points)
        if metrics['alt_ratio'] >= 80:
            score += 10
        elif metrics['alt_ratio'] >= 50:
            score += 5
        
        # Content length (15 points)
        if metrics['word_count'] >= 300:
            score += 15
        elif metrics['word_count'] >= 150:
            score += 8
        
        # Technical SEO (30 points)
        if metrics['has_viewport']:
            score += 10
        if metrics['has_canonical']:
            score += 10
        if metrics['has_schema']:
            score += 10
        
        return min(score, 100)
    
    def _calculate_localization_score(self, metrics: Dict) -> int:
        """Calculate localization score"""
        score = 0
        
        if metrics['lang_attr']:
            score += 25
        if metrics['has_hreflang']:
            score += 25
        if metrics['has_arabic'] or metrics['has_lang_switcher']:
            score += 25
        if metrics['og_locale']:
            score += 25
        
        return score
    
    def analyze_all(self) -> List[Dict]:
        """Analyze all URLs with rate limiting"""
        print(f"Starting analysis of {len(self.urls)} URLs...")
        
        for i, url in enumerate(self.urls, 1):
            print(f"Analyzing {i}/{len(self.urls)}: {url}")
            result = self.analyze_single_url(url)
            self.results.append(result)
            
            # Rate limiting - be respectful
            if i < len(self.urls):
                time.sleep(2)
        
        print("Analysis complete!")
        return self.results
    
    def export_to_csv(self, filename: str = 'seo_analysis.csv'):
        """Export results to CSV"""
        if not self.results:
            print("No results to export")
            return
        
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"Results exported to {filename}")
    
    def export_to_json(self, filename: str = 'seo_analysis.json'):
        """Export results to JSON"""
        if not self.results:
            print("No results to export")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"Results exported to {filename}")
    
    def generate_comparison_report(self) -> str:
        """Generate a comparative analysis report"""
        if not self.results:
            return "No results available"
        
        successful = [r for r in self.results if r.get('status') == 'success']
        
        if not successful:
            return "No successful analyses"
        
        report = []
        report.append("=" * 80)
        report.append("SEO ANALYSIS COMPARISON REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total URLs Analyzed: {len(self.results)}")
        report.append(f"Successful Analyses: {len(successful)}")
        report.append("\n" + "-" * 80)
        
        # Overall statistics
        avg_seo = sum(r['seo_score'] for r in successful) / len(successful)
        avg_loc = sum(r['localization_score'] for r in successful) / len(successful)
        avg_words = sum(r['word_count'] for r in successful) / len(successful)
        
        report.append("\nOVERALL STATISTICS")
        report.append("-" * 80)
        report.append(f"Average SEO Score: {avg_seo:.2f}/100")
        report.append(f"Average Localization Score: {avg_loc:.2f}/100")
        report.append(f"Average Word Count: {avg_words:.0f}")
        
        # Best performers
        best_seo = max(successful, key=lambda x: x['seo_score'])
        best_loc = max(successful, key=lambda x: x['localization_score'])
        
        report.append("\n" + "-" * 80)
        report.append("BEST PERFORMERS")
        report.append("-" * 80)
        report.append(f"\nHighest SEO Score ({best_seo['seo_score']}/100):")
        report.append(f"  {best_seo['url']}")
        report.append(f"\nHighest Localization Score ({best_loc['localization_score']}/100):")
        report.append(f"  {best_loc['url']}")
        
        # Detailed per-URL analysis
        report.append("\n" + "-" * 80)
        report.append("DETAILED URL ANALYSIS")
        report.append("-" * 80)
        
        for result in successful:
            report.append(f"\n{result['url']}")
            report.append(f"  Domain: {result['domain']}")
            report.append(f"  SEO Score: {result['seo_score']}/100")
            report.append(f"  Localization Score: {result['localization_score']}/100")
            report.append(f"  Title Length: {result['title_length']} chars")
            report.append(f"  Description Length: {result['desc_length']} chars")
            report.append(f"  Word Count: {result['word_count']}")
            report.append(f"  Internal Links: {result['internal_links']}")
            report.append(f"  Images (with alt): {result['images_with_alt']}/{result['total_images']}")
            report.append(f"  Technical SEO:")
            report.append(f"    - Viewport: {'✓' if result['has_viewport'] else '✗'}")
            report.append(f"    - Canonical: {'✓' if result['has_canonical'] else '✗'}")
            report.append(f"    - Schema: {'✓' if result['has_schema'] else '✗'}")
            report.append(f"    - Hreflang: {'✓' if result['has_hreflang'] else '✗'}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, filename: str = 'seo_report.txt'):
        """Save the comparison report to a file"""
        report = self.generate_comparison_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to {filename}")


# Example usage
if __name__ == "__main__":
    # Your portfolio URLs
    urls = [
        "https://cfi.trade/en/jo/academy/course/asset-deep-dives/beginners-guide-to-the-financial-markets",
        "https://manateq.qa",
        "https://jcbank.com.jo",
        # Add more URLs as needed
    ]
    
    # Create analyzer instance
    analyzer = BatchSEOAnalyzer(urls)
    
    # Run analysis
    results = analyzer.analyze_all()
    
    # Export results
    analyzer.export_to_csv('portfolio_seo_analysis.csv')
    analyzer.export_to_json('portfolio_seo_analysis.json')
    
    # Generate and print report
    print("\n" + analyzer.generate_comparison_report())
    analyzer.save_report('portfolio_seo_report.txt')
    
    print("\n✓ Analysis complete! Check the generated files for results.")