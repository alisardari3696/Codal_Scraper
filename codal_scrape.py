import asyncio
import aiohttp
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

MAIN_DIR = Path(__file__).parent / "codal_data"
MAIN_DIR.mkdir(exist_ok=True)

BASE_URL = "https://search.codal.ir/api/search/v2/q"

BASE_PARAMS = {
    "Audited": "true",
    "AuditorRef": "-1",
    "Category": "1",
    "Childs": "false",
    "CompanyState": "0",
    "CompanyType": "-1",
    "Consolidatable": "true",
    "IsNotAudited": "false",
    "Length": "-1",
    "LetterType": "-1",
    "Mains": "true",
    "NotAudited": "true",
    "NotConsolidatable": "true",
    "Publisher": "false",
    "TracingNo": "-1",
    "search": "true",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8",
    "Referer": "https://codal.ir/",
}


def build_url(symbol: str, page: int = 1) -> str:
    params = dict(BASE_PARAMS)
    params["Symbol"] = quote(symbol)
    params["PageNumber"] = str(page)
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{BASE_URL}?{query}"


def parse_response(text: str):
    """هم JSON و هم XML رو پارس می‌کنه"""
    text = text.strip()
    if not text:
        return None

    # اول JSON امتحان کن
    if text.startswith("{"):
        try:
            data = json.loads(text)
            return {
                "Page": data.get("Page", 1),
                "Total": data.get("Total", 0),
                "Letters": data.get("Letters", []),
            }
        except json.JSONDecodeError:
            pass

    # XML رو پارس کن
    if text.startswith("<"):
        try:
            # namespace رو حذف کن تا پارس ساده‌تر شه
            text_clean = text.replace(
                'xmlns="http://schemas.datacontract.org/2004/07/Codal.Services.Model.Dto.Search"',
                ""
            ).replace(
                'xmlns:i="http://www.w3.org/2001/XMLSchema-instance"',
                ""
            ).replace(
                'xmlns:d5p1="http://schemas.microsoft.com/2003/10/Serialization/Arrays"',
                ""
            )
            root = ET.fromstring(text_clean)

            letters = []
            for letter in root.findall(".//CodalLetterHeaderDto"):
                def get(tag):
                    el = letter.find(tag)
                    return el.text if el is not None and el.text else ""
                letters.append({
                    "Symbol": get("Symbol"),
                    "Title": get("Title"),
                    "ExcelUrl": get("ExcelUrl"),
                    "PublishDateTime": get("PublishDateTime"),
                    "TracingNo": get("TracingNo"),
                    "PdfUrl": get("PdfUrl"),
                })

            page_el = root.find("Page")
            total_el = root.find("Total")
            return {
                "Page": int(page_el.text) if page_el is not None and page_el.text else 1,
                "Total": int(total_el.text) if total_el is not None and total_el.text else 0,
                "Letters": letters,
            }
        except ET.ParseError as e:
            print(f"  ✗ خطای پارس XML: {e}")
            return None

    return None


async def fetch_json(session, url, retries=4):
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as r:
                if r.status == 200:
                    text = await r.text()
                    parsed = parse_response(text)
                    if parsed:
                        return parsed
                    else:
                        print(f"  ⚠️ پاسخ نامعتبر (تلاش {attempt+1})")
                elif r.status == 429:
                    wait = 5 * (attempt + 1)
                    print(f"  ⏳ rate limit — {wait} ثانیه صبر...")
                    await asyncio.sleep(wait)
                    continue
        except Exception as e:
            if attempt == retries - 1:
                print(f"  ✗ خطا: {e}")
                return None
            await asyncio.sleep(2 * (attempt + 1))
    return None


async def fetch_file(session, url, dest: Path):
    if dest.exists() and dest.stat().st_size > 0:
        return "exists"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as r:
            if r.status != 200:
                return f"http_{r.status}"
            data = await r.read()
            if not data:
                return "empty"
            with open(dest, "wb") as f:
                f.write(data)
            return "ok"
    except Exception as e:
        return f"error: {e}"


async def get_all_letters(session, symbol: str):
    first = await fetch_json(session, build_url(symbol, 1))
    if not first:
        print("❌ صفحه اول جواب نداد — دوباره امتحان کن یا چند دقیقه صبر کن")
        return []

    total_pages = first.get("Page", 1)
    total_files = first.get("Total", 0)
    print(f"\n📊 سهم: {symbol} | صفحات: {total_pages} | کل فایل‌ها: {total_files}\n")

    all_letters = list(first.get("Letters", []))

    # یکی‌یکی با تأخیر (نه موازی) → کدال بلاک نمی‌کنه
    for p in range(2, total_pages + 1):
        await asyncio.sleep(1.0)
        print(f"  ⏳ دریافت صفحه {p}/{total_pages}...")
        r = await fetch_json(session, build_url(symbol, p))
        if r:
            all_letters.extend(r.get("Letters", []))
        else:
            print(f"  ⚠️ صفحه {p} جواب نداد")

    return all_letters


async def main():
    symbol = input("🔍 نماد مورد نظر را وارد کنید (مثلاً فملی): ").strip()
    symbol = symbol.replace('ي', 'ی').replace('ك', 'ک')

    if not symbol:
        print("نماد خالی است!")
        return

    t0 = time.perf_counter()

    connector = aiohttp.TCPConnector(limit=3, ssl=False)
    async with aiohttp.ClientSession(connector=connector, headers=HEADERS) as session:
        letters = await get_all_letters(session, symbol)

        if not letters:
            print("❌ هیچ داده‌ای پیدا نشد.")
            return

        print("=" * 90)
        print(f"{'#':<4} {'تاریخ':<20} {'عنوان':<55}")
        print("=" * 90)
        for idx, letter in enumerate(letters, 1):
            title = letter.get("Title", "بدون عنوان")[:53]
            date = letter.get("PublishDateTime", "")[:19]
            print(f"{idx:<4} {date:<20} {title}")
        print("=" * 90)
        print(f"\n📁 {len(letters)} مورد پیدا شد.\n")

        choice = input("همه دانلود شود؟ (y) / انتخاب شماره‌ها با کاما / هیچ (n): ").strip().lower()

        if choice in ("n", ""):
            print("خدانگهدار!")
            return

        if choice == "y":
            selected = list(range(len(letters)))
        else:
            try:
                selected = [int(x.strip()) - 1 for x in choice.split(",") if x.strip()]
                selected = [i for i in selected if 0 <= i < len(letters)]
            except ValueError:
                print("ورودی نامعتبر!")
                return

        ticker_dir = MAIN_DIR / symbol
        ticker_dir.mkdir(exist_ok=True)

        downloads = []
        for i in selected:
            letter = letters[i]
            excel_url = letter.get("ExcelUrl")
            if not excel_url:
                continue
            title = letter.get("Title", "no_title").replace("/", "_").replace("\\", "_")[:80]
            date = letter.get("PublishDateTime", "").replace("/", "-").replace(":", "-")[:19]
            filename = f"{symbol}_{date}_{title}.xls"
            dest = ticker_dir / filename
            if dest.exists():
                continue
            downloads.append((excel_url, dest, filename))

        print(f"\n⬇️  شروع دانلود {len(downloads)} فایل...\n")

        sem = asyncio.Semaphore(3)
        async def limited(url, dest, name):
            async with sem:
                res = await fetch_file(session, url, dest)
                icon = "✓" if res == "ok" else "✗"
                print(f"  {icon} {name}  [{res}]")
                return res

        tasks = [limited(u, d, n) for u, d, n in downloads]
        results = await asyncio.gather(*tasks)

        ok = sum(1 for r in results if r == "ok")
        print(f"\n✅ موفق: {ok} | ❌ ناموفق: {len(results) - ok}")
        print(f"📂 مسیر: {ticker_dir}")
        print(f"⏱️  زمان: {time.perf_counter() - t0:.1f} ثانیه")


if __name__ == "__main__":
    asyncio.run(main())
