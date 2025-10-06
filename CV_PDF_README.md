# CV PDF Generation

This repository includes automated CV PDF generation from the JSON data in `_data/cv.json`.

## How it works

1. **Automatic Generation**: When you update `_data/cv.json` and push to GitHub, a GitHub Action automatically generates a new PDF and commits it to the repository.

2. **Manual Generation**: You can also generate the PDF locally by running:
   ```bash
   pip install -r requirements.txt
   python generate_cv_pdf.py
   ```

3. **Navigation**: The CV link in the site navigation points directly to `/files/cv.pdf`, which will download or open the PDF file in a new tab.

## Files

- `generate_cv_pdf.py` - Python script that converts CV JSON data to PDF
- `.github/workflows/generate-cv-pdf.yml` - GitHub Action workflow for automatic PDF generation
- `requirements.txt` - Python dependencies
- `files/cv.pdf` - Generated CV PDF file

## Customization

The PDF layout and styling can be customized by editing the `create_styles()` and `generate_pdf()` functions in `generate_cv_pdf.py`.

## Dependencies

- `reportlab` - For PDF generation

The GitHub Action automatically installs dependencies, but for local development you'll need to install them manually.