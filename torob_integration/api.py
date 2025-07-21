import requests
import json
import time
import random
import urllib.parse

class Torob:
    def __init__(self):
        self.base_url = "https://api.torob.com/v4"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'fa-IR,fa;q=0.9,en;q=0.8',
            'Referer': 'https://torob.com/',
        }
    
    def search(self, q, page=0):
        """جستجو در ترب با استفاده از API اصلی"""
        print(f"🔍 Torob API: جستجو برای '{q}' در صفحه {page}")
        
        try:
            # استفاده از API اصلی مطابق با setup.py
            url = f"{self.base_url}/base-product/search/"
            params = {
                'q': q,
                'page': page
            }
            
            print(f"📡 درخواست به: {url}")
            print(f"📋 پارامترها: {params}")
            
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📦 داده دریافت شد: {type(data)}")
                
                # پردازش داده‌ها مطابق با api.py
                processed_data = self._process_search_data(data)
                
                if processed_data and processed_data.get('results'):
                    print(f"✅ API موفق: {len(processed_data['results'])} محصول")
                    return processed_data
                else:
                    print("❌ داده‌های معتبری دریافت نشد")
                    return None
            else:
                print(f"❌ خطای HTTP: {response.status_code}")
                print(f"📄 پاسخ: {response.text[:200]}...")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ خطای Timeout")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ خطای اتصال")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ خطای JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ خطای عمومی: {e}")
            return None
    
    def _process_search_data(self, data):
        """پردازش داده‌های جستجو مطابق با api.py"""
        try:
            if not data or not isinstance(data, dict):
                return None
            
            # بررسی وجود results
            if 'results' not in data:
                print("❌ فیلد results یافت نشد")
                return None
            
            results = data['results']
            if not isinstance(results, list):
                print("❌ results یک لیست نیست")
                return None
            
            print(f"📋 پردازش {len(results)} محصول...")
            
            # پردازش هر محصول مطابق با __get_search_data_from_url
            for item in results:
                if 'more_info_url' in item and item['more_info_url']:
                    try:
                        # استخراج prk و search_id از more_info_url
                        more_info_url = item['more_info_url']
                        
                        # استخراج prk
                        prk_start = more_info_url.find("prk=")
                        if prk_start != -1:
                            prk_start += 4
                            prk_end = more_info_url.find("&", prk_start)
                            if prk_end == -1:
                                prk_end = len(more_info_url)
                            item["prk"] = more_info_url[prk_start:prk_end]
                        
                        # استخراج search_id
                        search_id_start = more_info_url.find("search_id=")
                        if search_id_start != -1:
                            search_id_start += 10
                            search_id_end = more_info_url.find("&", search_id_start)
                            if search_id_end == -1:
                                search_id_end = len(more_info_url)
                            item["search_id"] = more_info_url[search_id_start:search_id_end]
                        
                        print(f"✅ محصول پردازش شد: prk={item.get('prk', 'N/A')}, search_id={item.get('search_id', 'N/A')}")
                        
                    except Exception as e:
                        print(f"❌ خطا در پردازش more_info_url: {e}")
                        continue
            
            return data
            
        except Exception as e:
            print(f"❌ خطا در پردازش داده‌ها: {e}")
            return None
    
    def details(self, prk, search_id=None):
        """دریافت جزئیات محصول مطابق با API"""
        try:
            if not prk:
                return {}
            
            url = f"{self.base_url}/base-product/details/"
            params = {'prk': prk}
            if search_id:
                params['search_id'] = search_id
            
            print(f"📡 درخواست جزئیات: {url}")
            print(f"📋 پارامترها: {params}")
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ جزئیات دریافت شد")
                return data
            else:
                print(f"❌ خطا در دریافت جزئیات: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ خطا در details: {e}")
            return {}
    
    def suggestion(self, q):
        """پیشنهادات محصول"""
        try:
            url = "https://api.torob.com/suggestion2/"
            params = {"q": q}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ خطا در suggestion: {e}")
            return {}
    
    def special_offers(self, page=0):
        """پیشنهادات ویژه"""
        try:
            url = f"{self.base_url}/special-offers/"
            params = {"page": page}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ خطا در special_offers: {e}")
            return {}
    
    def price_chart(self, prk, search_id=None):
        """نمودار قیمت محصول"""
        try:
            url = f"{self.base_url}/base-product/price-chart/"
            params = {"prk": prk}
            if search_id:
                params['search_id'] = search_id
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"❌ خطا در price_chart: {e}")
            return {}