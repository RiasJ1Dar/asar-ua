**Українська** · [English](README.en.md)

# asar-ua

Універсальний патчер локалі для Electron `app.asar`: розпакувати → застосувати
JSON-мапу рядків → запакувати → поставити з `.bak` / відкотити.

Antigravity лишається повним продакшен-паком у
[antigravity-ua](https://github.com/RiasJ1Dar/antigravity-ua); цей репо — **спільний
пайплайн** під наступні застосунки.

## Вимоги

Python 3.10+, без Node.js. Формат ASAR — чистий Python (адаптовано з antigravity-ua).

> Integrity-блоки всередині ASAR лишаються **SHA-256** — так вимагає Electron.
> Це не плутати з [ota-sign](https://github.com/RiasJ1Dar/ota-sign), де контент-хеш — SHA-512.

## CLI

```bash
pip install -e .

asar-ua extract app.asar ./tree
asar-ua apply ./tree profiles/demo/locale.uk.json
asar-ua pack ./tree app_uk.asar
asar-ua install /path/to/resources/app.asar ./app_uk.asar
asar-ua restore /path/to/resources/app.asar

# одним кроком:
asar-ua patch app.asar profiles/demo/locale.uk.json app_uk.asar
```

Мапа — JSON `{"English": "Українською", ...}`; довші ключі застосовуються першими.
Бінарні суфікси (шрифти, картинки, `.node`…) пропускаються.

## Профілі

`profiles/demo/` — мінімальний приклад. Новий застосунок = нова тека профілю з мапою.

## Ліцензія

MIT
