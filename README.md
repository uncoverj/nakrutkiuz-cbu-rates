# CBU emergency snapshot

This repository holds a public snapshot of the [Central Bank of Uzbekistan's
official rates](https://cbu.uz/ru/arkhiv-kursov-valyut/veb-masteram/). It was
seeded on 2 November 2026 because Oracle Dubai cannot reach `cbu.uz` directly.

The bot now refreshes rates automatically from Trustbank's dated CBU column
when the direct CBU API is unavailable. This repository is an emergency
fallback only. Its JSON includes a fetch timestamp and the bot rejects it
after 48 hours. The scheduled GitHub workflow was removed because this
account's Actions jobs were blocked by GitHub billing.

`fetch_rates.py` can refresh the file manually from a network that reaches the
CBU. No credentials or bot data belong in this repository.
