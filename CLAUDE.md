# CLAUDE.md

## Project

**receitanet-bx** — Windows desktop RPA bot that downloads SPED fiscal documents (Fiscal, Contribuições, Contábil, ECF) from the Receita Federal's **Receitanet BX** desktop application. Uses OpenCV template matching against PNG reference images to drive the GUI, combined with PyAutoGUI and PyWinAuto for keyboard/mouse control.

**Windows-only.** Requires Python 3.8+, Receitanet BX 1.9.24, a valid A1 digital certificate, and a 1920×1080 display (template images are resolution-specific).

## Structure

```
src/
├── base/
│   ├── bot.py      # BaseBot abstract class
│   └── state.py    # Singleton state (shared across modules)
├── core/
│   ├── bot.py      # DesktopBot — keyboard/mouse automation engine
│   ├── cv2find.py  # OpenCV template matching (find UI elements by PNG)
│   └── application/ # PyWinAuto window handle management
├── modules/
│   ├── common.py   # Decorators: @time_execution, @attempts (retry)
│   ├── convert.py  # Date conversion helpers
│   ├── data.py     # Date formatting
│   ├── exceptions.py # Custom exception hierarchy
│   ├── file.py     # File I/O
│   ├── log.py      # Daily log rotation (logs/DD-MM-AAAA.log)
│   ├── types.py    # SpedType enum
│   └── validate.py # CNPJ, date, field validation
└── images/         # ~100 PNG templates for UI element detection
    ├── login/
    ├── baixa/
    ├── combobox-sistemas/
    ├── combobox-arquivos/
    ├── combobox-periodos/
    ├── sped-fiscal/
    └── pop-ups/
receitanet.py       # ReceitaNetBx — UI interaction sequences
sped.py             # SPED orchestration (which type/period to download)
main.py             # Entry point — reads JSON from stdin
```

## Commands

```bash
python main.py      # Reads JSON config from stdin
pytest              # Run unit tests
```

Input is a JSON payload piped to stdin. Set `DEVELOP_MODE=true` for dry-run testing without actually clicking the UI.

## Conventions

- **Inheritance chain:** `BaseBot → DesktopBot → ReceitaNetBx / Sped`. Add new UI sequences to `ReceitaNetBx`, new orchestration to `Sped`.
- **Template matching:** all UI element detection goes through `cv2find.py`. Never hardcode pixel coordinates — always use a PNG template in `src/images/`. Templates are captured at 1920×1080; if the screen resolution changes, retake them.
- **Retry logic:** wrap fragile UI steps with the `@attempts(n)` decorator from `common.py`.
- **SpedType enum** (`modules/types.py`) is the canonical list of supported SPED types — add new types there before implementing them.
- **Exceptions:** raise from `modules/exceptions.py` hierarchy. Never raise bare `Exception`.
- **Logs:** `modules/log.py` writes to `logs/DD-MM-AAAA.log`. Do not use `print()`.
- **State:** shared mutable state goes through `src/base/state.py` singleton — do not use module-level globals elsewhere.
- **Tests** in `tests/` cover `validate`, `data`, and `convert` modules. Run `pytest` before any change to those modules.

## Environment

| Variable | Purpose |
|---|---|
| `DEVELOP_MODE` | `true` = dry-run (no real clicks) |
| OneDrive sync path | Configured inside the JSON input payload |

No `.env` file — parameters are injected via stdin JSON or environment variables set by the Airflow task.
