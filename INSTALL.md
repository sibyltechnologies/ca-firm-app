# CA Firm Management System — Phase 1
## Installation Guide (ERPNext v16 / Frappe Framework)

---

## ✅ PREREQUISITES

| Requirement        | Version          |
|--------------------|------------------|
| ERPNext            | v16 (develop)    |
| Frappe Framework   | v16              |
| Python             | 3.11+            |
| Node.js            | 18+              |
| MariaDB            | 10.6+            |
| Redis              | 6+               |

---

## 📁 WHAT THIS APP INCLUDES (Phase 1)

### DocTypes (Data Models)
| DocType                    | Purpose                                  |
|----------------------------|------------------------------------------|
| CA Client                  | Client master + lead/CRM data            |
| CA Engagement              | Engagement management + team + fees      |
| CA Staff Profile           | Staff with skills, ICAP no., billing rate|
| CA Timesheet Entry         | Time logging per engagement              |
| CA Invoice                 | Billing and payment tracking             |
| CA Contact Log             | CRM contact/interaction log              |
| CA Engagement Team Member  | Child table for team on engagement       |
| CA Staff Skill             | Child table for staff skills             |

### Reports
| Report                     | Purpose                                  |
|----------------------------|------------------------------------------|
| Engagement Status Report   | All engagements with days-to-deadline   |
| Staff Utilization Report   | Hours logged vs. target per month        |
| Billing Summary Report     | Invoice-level billing and payment status |

### Roles
- **CA Partner** — Full access, submit/cancel rights
- **CA Manager** — Create/edit clients, engagements, invoices
- **CA Senior** — Read/write on engagements and timesheets
- **CA Trainee** — Read-only + log own timesheets
- **CA Admin** — Administrative full access

### Automations
- Daily deadline reminders (email) at 14, 7, 3, 1 days
- Auto-overdue invoice marking (daily)
- Auto-financial-year calculation (Pakistan FY: Jul-Jun)
- Auto-billable amount calculation from hourly rate

---

## 🚀 INSTALLATION STEPS

### Step 1: Place app in your bench apps folder

```bash
cd /path/to/your/bench
```

**Option A — Copy manually:**
```bash
cp -r /path/to/ca_firm_app/ca_firm_management ./apps/ca_firm_management
```

**Option B — If hosted on Git (after you push it):**
```bash
bench get-app https://github.com/YOUR_ORG/ca_firm_management
```

---

### Step 2: Install the app on your site

```bash
bench --site YOUR_SITE_NAME install-app ca_firm_management
```

Replace `YOUR_SITE_NAME` with your actual Frappe site name (e.g., `myfirm.localhost`).

---

### Step 3: Run migrations

```bash
bench --site YOUR_SITE_NAME migrate
```

This creates all the database tables for the DocTypes.

---

### Step 4: Build assets

```bash
bench build --app ca_firm_management
```

---

### Step 5: Restart bench

```bash
bench restart
```

---

### Step 6: Verify installation

1. Login to ERPNext as Administrator
2. Go to: **Settings → Installed Apps**
3. You should see **CA Firm Management** listed
4. Navigate to the module via the main menu

---

## 👤 FIRST-TIME SETUP (Do in this order)

### A. Create Staff Profiles
1. Go to **CA Firm Management → CA Staff Profile → New**
2. Create profiles for all Partners, Managers, Seniors, Trainees
3. Set designation, ICAP membership, hourly rate, monthly target hours
4. Link each profile to their ERPNext User Account → roles will auto-assign

### B. Create Clients
1. Go to **CA Firm Management → CA Client → New**
2. Fill: Client Name, Entity Type, NTN, Industry
3. Assign Partner and Manager
4. Set initial Risk Rating

### C. Create Engagements
1. From the Client form → click **Actions → New Engagement**
2. OR go to **CA Engagement → New**
3. Set Engagement Type, Period, Deadline, Team, Fee
4. Upload Engagement Letter → check "Terms Agreed" → Submit

### D. Log Time
1. Go to **CA Timesheet Entry → New**
2. Select Staff Member, Work Date, Engagement, Activity
3. Enter Hours + Work Description
4. Billable Amount auto-calculates from Staff's hourly rate

### E. Create Invoice
1. From submitted Engagement → click **Actions → Create Invoice**
2. Verify amount + tax (16% auto-applied if marked)
3. Submit invoice

---

## ⚙️ SCHEDULER SETUP

Ensure Frappe scheduler is enabled:

```bash
bench --site YOUR_SITE_NAME set-config scheduler_enabled 1
bench restart
```

Daily reminder emails require your outgoing email configured in:
**Settings → Email Account → Add Outgoing Email**

---

## 🔐 PERMISSION MATRIX (Quick Reference)

| Action               | Partner | Manager | Senior | Trainee | Admin |
|----------------------|---------|---------|--------|---------|-------|
| Create Client        | ✅      | ✅      | ❌     | ❌      | ✅    |
| Edit Client          | ✅      | ✅      | ✅     | ❌      | ✅    |
| Create Engagement    | ✅      | ✅      | ❌     | ❌      | ❌    |
| Submit Engagement    | ✅      | ❌      | ❌     | ❌      | ❌    |
| Log Timesheet        | ✅      | ✅      | ✅     | ✅      | ❌    |
| Create Invoice       | ✅      | ✅      | ❌     | ❌      | ✅    |
| Submit Invoice       | ✅      | ❌      | ❌     | ❌      | ❌    |
| View All Reports     | ✅      | ✅      | ❌     | ❌      | ✅    |

---

## 🛠️ TROUBLESHOOTING

**App not visible in menu:**
```bash
bench --site YOUR_SITE clear-cache
bench restart
```

**Migration error on DocType:**
```bash
bench --site YOUR_SITE migrate --skip-failing
```
Then review the error in `logs/frappe.log`

**Emails not sending:**
- Check Settings → Email Account → outgoing SMTP configured
- Check `bench logs` for email errors

**Permission issues:**
- Ensure Staff Profile is linked to correct User Account
- Run: Desk → Settings → Role Permissions Manager → CA Engagement

---

## 🗺️ WHAT'S COMING IN PHASE 2

Phase 2 will add on top of this foundation:
- **Risk Assessment Engine** (ISA 315) — inherent + control risk scoring
- **Materiality Calculator** (ISA 320) — revenue/asset % based
- **Fraud Risk Checklist**
- **Risk Heatmap Dashboard**
- **Audit Planning Wizard**
- **Work Program Generator**

All Phase 2 DocTypes will link back to the CA Engagement created in Phase 1.

---

## 📞 SUPPORT

For issues during installation, check:
- Frappe Forum: https://discuss.frappe.io
- ERPNext Docs: https://docs.erpnext.com
- Frappe Framework Docs: https://frappeframework.com/docs

---

*CA Firm Management System — Built for Pakistan CA Practice*
*Phase 1 MVP | ERPNext v16 Compatible*
