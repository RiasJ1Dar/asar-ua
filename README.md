**Українська** · [English](README.en.md)

# asar-ua

Універсальний патчер локалі для Electron `app.asar`: розпакувати архів,
застосувати JSON-мапу рядків, запакувати результат, встановити його з резервною
копією або відкотити зміни.

Повний пакет локалізації Antigravity залишається в
[antigravity-ua](https://github.com/RiasJ1Dar/antigravity-ua). Цей репозиторій
містить спільний пайплайн, який можна використати для інших Electron-застосунків.

## Вимоги

- Python 3.10 або новіший.
- Node.js не потрібен: читання й запис ASAR реалізовані на Python.
- Перед `install` або `restore` закрий Electron-застосунок, який використовує архів.

Integrity-блоки всередині ASAR залишаються на SHA-256, як очікує Electron.
SHA-512 у [ota-sign](https://github.com/RiasJ1Dar/ota-sign) належить іншому
рівню: доставці оновлень.

## Встановлення

```bash
git clone https://github.com/RiasJ1Dar/asar-ua.git
cd asar-ua
python -m pip install -e .
```

## Швидкий сценарій

```bash
asar-ua extract app.asar ./tree
asar-ua apply ./tree profiles/demo/locale.uk.json
asar-ua pack ./tree app_uk.asar
asar-ua install /path/to/resources/app.asar ./app_uk.asar

# повернути оригінал
asar-ua restore /path/to/resources/app.asar
```

Те саме розпакування, заміни й пакування однією командою:

```bash
asar-ua patch app.asar profiles/demo/locale.uk.json app_uk.asar
```

## Команди

| Команда | Дія |
|---|---|
| `extract ASAR OUT` | Розпакувати `app.asar` у теку |
| `apply TREE MAP_JSON` | Застосувати мапу до розпакованого дерева |
| `pack TREE OUT_ASAR` | Запакувати дерево в новий ASAR |
| `install TARGET_ASAR NEW_ASAR` | Створити `.bak` один раз і замінити ціль |
| `restore TARGET_ASAR` | Відновити ціль із `.bak` |
| `patch ASAR MAP_JSON OUT_ASAR [--work DIR]` | Виконати extract, apply і pack |

Без `--work` команда `patch` створює робочу теку поруч із вихідним ASAR.
Якщо вказана робоча тека вже існує, вона буде заново створена; не використовуй
для `--work` теку з потрібними файлами.

## Формат мапи

```json
{
  "Settings": "Налаштування",
  "Check for updates": "Перевірити оновлення"
}
```

Мапа має бути JSON-об'єктом `рядок → рядок`. Порожні й нестрокові пари
ігноруються. Довші ключі застосовуються першими, але заміна все одно є точним
пошуком підрядка, а не синтаксичним розбором JavaScript.

Під час `apply`:

- текстові файли читаються як UTF-8;
- файли, які не читаються як UTF-8, пропускаються;
- шрифти, зображення, медіа, `.node`, `.dll`, `.exe`, `.wasm` та інші
  відомі бінарні суфікси не змінюються;
- CLI друкує кількість змінених файлів і замін.

## Профілі

`profiles/demo/` містить мінімальний приклад. Для нового застосунку створи
окрему теку профілю з власною мапою та короткою інструкцією. Сам патчер не
прив'язаний до української мови: значеннями можуть бути будь-які рядки.

## Резервна копія

`install` створює `app.asar.bak` лише тоді, коли резервної копії ще немає.
Наступні встановлення її не перезаписують. `restore` копіює цей файл назад;
якщо `.bak` відсутній, команда завершується помилкою.

## Перевірка розробки

```bash
python -m asar_ua --help
python -m asar_ua patch --help
```

## Ліцензія

MIT