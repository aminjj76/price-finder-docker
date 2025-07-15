FROM python:3.9-alpine

WORKDIR /app

# نصب dependencies سیستم
RUN apk add --no-cache gcc g++ musl-dev

# کپی requirements
COPY requirements.txt .

# نصب Python packages
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد
COPY . .

# تنظیم متغیرهای محیطی
ENV PYTHONPATH=/app
ENV FLASK_APP=finder_price.py

# پورت
EXPOSE 5000

# اجرا
CMD ["python", "finder_price.py"]