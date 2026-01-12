# SEO Audit Workflow - 5 Test Cases

## 🔧 Webhook URL
```
https://n8n.programmx.com/webhook/OnboardingReport


## ✅ TEST 1: BFSS - Complete Input
**Website:** [bfss.co.uk](https://bfss.co.uk/) 
**Purpose:** Full workflow test with all fields
```bash
curl -X POST "https://n8n.programmx.com/webhook/OnboardingReport" -H "Content-Type: application/json" -d "{\"target_url\":\"https://bfss.co.uk/\",\"email\":\"ramzanx0553@gmail.com\",\"location\":\"United Kingdom\",\"report_type\":\"onboarding\"}"


## ✅ TEST 2: ProgrammX - Complete Input
**Website:** [programmx.com](https://programmx.com/) 
**Purpose:** Different industry (tech/software) test
```bash
curl -X POST "https://n8n.programmx.com/webhook/OnboardingReport" -H "Content-Type: application/json" -d "{\"target_url\":\"https://programmx.com/\",\"email\":\"ramzanx0016@gmail.com\",\"location\":\"United States\",\"report_type\":\"onboarding\"}"

## ✅ TEST 3: BFSS - Minimal Input
**Purpose:** Test with only required fields (defaults should apply)
```bash
curl -X POST "https://n8n.programmx.com/webhook/OnboardingReport" -H "Content-Type: application/json" -d "{\"target_url\":\"https://bfss.co.uk/\",\"email\":\"ramzanx0016@gmail.com\"}"

## ✅ TEST 4: ProgrammX - URL with HTTPS
**Purpose:** Test URL cleaning (remove https:// prefix)
```bash
curl -X POST "https://n8n.programmx.com/webhook/OnboardingReport" -H "Content-Type: application/json" -d "{\"target_url\":\"https://programmx.com/\",\"email\":\"ramzanx0553@gmail.com\",\"report_type\":\"onboarding\"}"


## ❌ TEST 5: Missing URL (Should FAIL)
**Purpose:** Test error handling when required field is missing
```bash
curl -X POST "https://n8n.programmx.com/webhook/OnboardingReport" -H "Content-Type: application/json" -d "{\"email\":\"ramzanx0553@gmail.com\",\"report_type\":\"onboarding\"}"