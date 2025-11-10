# 📚 HR Policy Assistant - User Guide

## Overview
The HR Policy Assistant is an intelligent chatbot that helps employees get instant answers to their policy questions by searching through uploaded company policy documents.

## 🎯 Features

### For HR Administrators:
- **Upload Policy Documents** (PDF, DOCX, TXT)
- **Organize by Category** (Leave, Benefits, Code of Conduct, etc.)
- **Manage Documents** (View, Update, Delete)
- **Track Uploads** with metadata

### For Employees:
- **Ask Questions** in natural language
- **Get AI-Powered Answers** based on actual policy documents
- **See Referenced Policies** with each answer
- **Browse All Policies** by category

## 📖 How to Use

### 1️⃣ For HR: Upload Policy Documents

1. Navigate to **"HR Policy Assistant"** in the sidebar
2. Go to **"📤 Upload Policy (HR)"** tab
3. Enter policy details:
   - **Policy Name**: e.g., "Leave Policy 2025"
   - **Category**: Select from dropdown (Leave Policy, Benefits, etc.)
4. **Upload Document**: Click "Browse files" and select your policy document
5. Review the extracted text preview
6. Click **"📥 Upload Policy to System"**
7. ✅ Policy is now searchable by employees!

### 2️⃣ For Employees: Ask Policy Questions

1. Navigate to **"HR Policy Assistant"** in the sidebar
2. Go to **"💬 Ask Policy Question (Employee)"** tab
3. Type your question in the text area:
   - "How many sick leaves am I entitled to per year?"
   - "What is the work from home policy?"
   - "When do I get my annual bonus?"
4. Click **"🔍 Get Answer"**
5. Get an AI-generated answer with:
   - Direct answer to your question
   - Referenced policy documents
   - Relevant details (numbers, procedures, eligibility)

### 3️⃣ View All Policies

1. Go to **"📚 View All Policies"** tab
2. Browse policies organized by category
3. Expand any policy to read full content
4. HR can delete outdated policies

## 💡 Example Questions Employees Can Ask

**Leave Policy:**
- "How many vacation days do I get?"
- "What is the process to apply for sick leave?"
- "Can I carry forward unused leave?"

**Benefits:**
- "What health insurance benefits are available?"
- "Am I eligible for the gym membership reimbursement?"
- "What is the parental leave policy?"

**Remote Work:**
- "How many days can I work from home?"
- "What are the requirements for remote work equipment?"
- "Do I need manager approval for WFH?"

**Code of Conduct:**
- "What is the dress code policy?"
- "What are the working hours?"
- "What is the social media usage policy?"

## 🔧 Technical Details

### Agent Architecture:
- **Agent Name**: `hr_policy_agent`
- **Model**: Gemini 2.0 Flash
- **Tools**: Policy document storage, search, and retrieval
- **Integration**: Part of HR Root Agent system

### Document Storage:
- **Format Support**: PDF, DOCX, TXT
- **Storage**: Session-based (in-memory for demo)
- **Production**: Can be integrated with database (MongoDB, PostgreSQL, etc.)

### AI Capabilities:
- **Natural Language Understanding**: Understands employee questions
- **Semantic Search**: Finds relevant policy sections
- **Contextual Answers**: Generates clear, specific answers
- **Source Citation**: Always references policy documents

## 📊 Policy Categories

Available categories for organizing policies:
1. **Leave Policy** - Vacation, sick leave, personal days
2. **Benefits** - Health insurance, retirement, perks
3. **Code of Conduct** - Workplace behavior, ethics
4. **Remote Work** - WFH policies, equipment, guidelines
5. **Attendance** - Working hours, punctuality, time tracking
6. **Compensation** - Salary, bonuses, raises
7. **Performance Management** - Reviews, goals, feedback
8. **Health & Safety** - Workplace safety, emergency procedures
9. **Training & Development** - Learning opportunities, career growth
10. **General** - Miscellaneous policies

## 🚀 Getting Started

### Step 1: Upload Sample Policies
HR should start by uploading key policy documents:
- Leave Policy
- Benefits Overview
- Code of Conduct
- Remote Work Guidelines

### Step 2: Test with Sample Questions
Try asking common questions to ensure the agent provides accurate answers.

### Step 3: Train Employees
Show employees how to:
- Access the HR Policy Assistant
- Ask questions effectively
- Interpret the AI responses

### Step 4: Monitor and Update
- Regularly update policy documents
- Add new policies as they're created
- Remove outdated policies

## 🔐 Best Practices

### For HR:
- ✅ Keep policy documents up-to-date
- ✅ Use clear, structured policy formatting
- ✅ Organize policies by relevant categories
- ✅ Review AI responses periodically for accuracy
- ✅ Encourage employees to contact HR for sensitive matters

### For Employees:
- ✅ Ask specific, clear questions
- ✅ Check the referenced policy document
- ✅ Contact HR directly for personalized situations
- ✅ Don't share confidential information in questions

## 🛡️ Privacy & Security

- Policy documents are stored securely
- Employee queries are processed confidentially
- Sensitive matters should still be handled directly with HR
- No personal employee data is stored in queries

## 📞 Support

If you have questions or issues:
1. Check the referenced policy documents
2. Try rephrasing your question
3. Contact HR department directly
4. Report technical issues to IT support

## 🎓 Training Resources

### For HR Administrators:
- Policy document formatting guidelines
- Effective category organization
- Troubleshooting upload issues

### For Employees:
- How to ask effective questions
- Understanding AI responses
- When to contact HR directly

---

**Version**: 1.0  
**Last Updated**: November 10, 2025  
**Powered by**: Google Gemini AI & Agent Development Kit
