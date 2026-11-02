"""Publish a small, timestamped copy of the official CBU JSON response."""
import json
import os
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

SOURCE = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
OUTPUT = Path(__file__).resolve().parent / 'rates.json'
REQUIRED = {'USD', 'EUR', 'RUB'}


def main():
    request = urllib.request.Request(SOURCE, headers={'User-Agent': 'NakrutkiUZ-CBU-Mirror/1.0'})
    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.load(response)
    if not isinstance(data, list):
        raise ValueError('Invalid CBU payload')
    today = datetime.now(timezone(timedelta(hours=5))).date()
    rows = {}
    for row in data:
        if row.get('Ccy') not in REQUIRED:
            continue
        code = row['Ccy']
        rate = float(row['Rate']) / float(row.get('Nominal', 1))
        effective = datetime.strptime(row['Date'], '%d.%m.%Y').date()
        if not 0 < rate or not 0 <= (today - effective).days <= 7:
            raise ValueError(f'Invalid {code} rate or date')
        rows[code] = {key: row[key] for key in ('Ccy', 'Rate', 'Nominal', 'Date')}
    if rows.keys() != REQUIRED:
        raise ValueError('Incomplete CBU payload')
    payload = {'source': SOURCE, 'fetched_ts': int(time.time()),
               'rates': [rows[code] for code in sorted(REQUIRED)]}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=OUTPUT.parent,
                                     prefix='.rates-', suffix='.json', delete=False) as stream:
        json.dump(payload, stream, ensure_ascii=False, separators=(',', ':'))
        stream.write('\n')
        tmp = Path(stream.name)
    os.replace(tmp, OUTPUT)
    print('Official CBU snapshot written:', ', '.join(sorted(rows)))


if __name__ == '__main__':
    main()
