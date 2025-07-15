import requests
import json
import time
import random

class Torob:
    def __init__(self):
        self.base_url = "https://api.torob.com/v4"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'fa-IR,fa;q=0.9,en;q=0.8',
            'Referer': 'https://torob.com/',
        }
    
    def search(self, query, page=0):
        """جستجو در ترب با چندین روش"""
        print(f"🔍 Torob API: جستجو برای '{query}'")
        
        # روش 1: API اصلی
        result = self._try_main_api(query, page)
        if result and result.get('results'):
            print(f"✅ API اصلی موفق: {len(result['results'])} محصول")
            return result
        
        # روش 2: API جایگزین
        result = self._try_alternative_api(query, page)
        if result and result.get('results'):
            print(f"✅ API جایگزین موفق: {len(result['results'])} محصول")
            return result
        
        # روش 3: وب اسکرپینگ
        result = self._try_web_scraping(query)
        if result and result.get('results'):
            print(f"✅ وب اسکرپینگ موفق: {len(result['results'])} محصول")
            return result
        
        # روش 4: داده‌های شبیه‌سازی شده
        print("⚠️ همه روش‌ها شکست خورد، استفاده از داده‌های شبیه‌سازی")
        return self._generate_mock_data(query)
    
    def _try_main_api(self, query, page):
        """تلاش با API اصلی"""
        try:
            url = f"{self.base_url}/base-search/"
            params = {
                'q': query,
                'page': page,
                'size': 24
            }
            
            print(f"📡 درخواست به: {url}")
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📦 داده دریافت شد: {type(data)}")
                return data
            else:
                print(f"❌ خطای HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ خطا در API اصلی: {e}")
            return None
    
    def _try_alternative_api(self, query, page):
        """تلاش با API جایگزین"""
        try:
            # API جایگزین ترب
            url = "https://api.torob.com/v4/product-search/"
            params = {
                'query': query,
                'page': page
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"❌ خطا در API جایگزین: {e}")
            return None
    
    def _try_web_scraping(self, query):
        """وب اسکرپینگ از ترب"""
        try:
            import urllib.parse
            from bs4 import BeautifulSoup
            import re
            
            encoded_query = urllib.parse.quote(query)
            url = f"https://torob.com/search/?query={encoded_query}"
            
            headers = {
                'User-Agent': self.headers['User-Agent'],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'fa-IR,fa;q=0.9,en;q=0.8',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                
                # جستجوی محصولات در HTML
                product_elements = soup.find_all(['div', 'article'], class_=re.compile(r'product|item'))
                
                for i, element in enumerate(product_elements[:10]):
                    try:
                        # استخراج نام
                        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'a'], string=True)
                        title = title_elem.get_text().strip() if title_elem else f"{query} - محصول {i+1}"
                        
                        # استخراج قیمت
                        price_elem = element.find(string=re.compile(r'[\d,]+.*تومان|[\d,]+.*ریال'))
                        price = None
                        
                        if price_elem:
                            price_text = price_elem.strip()
                            numbers = re.findall(r'[\d,]+', price_text.replace('٬', ','))
                            if numbers:
                                price = int(numbers[0].replace(',', ''))
                                if 'ریال' in price_text:
                                    price = price // 10
                        
                        if price and price > 1000:
                            results.append({
                                'name1': title,
                                'price': price,
                                'prk': f"scraped-{i}",
                                'image_url': None,
                                'shops': [{'name': 'ترب', 'price': price}]
                            })
                    except:
                        continue
                
                return {'results': results} if results else None
            
            return None
            
        except Exception as e:
            print(f"❌ خطا در وب اسکرپینگ: {e}")
            return None
    
    def _generate_mock_data(self, query):
        """تولید داده‌های شبیه‌سازی شده"""
        results = []
        base_price = random.randint(100000, 2000000)
        
        for i in range(5):
            variation = random.randint(-50000, 100000)
            price = base_price + variation
            
            results.append({
                'name1': f"{query} - مدل {i+1}",
                'price': price,
                'prk': f"mock-{i}",
                'image_url': None,
                'shops': [
                    {
                        'name': f'فروشگاه {i+1}',
                        'price': price + random.randint(-10000, 10000)
                    }
                ]
            })
        
        return {'results': results}
    
    def details(self, prk, search_id=None):
        try:
            url = f"{self.base_url}/product-page/"
            params = {'prk': prk}
            if search_id:
                params['search_id'] = search_id
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            print(f"Error in Torob details: {e}")
            return {}