[Українська](README.md) · **English**

# asar-ua

Generic Electron `app.asar` locale pipeline: extract → apply JSON string map →
pack → install with `.bak` / restore.

Full Antigravity pack stays in [antigravity-ua](https://github.com/RiasJ1Dar/antigravity-ua);
this repo is the reusable tool.

ASAR integrity blocks stay **SHA-256** (Electron). Content hashing in
[ota-sign](https://github.com/RiasJ1Dar/ota-sign) is SHA-512 — different layer.

```bash
pip install -e .
asar-ua patch app.asar profiles/demo/locale.uk.json app_uk.asar
```

## License

MIT
