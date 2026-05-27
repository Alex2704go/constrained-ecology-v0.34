# find_all_md_files.py
import urllib.request
import re
import concurrent.futures

ids = [
    "11XVElY_0YzO4S-x2VM7fDW0aSxy8fQAb",
    "11p2YwRDth4f8W9bgSkrSZGqG7v2mT9CM",
    "12SYqFkJK1S9TzDR9vjRFKHLdjuHzQzJf",
    "13avZNwFGJkJU_vJ_kkm0U-nHQ--cXoA1",
    "13naoq2xX6h9mXlO_bquwb-UOPYjYpoz5",
    "14Csy9wEbDE4sUgmVwN7l8hWs8v5VBdUp",
    "14Ez6dT-YbvRWnssIouhpLX7cPoGiB2XC",
    "15JUEj4AGsM67LWuMJ0gRrE5lQaG_9fdh",
    "15eXgm9d5EZZvc91ksvIKfbupW9-_VD0j",
    "15p0jqUOur0OjaoTrcRweYnNXfQqV8ynX",
    "15rYSwcu_YuWVUAaU83Dz-oj1JT11rt8X",
    "17fk0r1gXkIpyOA__UFfHxGOU2RWSKXx8",
    "18zQRoSp-JzUMMNsA8w-7Jqfuc2SIyhl4",
    "19yti0-jVl-UoBHOPOHMsn34GelTka4z3",
    "1AjQolmQOivNlrHQ_ADSdnlFv8z1MxTKz",
    "1BtNEw2UPvWECY0QHHWW3_WmoWUMaVgyF",
    "1Dsf8Fo9m1V4ibGF1w5xenJf3Ab0Q19_u",
    "1H7wWzySV8yjgH7szMsOBeM2Z-MgZeFr1",
    "1J3NA5tBCZ3yw65cG5lfTMYlv7BL332k5",
    "1JvUCPhmU6dJskvHIeaqemlyushv5hJDB",
    "1Jwjg216dO3ITrNsWVslgSZg2LJKZb-Yv",
    "1Lq1b6wCIZF8LQJ3aJCITcrvQt9KoQcE0",
    "1OQEDWgiPrRb8-4zZQfJB_SrqUEqfgWAC",
    "1PF-YLxuH0HLyBv8bpF23W9ZEg9m46ZqZ",
    "1P_8VcylcICGc8a9LJOOvpvqWMT_097op",
    "1Rrs_sO_fEpfmuGwAWVHc_s1N7TlB-dwX",
    "1SdovdCl-281EdsqAQZmuo2Cz36GszMJX",
    "1Vc4I21zcTyVqVyBIfN5yYnI9cukdVEba",
    "1X2D9NFhgbAJTTEJXp-9oNF6pFqiIWrbQ",
    "1Zf_n-_ntYzlx4c_V08f42Djlp2KIwdI0",
    "1b6gATBnl9q-q_JXMPXjqtTFRkaKPJscU",
    "1bdNFpzx-akimJmZPwII62tqQWKJwQbrs",
    "1chqUhN1kZdDMnbdVd5Ed4nUq1K5aMzE7",
    "1ckl8Xtel9PfGwbhTNHKWaJNx1h6XA7S8",
    "1dd3tjzUungfbviX5COFs5enex_XUNvHy",
    "1gg1B0x4NUqqAlGdzuBRlmFdOz12xML_u",
    "1gsNwpuwDdOi2Adj5kDw3XGKFB-MDWqWW",
    "1hMzVhFpTOlL5cg73zTucoSmxtcAJJa3A",
    "1kx8u8mUAOfDO9tcgl9ix83W9uoQ4ZTbr",
    "1mv6UrJiByQ0XYDUzmnWD2LbBleV2H0js",
    "1nSNQ7RfM-zRX4jCg926TUmfslBWUobYr",
    "1nkiMUbfFP9q4V70Me78iXVB8ECM-8She",
    "1rw9A6pTDec06Kjiv3F5kFbDG1cQ2X4u7",
    "1tY6VNUJ62hn0pcYM7IyQGBCvaf7P82FG",
    "1uEktrgniHiwNICum4-foZlNEbfSz1Pno",
    "1uMwitM29IGEy_6w7lOKn5oKiu__dxTzt",
    "1wuk2gmimlSM7pueqKJVxixSXgPgq09Th",
    "1xPwOpgB29CJRNY8nH84Jwi8NQuhI-vUZ",
    "1xs21fTd84UE2GaqBoN2RWCptpusK0Zqw",
    "1yJmJGcEG04t1qWXcQPG5n2L4A6XSJa8v",
    "1zily2KUWO9PKqMSx4SV0-m6Uq4wJg0ip"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scan_folder(folder_id):
    url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        # Search for any markdown (.md) or text (.txt) files
        md_files = re.findall(r'"([^"\\]+\.(?:md|txt))"', html)
        # Search for CSV/Parquet files
        data_files = re.findall(r'"([^"\\]+\.(?:xlsx|csv|parquet))"', html)
        
        return folder_id, md_files, data_files
    except:
        return folder_id, [], []

print("Scanning all Google Drive subfolders...")
with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    results = list(executor.map(scan_folder, ids))

print("\nScan Results:")
for folder_id, mds, datas in results:
    if mds or datas:
        # Get title
        print(f"Folder: {folder_id}")
        if mds:
            print(f" -> Markdown/Text files: {mds}")
        if datas:
            print(f" -> Data files: {datas}")
