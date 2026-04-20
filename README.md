# Simple ELT Framework

This project includes a beginner-friendly Python ELT framework using Excel as the source and target.

## Structure

- `config/`
- `metadata/`
- `src/`
  - `connectors/`
  - `transformations/`
  - `validations/`
- `tests/`
- `utils/`
- `data/`
- `output/`
- `logs/`
- `reports/`
- `main.py`

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the ELT process

```bash
python main.py
```

## Run tests with HTML report

```bash
pytest --html=reports/report.html
```
