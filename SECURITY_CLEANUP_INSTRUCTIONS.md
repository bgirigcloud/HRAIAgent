# 🚨 SECURITY CLEANUP - Remove API Keys from Git History

## ⚠️ CRITICAL SECURITY ISSUE DETECTED

**API Keys and credentials found in Git commits:**
- `.env` file with `GOOGLE_API_KEY` exposed
- `HR_root_agent/.env` with API key exposed
- Committed in multiple commits (ca410bd, 7b36641, 41e6718)

---

## 🔴 IMMEDIATE ACTIONS REQUIRED

### Step 1: Revoke All Exposed API Keys

**🚨 DO THIS FIRST - BEFORE CLEANING GIT:**

1. **Revoke Google API Keys:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Project: `zeta-turbine-477404-d9`
   - Find these exposed keys:
     - `AQ.Ab8RN6LvMcYdV8SEOsCOF7-pyUOYWav1aCjmk0s5u4N8r412ZQ`
     - `AIzaSyAvoASqKedyssHVM2A7EfBqkxbKKh37evo`
   - **DELETE/REVOKE** these keys immediately
   - Generate new API keys

2. **Update Cloud Run with New Key:**
   ```bash
   gcloud run services update hraiagent \
     --region us-central1 \
     --update-env-vars "GOOGLE_API_KEY=<NEW_KEY_HERE>"
   ```

3. **Update Dialogflow Credentials:**
   - Check if any Dialogflow keys were exposed
   - Regenerate if necessary

---

## 🧹 Step 2: Remove Sensitive Files from Git History

### Option A: Using BFG Repo-Cleaner (RECOMMENDED - Faster & Safer)

1. **Install BFG:**
   ```powershell
   # Download from: https://rtyley.github.io/bfg-repo-cleaner/
   # Or use Scoop:
   scoop install bfg
   ```

2. **Backup Repository:**
   ```powershell
   cd D:\CloudHeroWithAI\HrMultiAgent
   git clone --mirror https://github.com/bgirigcloud/HRAIAgent.git HRAIAgent-backup.git
   ```

3. **Clean Repository:**
   ```powershell
   cd D:\CloudHeroWithAI\HrMultiAgent\HRAIAgent
   
   # Remove .env files from all commits
   bfg --delete-files .env
   bfg --delete-files '.env.*'
   
   # Remove credentials files
   bfg --delete-files '*credentials*.json'
   bfg --delete-files '*.key'
   bfg --delete-files '*.pem'
   
   # Clean up
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```

4. **Force Push (⚠️ WARNING: Rewrites history):**
   ```powershell
   git push origin --force --all
   git push origin --force --tags
   ```

---

### Option B: Using git filter-repo (More Control)

1. **Install git-filter-repo:**
   ```powershell
   pip install git-filter-repo
   ```

2. **Create paths-to-remove.txt:**
   ```
   .env
   HR_root_agent/.env
   **/.env
   .env.*
   **/.env.*
   credentials.json
   google_credentials.json
   service_account.json
   token.json
   *.key
   *.pem
   *.p12
   ```

3. **Run filter-repo:**
   ```powershell
   cd D:\CloudHeroWithAI\HrMultiAgent\HRAIAgent
   
   # Backup first!
   git clone . ../HRAIAgent-backup
   
   # Remove files from history
   git filter-repo --paths-from-file paths-to-remove.txt --invert-paths
   
   # Force push
   git remote add origin https://github.com/bgirigcloud/HRAIAgent.git
   git push origin --force --all
   ```

---

### Option C: Using git filter-branch (Slower, built-in)

```powershell
cd D:\CloudHeroWithAI\HrMultiAgent\HRAIAgent

# Backup
git clone . ../HRAIAgent-backup

# Remove .env files from all commits
git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch .env HR_root_agent/.env .env.* **/.env" `
  --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
git push origin --force --tags
```

---

## 🛡️ Step 3: Secure Repository Going Forward

### Update .gitignore (Already Done ✅)

Your `.gitignore` already includes:
```gitignore
.env
.env.*
credentials.json
google_credentials.json
service_account.json
token.json
*.key
*.pem
*.p12
```

### Delete Local .env Files (Keep Template Only)

```powershell
# Remove actual .env files
Remove-Item .env -ErrorAction SilentlyContinue
Remove-Item HR_root_agent\.env -ErrorAction SilentlyContinue
Remove-Item .env.* -ErrorAction SilentlyContinue

# Create .env.example template
@"
# Environment Variables Template
# Copy this file to .env and fill in your actual values

# Google API Key for Gemini AI
GOOGLE_API_KEY=your_api_key_here

# Dialogflow Configuration
DIALOGFLOW_PROJECT_ID=your_project_id
DIALOGFLOW_AGENT_ID=your_agent_id

# Cloud Storage (Optional)
GCS_BUCKET_NAME=your_bucket_name
"@ | Out-File -FilePath .env.example -Encoding UTF8
```

---

## 📋 Step 4: Verify Cleanup

### Check Git History is Clean:

```powershell
# Search for API keys in history
git log --all -p -S 'GOOGLE_API_KEY' | Select-String 'GOOGLE_API_KEY'

# Check if .env files still exist in history
git log --all --full-history -- .env

# Verify file sizes reduced
git count-objects -vH
```

### Verify GitHub Repository:

1. Go to: https://github.com/bgirigcloud/HRAIAgent
2. Use GitHub's search: `GOOGLE_API_KEY` or `AIzaSy`
3. Should show "No results"
4. Check old commits - .env files should be gone

---

## 🔒 Step 5: Security Best Practices

### Use Environment Variables in Cloud Run:

```bash
# Set environment variables in Cloud Run (NOT in code)
gcloud run services update hraiagent \
  --region us-central1 \
  --update-env-vars "GOOGLE_API_KEY=<NEW_KEY>,DIALOGFLOW_PROJECT_ID=<PROJECT>"
```

### Use Secret Manager (RECOMMENDED):

```bash
# Create secret
gcloud secrets create google-api-key \
  --replication-policy="automatic" \
  --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:189940306251-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Update Cloud Run to use secret
gcloud run services update hraiagent \
  --region us-central1 \
  --update-secrets="GOOGLE_API_KEY=google-api-key:latest"
```

### Never Commit:
- ❌ .env files
- ❌ credentials.json
- ❌ service_account.json
- ❌ API keys in code
- ❌ Database passwords
- ❌ Private keys (.key, .pem)

### Always Commit:
- ✅ .env.example (template)
- ✅ .gitignore (with sensitive patterns)
- ✅ Documentation
- ✅ Code that reads from environment variables

---

## 📞 Step 6: Notify Team Members

**⚠️ IMPORTANT:** After force-pushing, all team members must:

```powershell
# Backup their local changes first!
git stash

# Delete local repo
cd ..
Remove-Item -Recurse -Force HRAIAgent

# Fresh clone
git clone https://github.com/bgirigcloud/HRAIAgent.git
cd HRAIAgent

# Restore their changes (if any)
git stash pop
```

---

## ✅ Checklist

- [ ] **CRITICAL:** Revoke all exposed API keys in Google Cloud Console
- [ ] **CRITICAL:** Generate new API keys
- [ ] **CRITICAL:** Update Cloud Run with new keys
- [ ] Backup repository locally
- [ ] Choose cleanup method (BFG/filter-repo/filter-branch)
- [ ] Run cleanup commands
- [ ] Verify cleanup completed
- [ ] Force push to GitHub (⚠️ rewrites history)
- [ ] Delete local .env files
- [ ] Create .env.example template
- [ ] Verify GitHub shows no sensitive data
- [ ] Update Cloud Run to use Secret Manager
- [ ] Notify all team members to re-clone
- [ ] Add pre-commit hooks to prevent future commits

---

## 🔍 Verification Commands

```powershell
# Check for API keys in current files
Get-ChildItem -Recurse -File | Select-String "AIzaSy|GOOGLE_API_KEY" | Select-Object Path, LineNumber, Line

# Check Git history for sensitive data
git log --all --source --full-history -p -S "AIzaSy"

# Check repository size (should be smaller after cleanup)
git count-objects -vH
```

---

## 📚 Additional Resources

- **BFG Repo-Cleaner:** https://rtyley.github.io/bfg-repo-cleaner/
- **git-filter-repo:** https://github.com/newren/git-filter-repo
- **GitHub: Removing sensitive data:** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- **Google Cloud Secret Manager:** https://cloud.google.com/secret-manager/docs

---

## ⚠️ WARNING

**Force pushing rewrites Git history and will:**
- Break active pull requests
- Require all team members to re-clone
- Change all commit hashes
- Potentially cause data loss if not backed up

**Always backup before proceeding!**

---

**Created:** November 12, 2025  
**Status:** 🚨 URGENT - Immediate Action Required  
**Priority:** P0 - Critical Security Issue
