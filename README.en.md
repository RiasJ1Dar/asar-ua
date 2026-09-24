[Українська](README.md) · **English**

# asar-ua

A reusable locale patcher for Electron `app.asar`: extract an archive, apply a
JSON string map, pack the result, install it with a backup, or restore the
original.

The complete Antigravity localization remains in
[antigravity-ua](https://github.com/RiasJ1Dar/antigravity-ua). This repository
contains the shared pipeline that can be reused for other Electron applications.

## Requirements

- Python 3.10 or newer.
- Node.js is not required; ASAR reading and writing are implemented in Python.
- Close the Electron application before `install` or `restore`.

ASAR integrity blocks remain SHA-256, as expected by Electron. SHA-512 in
[ota-sign](https://github.com/RiasJ1Dar/ota-sign) belongs to the separate update
delivery layer.

## Installation

```bash
git clone https://github.com/RiasJ1Dar/asar-ua.git
cd asar-ua
python -m pip install -e .
```

## Quick workflow

```bash
asar-ua extract app.asar ./tree
asar-ua apply ./tree profiles/demo/locale.uk.json
asar-ua pack ./tree app_uk.asar
asar-ua install /path/to/resources/app.asar ./app_uk.asar

# restore the original
asar-ua restore /path/to/resources/app.asar
```

Run extract, replace, and pack in one command:

```bash
asar-ua patch app.asar profiles/demo/locale.uk.json app_uk.asar
```

## Commands

| Command | Action |
|---|---|
| `extract ASAR OUT` | Unpack `app.asar` into a directory |
| `apply TREE MAP_JSON` | Apply a map to an extracted tree |
| `pack TREE OUT_ASAR` | Pack a tree into a new ASAR |
| `install TARGET_ASAR NEW_ASAR` | Create `.bak` once and replace the target |
| `restore TARGET_ASAR` | Restore the target from `.bak` |
| `patch ASAR MAP_JSON OUT_ASAR [--work DIR]` | Run extract, apply, and pack |

Without `--work`, `patch` creates a work directory beside the output ASAR.
An existing work directory is recreated, so do not point `--work` at a
directory that contains files you need.

## Map format

```json
{
  "Settings": "Налаштування",
  "Check for updates": "Перевірити оновлення"
}
```

The map must be a JSON object of `string → string`. Empty keys and non-string
pairs are ignored. Longer keys are applied first, but replacement is still an
exact substring operation rather than JavaScript syntax parsing.

During `apply`:

- text files are read as UTF-8;
- files that cannot be read as UTF-8 are skipped;
- fonts, images, media, `.node`, `.dll`, `.exe`, `.wasm`, and other known
  binary suffixes are left untouched;
- the CLI prints the number of changed files and replacements.

## Profiles

`profiles/demo/` contains a minimal example. Add one profile directory per
application, with its own map and short instructions. The patcher itself is not
limited to Ukrainian; map values may contain any strings.

## Backup behavior

`install` creates `app.asar.bak` only when a backup does not already exist.
Later installs preserve that first backup. `restore` copies it back and fails
if the `.bak` file is missing.

## Development check

```bash
python -m asar_ua --help
python -m asar_ua patch --help
```

## License

MIT