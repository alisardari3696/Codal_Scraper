# Codal Scraper 📊

ابزار استخراج داده از کدال (Codal.ir) برای دریافت صورت‌های مالی و گزارش‌های شرکت‌های بورسی.

---

## 📖 درباره پروژه

این پروژه یک **داده‌کاو (Data Scraper)** برای وب‌سایت [کدال](https://codal.ir) است که به کمک آن می‌توان صورت‌های مالی، گزارش‌های میان‌دوره‌ای و سایر اطلاعیه‌های شرکت‌های پذیرفته‌شده در بورس تهران را به صورت خودکار دانلود کرد.

### 🎯 هدف بلندمدت

این کد **نمونه‌ی اولیه (Prototype)** یک سیستم بزرگ‌تر است. هدف نهایی:

1. **دریافت خودکار داده‌های مالی** از کدال برای تمام شرکت‌های بورسی
2. **تحلیل خودکار (Automated Analysis)** صورت‌های مالی
3. **مقایسه و رتبه‌بندی** شرکت‌ها بر اساس شاخص‌های مالی
4. **کمک به تحقیقات و سرمایه‌گذاری** با داده‌های ساخت‌یافته و آماده تحلیل

به عبارت دیگر، این پروژه می‌خواهد پلی باشد بین **داده‌های خام کدال** و **تصمیم‌گیری هوشمند سرمایه‌گذاری**.

---

## ⚠️ سلب مسئولیت (Disclaimer)

- این پروژه **هیچ‌گونه وابستگی رسمی** به سازمان بورس، کدال یا هیچ نهاد دولتی ندارد.
- **API مورد استفاده در این پروژه از طریق مهندسی معکوس (Reverse Engineering)** ترافیک شبکه‌ی وب‌سایت کدال کشف شده است و **مستندات رسمی و عمومی ندارد**.
- این API ممکن است **در هر زمان تغییر کند** یا **از دسترس خارج شود**.
- کد **فقط برای اهداف آموزشی، تحقیقاتی و شخصی** منتشر شده است.
- مسئولیت هرگونه استفاده‌ی نادرست، تجاری یا مغایر با قوانین، **بر عهده‌ی کاربر** است.
- لطفاً **به سرورهای کدال فشار نیاورید** — این ابزار با تأخیرهای محترمانه طراحی شده تا به سرویس آسیب نرساند.

---

## 🚀 ویژگی‌ها

- ✅ دریافت لیست کامل صورت‌های مالی سالانه و میان‌دوره‌ای
- ✅ پارس هم‌زمان پاسخ‌های **JSON** و **XML** (چون کدال بسته به درخواست، هر دو را برمی‌گرداند)
- ✅ تأخیر تصادفی بین درخواست‌ها برای جلوگیری از Rate Limit
- ✅ مدیریت خودکار خطای `HTTP 429` (Rate Limit) با صبر پلکانی
- ✅ دانلود موازی کنترل‌شده با `Semaphore`
- ✅ ذخیره‌سازی در پوشه‌ی مخصوص هر نماد
- ✅ رد کردن خودکار فایل‌های تکراری (از دانلود دوباره جلوگیری می‌کند)
- ✅ ورودی نماد با پیش‌فرض `فملی`
- ✅ اصلاح خودکار حروف عربی `ي` و `ك` به فارسی `ی` و `ک`
- ✅ سازگار با **Python 3.10+** و **Python 3.14**

---

## 📦 پیش‌نیازها

- **Python 3.10** یا بالاتر
- **aiohttp** برای درخواست‌های async

نصب پیش‌نیاز:

```bash
pip install aiohttp
```

> **نکته برای کاربران ایرانی:** اگر `pip` به دلیل تحریم یا کندی، نصب را انجام نداد، از آینه‌های داخلی استفاده کنید:
> ```bash
> pip install aiohttp -i https://mirror-pypi.runflare.com/simple/ --trusted-host mirror-pypi.runflare.com
> ```

---

## 🛠️ نصب و اجرا

### ۱) کلون کردن مخزن

```bash
git clone https://github.com/<your-username>/Codal_Scraper.git
cd Codal_Scraper
```

### ۲) نصب پیش‌نیاز

```bash
pip install aiohttp
```

### ۳) اجرا

```bash
python codal_scrape.py
```

سپس:

```
🔍 نماد مورد نظر را وارد کنید (مثلاً فملی):
```


سپس لیست تمام صورت‌های مالی نمایش داده می‌شود و می‌توانید:

- `y` بزنید → دانلود همه
- شماره‌ها را با کاما وارد کنید (مثلاً `1,3,5,10-20`) → دانلود انتخابی
- `n` بزنید → انصراف

---

## 📂 ساختار خروجی

فایل‌های دانلودشده در پوشه‌ی کنار اسکریپت ذخیره می‌شوند:

```
Codal_Scraper/
├── codal_scrape.py
├── README.md
└── codal_data/
    ├── فملی/
    │   ├── فملی_۱۴۰۵-۰۶-۰۴_۱۵-۵۳-۴۱_گزارش فعالیت ماهانه ....xls
    │   └── ...
    ├── فولاد/
    │   └── ...
    └── شستا/
        └── ...
```

---

## ⚙️ تنظیمات

### تغییر دسته‌بندی اطلاعیه‌ها(ممکنه اعداد متفاوت باشند باید تست شود!)

در متغیر `BASE_PARAMS`، پارامتر `Category` را تغییر دهید:

| Category | نوع اطلاعیه |
|----------|-------------|
| `1` | اطلاعات و صورت‌های مالی سالانه ✅ (پیش‌فرض) |
| `2` | افشای اطلاعات بااهمیت و شفاف‌سازی |
| `3` | گزارش عملکرد ماهانه |
| `4` | اساسنامه / امیدنامه |
| `5` | اطلاعات هیئت مدیره و کمیته حسابرسی |
| `6` | آگهی دعوت به مجامع و تصمیمات |
| `7` | افزایش سرمایه |
| `8` | شفاف‌سازی مربوط به بورس/فرابورس |
| `9` | شفاف‌سازی مربوط به سازمان |
| `10` | سایر |
| `11` | اوراق بدهی |
| `-1` | همه (⚠️ ممکن است منجر به Rate Limit شدید شود) |

مثال:

```python
BASE_PARAMS = {
    "Category": "3",   # ← تغییر به گزارش عملکرد ماهانه
    ...
}
```

### تغییر تأخیر بین درخواست‌ها

برای جلوگیری از Rate Limit، می‌توانید مقدار تأخیر را در تابع `get_all_letters` تغییر دهید:

```python
for p in range(2, total_pages + 1):
    await asyncio.sleep(1.0)   # ← افزایش به 2.0 یا 3.0 اگر بلاک شدی
```

### تغییر تعداد اتصال‌های هم‌زمان

```python
connector = aiohttp.TCPConnector(limit=3, ssl=False)   # ← کاهش به 2 یا 1 اگر بلاک شدی
```

---

## 🧠 چطور کار می‌کند؟

### ۱) کشف API
API `https://search.codal.ir/api/search/v2/q` از طریق **مهندسی معکوس (Reverse Engineering)** ترافیک شبکه‌ی وب‌سایت کدال کشف شده است. برای این کار:

1. در مرورگر، `F12` را بزنید (Developer Tools)
2. به تب **Network** بروید
3. در سایت کدال یک جستجو انجام دهید
4. درخواست ارسال‌شده به سرور را مشاهده کنید
5. پارامترهای URL را استخراج کنید

### ۲) پارامترهای کلیدی API

| پارامتر | توضیح | مثال |
|---------|-------|------|
| `Symbol` | نماد شرکت | `فملی` |
| `Category` | نوع اطلاعیه | `1` |
| `PageNumber` | شماره صفحه | `1` |
| `Audited` | حسابرسی شده | `true` |
| `NotAudited` | حسابرسی نشده | `true` |
| `Mains` | شرکت اصلی | `true` |
| `Childs` | زیرمجموعه‌ها | `false` |
| `Length` | طول دوره | `-1` (همه) |
| `search` | فعال‌سازی جستجو | `true` |

### ۳) بهینه‌سازی با هوش مصنوعی
کد اولیه از مخزن [Aghpour/Codal_Scraping](https://github.com/Aghpour/Codal_Scraping) گرفته شده و سپس توسط **هوش مصنوعی (Claude)** بهینه‌سازی و بازنویسی شده است. بهبودها شامل:

- پارس هم‌زمان JSON و XML (کد اصلی فقط JSON را می‌خواند)
- مدیریت خطای 429 با Retry پلکانی
- تأخیر بین صفحات (کد اصلی همه را موازی می‌فرستاد)
- حذف `os.chdir` و استفاده از `pathlib.Path` (جلوگیری از Race Condition)
- حذف وابستگی به `urllib` و `nest_asyncio`
- اضافه شدن `User-Agent` واقعی مرورگر
- پشتیبانی از Python 3.14

---

## ⚠️ محدودیت‌ها

- **Rate Limit:** کدال به درخواست‌های مکرر حساس است و IP شما را موقتاً (۵-۱۵ دقیقه) بلاک می‌کند. برای کار با حجم بالا، بین درخواست‌ها تأخیر بگذارید یا IP خود را تغییر دهید.
- **تغییر API:** چون مستندات رسمی وجود ندارد، اگر کدال ساختار API را تغییر دهد، این کد از کار می‌افتد.
- **فقط داده‌های عمومی:** این ابزار فقط به داده‌های عمومی کدال دسترسی دارد.
- **کاربران ایرانی:** ممکن است برای دسترسی به کدال نیاز به VPN یا اینترنت پایدار داشته باشید.

---

## 🔮 نقشه‌ی راه (Roadmap)

- [x] دریافت لیست صورت‌های مالی
- [x] دانلود فایل‌های Excel
- [ ] افزودن رابط گرافیکی (GUI) با `tkinter` یا `PyQt`
- [ ] افزودن دیتابیس (SQLite) برای ذخیره‌ی متادیتا
- [ ] تحلیل خودکار صورت‌های مالی با `pandas`
- [ ] محاسبه‌ی نسبت‌های مالی (P/E، ROE، ROA و ...)
- [ ] رسم نمودارهای مالی
- [ ] ساخت API خودمان برای دسترسی راحت‌تر
- [ ] پشتیبانی از نمادهای چندگانه به صورت هم‌زمان
- [ ] اکسپورت به فرمت CSV و JSON

---

## 🤝 مشارکت

از مشارکت شما استقبال می‌شود! برای مشارکت:

1. مخزن را Fork کنید
2. یک برنچ جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را Commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. یک Pull Request باز کنید

---

## 📜 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است. برای جزئیات بیشتر، فایل [LICENSE](LICENSE) را ببینید.

---

## 🙏 تقدیر و تشکر

- از [Aghpour](https://github.com/Aghpour/Codal_Scraping) برای کد اولیه
- از تیم کدال برای فراهم کردن داده‌های عمومی
- از انجمن متن‌باز پایتون ایران

---

## 📞 تماس

- **GitHub:** [@your-username](https://github.com/your-username)
- **Email:** alisardari3696@yahoo.com

---

## 🌟 حمایت

اگر این پروژه برایتان مفید بود، لطفاً یک ⭐ به آن بدهید. این کار انگیزه‌ی ادامه‌ی کار را دوچندان می‌کند.

---

# Codal Scraper (English)

A data scraper for [Codal.ir](https://codal.ir) — the official disclosure system of Tehran Stock Exchange — to download financial statements and periodic reports of listed companies.

## ⚠️ Disclaimer

This project is **not officially affiliated** with Codal, TSE, or any governmental body. The API used here was discovered through **reverse engineering** of Codal's network traffic and has **no public documentation**. Use it responsibly and only for educational/personal purposes.

## ✨ Features

- Download annual and interim financial statements
- Parse both JSON and XML responses
- Randomized delays to avoid rate limiting
- Automatic retry on HTTP 429
- Controlled parallel downloads
- Per-symbol folder structure
- Skip already-downloaded files

## 🚀 Quick Start

```bash
pip install aiohttp
python codal_scrape.py
```

Enter a symbol (e.g., `فملی`) or press Enter for the default (`فملی`).

## 📖 Roadmap

- [x] List financial statements
- [x] Download Excel files
- [ ] GUI
- [ ] Database (SQLite)
- [ ] Automated financial analysis
- [ ] Financial ratio calculation
- [ ] Charting
- [ ] CSV/JSON export

## 📜 License

MIT
