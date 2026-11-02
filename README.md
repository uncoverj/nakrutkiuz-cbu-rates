# Official CBU rate bridge

The Oracle Dubai VM cannot establish a TCP connection to `cbu.uz`. A separate
public GitHub repository contains only this script, the scheduled workflow and
the three public CBU rates. GitHub Actions fetches the [official JSON API](https://cbu.uz/ru/arkhiv-kursov-valyut/veb-masteram/)
every six hours. The bot first tries CBU directly, then downloads `rates.json`
from the public repository. A copy older than 48 hours is rejected. The bot
continues to reject purchases when its exchange rates are stale.

Place `fetch_rates.py` at the root of the public repository and
`refresh-rates.yml` at `.github/workflows/refresh-rates.yml`. Set the VM's
`CBU_MIRROR_URL` to the public raw GitHub URL. No bot code or secrets belong in
the public repository.
