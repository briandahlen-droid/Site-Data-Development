# 🚀 Quick Start - GitHub Deployment

## Step 1: Copy Files to Your Repository

Copy these **8 files** to your repository:
```
📁 Site-Data-Development/
├── app.py                    ⭐ REQUIRED
├── county_adapters.py        ⭐ REQUIRED
├── excel_generator.py        ⭐ REQUIRED
├── municode_parser.py        ⭐ REQUIRED
├── requirements.txt          ⭐ REQUIRED
├── README.md                 (Documentation)
├── .gitignore                (Git config)
└── verify_setup.py           (Optional test script)
```

## Step 2: Verify Setup (Optional)

```bash
# Navigate to your repository
cd Site-Data-Development

# Run verification script
python verify_setup.py
```

## Step 3: Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Add Site Data Development Tool v1.0"

# Push to your repo
git push origin main
```

**Your Repository:**  
https://github.com/briandahlen-droid/Site-Data-Development

---

## Step 4: Deploy to Streamlit Cloud (FREE)

### A. Sign Up
1. Go to: **https://share.streamlit.io**
2. Click "Sign in with GitHub"
3. Authorize Streamlit Cloud

### B. Deploy App
1. Click **"New app"**
2. Repository: `briandahlen-droid/Site-Data-Development`
3. Branch: `main`
4. Main file path: `app.py`
5. Click **"Deploy!"**

### C. Wait (~2 minutes)
Streamlit will:
- Install dependencies from `requirements.txt`
- Start your app
- Provide a public URL

### D. Access Your App
Your live app URL will be:
```
https://briandahlen-droid-site-data-development.streamlit.app
```
(Or similar - Streamlit provides exact URL)

---

## Step 5: Test Your App

### Test Parcels

**Hillsborough County:**
- Try: `192605-0000` or similar folio numbers

**Pinellas County:**
- Try format: `XX-XX-XX-XXXXX-XXX-XXXX`
- (Contact property appraiser for test parcel)

**Manatee County:**
- Try: 10-digit format `XXXXXXXXXX`
- (Contact property appraiser for test parcel)

### What to Test:
1. ✅ Parcel lookup returns data
2. ✅ Property details display correctly
3. ✅ Add to favorites works
4. ✅ Generate Excel report downloads
5. ✅ All tabs load properly

---

## Troubleshooting

### ❌ "ModuleNotFoundError"

**Problem:** Missing Python files

**Solution:**
```bash
# Verify all files are uploaded
ls -la

# Should see:
# app.py
# county_adapters.py
# excel_generator.py
# municode_parser.py
# requirements.txt
```

### ❌ "Import Error"

**Problem:** Files not in same directory

**Solution:**
- All `.py` files must be in root directory
- No subdirectories for Python files
- Check file paths in GitHub

### ❌ App Won't Start

**Problem:** Dependency issues

**Solution:**
1. Check `requirements.txt` is present
2. Verify Python version (3.9+ required)
3. Check Streamlit Cloud logs for details

### ❌ Parcel Not Found

**Problem:** Invalid parcel ID format

**Solution:**
- Verify county selection
- Check parcel ID format for that county
- Try removing dashes
- Try with dashes

---

## Support

**Deployment Issues:**
- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io

**App Issues:**
- Create GitHub Issue in your repository
- Contact Development Team

---

## Quick Commands Reference

```bash
# Local testing
pip install -r requirements.txt
streamlit run app.py

# Git commands
git add .
git commit -m "Your message"
git push origin main

# View app logs (Streamlit Cloud)
# Go to: App → Settings → Logs
```

---

## What's Next?

After successful deployment:

1. **Share with Team**
   - Send them the Streamlit URL
   - No installation needed!

2. **Gather Feedback**
   - What features are most useful?
   - What's missing?
   - Any bugs?

3. **Phase 2 Development**
   - Add Pasco & Sarasota counties
   - Municode zoning parsing
   - Property comparison
   - Batch processing

---

**Need Help?**

Contact: Brian Dahlen  
Team: Development Services  
Repository: https://github.com/briandahlen-droid/Site-Data-Development

---

✅ **Ready? Let's deploy!**

1. Copy files → Your GitHub repo
2. Push to GitHub
3. Deploy on Streamlit Cloud
4. Share URL with team!
