# Deployment Guide

## Deploying to Your GitHub Repository

### Step 1: Prepare Your Local Repository

```bash
# Navigate to your local repo
cd /path/to/Site-Data-Development

# Copy all files from this delivery
# Copy: app.py, county_adapters.py, excel_generator.py, municode_parser.py, 
#       requirements.txt, README.md, .gitignore
```

### Step 2: Commit and Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Site Data Development Tool v1.0"

# Push to your repository
git push origin main
```

**Your Repository:** https://github.com/briandahlen-droid/Site-Data-Development

---

## Deploying to Streamlit Cloud (FREE)

### Step 1: Sign Up for Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Authorize Streamlit Cloud to access your repositories

### Step 2: Deploy Your App

1. Click "New app"
2. Select your repository: `briandahlen-droid/Site-Data-Development`
3. Set main file path: `app.py`
4. Click "Deploy!"

### Step 3: Access Your Live App

Your app will be available at:
```
https://briandahlen-droid-site-data-development.streamlit.app
```

(Or similar - Streamlit will provide the exact URL)

### Step 4: Share with Team

Send the URL to your team members. No installation required - they just need a web browser!

---

## Local Development

### Setup

```bash
# Clone your repository
git clone https://github.com/briandahlen-droid/Site-Data-Development.git
cd Site-Data-Development

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

App will open in your browser at: `http://localhost:8501`

### Development Workflow

1. Make changes to code
2. Streamlit auto-reloads on save
3. Test thoroughly
4. Commit and push to GitHub
5. Streamlit Cloud auto-deploys (if configured)

---

## Configuration Options

### Streamlit Cloud Settings

In Streamlit Cloud dashboard, you can configure:
- **Python version**: 3.9+ recommended
- **Secrets**: For API keys (if needed in Phase 2)
- **Resources**: RAM and CPU allocation

### Custom Domain (Optional)

Streamlit Cloud allows custom domains:
1. Go to app settings
2. Add custom domain
3. Update DNS records as instructed

---

## Updating the App

### Method 1: Direct Push (Recommended)

```bash
# Make your changes locally
# Test with: streamlit run app.py

# Commit and push
git add .
git commit -m "Description of changes"
git push origin main

# Streamlit Cloud will auto-deploy within ~1 minute
```

### Method 2: Pull Requests

1. Create a feature branch
2. Make changes
3. Open Pull Request on GitHub
4. Review and merge
5. Streamlit Cloud deploys from main branch

---

## Troubleshooting

### App Won't Start

**Check:**
- All required files are in repository
- requirements.txt is correct
- No syntax errors in Python files

**Solution:**
```bash
# Test locally first
streamlit run app.py

# Check Streamlit Cloud logs for errors
```

### Import Errors

**Problem:** Module not found errors

**Solution:**
- Verify requirements.txt includes all dependencies
- Check Python version compatibility
- Reboot app in Streamlit Cloud dashboard

### API Timeouts

**Problem:** Property lookups timing out

**Solution:**
- Check network connectivity
- Verify county API endpoints are accessible
- Increase timeout in county_adapters.py

---

## Monitoring

### Streamlit Cloud Analytics

View in dashboard:
- Number of users
- Page views
- Resource usage
- Error logs

### User Feedback

Add feedback collection:
1. Add feedback form in app
2. Store in Google Sheets (Phase 2)
3. Monitor GitHub Issues

---

## Security

### Environment Variables

For Phase 2 (API keys, etc.):

1. In Streamlit Cloud dashboard:
   - Go to app settings
   - Click "Secrets"
   - Add as TOML format:
   ```toml
   [api]
   key = "your-api-key-here"
   ```

2. Access in code:
   ```python
   import streamlit as st
   api_key = st.secrets["api"]["key"]
   ```

### Best Practices

- ✅ Never commit API keys or passwords
- ✅ Use .gitignore for sensitive files
- ✅ Keep dependencies updated
- ✅ Monitor for security advisories

---

## Support

**Deployment Issues:**
- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io

**App-Specific Issues:**
- Create GitHub Issue
- Contact Development Team
- Check internal wiki

---

## Quick Reference

| Action | Command/URL |
|--------|------------|
| Run locally | `streamlit run app.py` |
| Your GitHub repo | https://github.com/briandahlen-droid/Site-Data-Development |
| Streamlit Cloud | https://share.streamlit.io |
| Your live app | (URL provided after deployment) |
| View logs | Streamlit Cloud dashboard → Logs |
| Update app | `git push origin main` |

---

**Ready to Deploy?**

1. ✅ Copy files to your repository
2. ✅ Push to GitHub
3. ✅ Deploy on Streamlit Cloud
4. ✅ Share URL with team!
