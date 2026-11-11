# ONCOAI Android starter

This is the first mobile-friendly ONCOAI app prototype.

## Files
- `app.py`: Streamlit app with live NCBI human-gene lookup.
- `requirements.txt`: Python dependencies.

## Run locally
1. Install Python on a computer.
2. Open a terminal in this folder.
3. Run: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`

## Publish for personal Android access
A simple route is to deploy this project using Streamlit Community Cloud:
1. Create a private GitHub repository named `oncoai`.
2. Upload `app.py` and `requirements.txt`.
3. In Streamlit Community Cloud, deploy the repository and select `app.py`.
4. Open the deployed app URL in Chrome on your Android phone.
5. Use Chrome menu (three dots) -> Add to Home screen. The exact wording may vary.

This creates a home-screen app shortcut to the hosted app. It is not yet a standalone APK and needs internet access. A native APK can be a later stage.

## Important
- Do not enter patient-identifying information.
- This is an educational research prototype, not a medical diagnostic or treatment tool.
- NCBI results may include multiple records; this starter displays the first matching human gene record.
