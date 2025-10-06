# CV PDF Generation

This repository includes automated CV PDF generation from the JSON data in `_data/cv.json`.

## How it works

1. **Automatic Generation**: When you update `_data/cv.json` and push to GitHub, a GitHub Action automatically generates a new PDF and commits it to the repository.

2. **Manual Generation**: You can also generate the PDF locally by running:
   ```bash
   pip install -r requirements.txt
   python generate_cv_pdf.py
   ```

3. **Manual Workflow Trigger**: You can manually trigger PDF generation from GitHub's Actions tab using the "Manual CV PDF Generation" workflow.

4. **Navigation**: The CV link in the site navigation points directly to `/files/cv.pdf`, which will download or open the PDF file in a new tab.

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

## Troubleshooting

### GitHub Action Issues

1. **Deprecated actions error**: The workflow has been updated to use the latest versions of GitHub actions (v4/v5).

2. **Permission denied**: The workflow includes proper permissions for writing to the repository.

3. **Manual testing**: Use the "Manual CV PDF Generation" workflow to test without changing CV data.

### Testing the Workflow

1. Go to your repository's Actions tab
2. Select "Manual CV PDF Generation" 
3. Click "Run workflow"
4. Check the workflow logs for any errors
5. Verify the PDF was generated and committed

### Local Testing

Before pushing changes, test locally:
```bash
pip install -r requirements.txt
python generate_cv_pdf.py
file files/cv.pdf  # Should show: PDF document, version 1.4
```