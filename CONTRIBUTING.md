# Contributing to Nepali NLP Library (`nepalinlplibrary`)

We welcome open-source contributions from computational linguists, machine learning researchers, and open-source developers!

---

## 1. Development Environment Setup

```bash
# 1. Clone your fork
git clone https://github.com/your-username/nepalinlplibrary.git
cd nepalinlplibrary

# 2. Install editable package with dev dependencies
pip install -e ".[dev]"

# 3. Run unit tests
python -m pytest tests/
```

---

## 2. Code & Architecture Guidelines

- **PEP 8 Compliance**: Follow standard Python code style.
- **Type Annotations**: Provide explicit type hints for all public function signatures.
- **Unit Test Coverage**: Every new feature, noising operator, or dataset parser MUST include corresponding unit tests under `tests/`.
- **Zero Hardcoded Paths**: Always use `nepalinlplibrary.config._config` for resolving data registry directories.

---

## 3. Pull Request Checklist

Before submitting your PR:
- [ ] Run `pytest tests/` and ensure **100% of tests pass**.
- [ ] Add docstrings and type hints to all new modules.
- [ ] Update `README.md` if adding a new public API or agent skill.
