# Curiosity AI Scans (localOCR) CLI Usage Examples

These are common command-line patterns for headless batch processing using `cli.py` within the localOCR workspace.

## 1. Extracting Specific Fields from an Image
**Use Case:** Quick extraction from a single image using the default DeepSeek-OCR model.
```bash
python cli.py \
  --model deepseek-ocr:latest \
  --mode extract \
  --fields "Invoice number, Date, Total amount" \
  samples/receipt.png
```

## 2. Processing a PDF with Hybrid Docling + Ollama
**Use Case:** Multi-page PDF extraction using Docling for text layout and Gemma 3 for data extraction.
```bash
python cli.py \
  --model gemma3:12b \
  --mode extract \
  --fields "Customer Name, Address, Total" \
  --ocr-backend hybrid \
  --pdf-pages \
  --pdf-scale 1.5 \
  samples/invoice.pdf
```

## 3. General Image Description
**Use Case:** Open-ended image analysis without structured data requirements.
```bash
python cli.py \
  --model llama3.2-vision \
  --mode description \
  samples/photo.jpg
```

## 4. Full Pipeline with Profiles, Preprocessing, and Exports
**Use Case:** Production-like batch processing with detailed CSV/JSON exports.
```bash
python cli.py \
  --model deepseek-ocr:latest \
  --mode extract \
  --fields "Date, Total" \
  --ocr-backend auto \
  --profile receipt \
  --preprocess high-accuracy-scan \
  --out-results results.csv \
  --out-structured structured.csv \
  --out-evidence evidence.json \
  samples/receipt.png
```
