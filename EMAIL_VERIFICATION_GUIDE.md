# Email Verification Guide

## Overview
This guide explains how to verify user email addresses in the Videoflix project using the enhanced dual email verification system.

## Prerequisites
- Docker and Docker Compose installed
- Videoflix project running in containers
- Access to the project terminal

## Two Verification Methods

### Method 1: Terminal-Based Verification (Recommended for Development)
This method allows developers to verify users directly through the command line.

### Method 2: Web-Based Verification (Standard User Flow)
This method follows the standard web application flow where users click verification links.

---

## Method 1: Terminal-Based Verification

### Step 1: Check Active Verification Tokens
First, see which users need verification:

```bash
docker-compose exec web python manage.py verify_email --list-tokens
```

**Example Output:**
```
📧 ACTIVE VERIFICATION TOKENS
============================================================
Email: user@example.com
Token: IdW-NiVYRfXeiEFMkWPmCEoes607hxY_Oqvio5wgY2o
Status: ❌ PENDING
Expires: (VALID)
Created: 2025-07-17 08:57:33
Verification URL: http://localhost:5173/verify-email/IdW-NiVYRfXeiEFMkWPmCEoes607hxY_Oqvio5wgY2o
------------------------------------------------------------
```

### Step 2A: Verify by Email Address
To verify a user using their email address:

```bash
docker-compose exec web python manage.py verify_email --verify "user@example.com"
```

**Success Output:**
```
✅ Successfully verified user: user@example.com
📧 Verification tokens removed.
```

### Step 2B: Verify by Token
Alternatively, verify using the verification token:

```bash
docker-compose exec web python manage.py verify_email --verify-token "IdW-NiVYRfXeiEFMkWPmCEoes607hxY_Oqvio5wgY2o"
```

**Success Output:**
```
✅ Successfully verified user: user@example.com
📧 Verification token removed.
```

### Step 3: Confirm Verification
Check that the user is now verified:

```bash
docker-compose exec web python manage.py verify_email --list-tokens
```

The user should now show `Status: ✅ VERIFIED`.

---

## Method 2: Web-Based Verification

### Step 1: Check Email Files
View the verification emails that were sent:

```bash
docker-compose exec web python manage.py verify_email --list-emails
```

**Example Output:**
```
📧 EMAIL FILES
==================================================
Directory: /app/logs/emails
 1. 20250717-085547-123156467582928.log
     Size: 392 bytes
     Modified: 2025-07-17 08:55:47
💡 Use --show-email FILENAME to view email content
```

### Step 2: View Email Content
To see the verification email that was sent:

```bash
docker-compose exec web python manage.py verify_email --show-email "20250717-085547-123156467582928.log"
```

**Example Output:**
```
📧 EMAIL CONTENT: 20250717-085547-123156467582928.log
============================================================
Subject: Verify Your Email Address
From: noreply@videoflix.com
To: user@example.com
Date: Thu, 17 Jul 2025 08:55:47 -0000

Please click the following link to verify your email address:
http://localhost:5173/verify-email/IdW-NiVYRfXeiEFMkWPmCEoes607hxY_Oqvio5wgY2o
============================================================
```

### Step 3: Use Verification URL
Copy the verification URL from the email and:
1. Open it in a browser, OR
2. Test it with the frontend application

---

## Common Commands Reference

### List all verification tokens
```bash
docker-compose exec web python manage.py verify_email --list-tokens
```

### Verify user by email
```bash
docker-compose exec web python manage.py verify_email --verify "user@example.com"
```

### Verify user by token
```bash
docker-compose exec web python manage.py verify_email --verify-token "TOKEN_STRING"
```

### List all email files
```bash
docker-compose exec web python manage.py verify_email --list-emails
```

### Show email content
```bash
docker-compose exec web python manage.py verify_email --show-email "FILENAME.log"
```

### Clean up expired tokens and old emails
```bash
docker-compose exec web python manage.py verify_email --cleanup
```

### Get help for all options
```bash
docker-compose exec web python manage.py verify_email --help
```

---

## Understanding the Output

### Token Status Colors
- 🟢 **Green (✅ VERIFIED)**: User has been verified
- 🔴 **Red (❌ PENDING)**: User needs verification
- 🟡 **Yellow (EXPIRED)**: Token has expired (24 hours)

### Token Information
- **Email**: User's email address
- **Token**: Unique verification token
- **Status**: Current verification status
- **Expires**: Whether token is still valid
- **Created**: When the token was generated
- **Verification URL**: Direct link for web verification

---

## Troubleshooting

### User Not Found
**Error**: `User with email 'user@example.com' not found`
**Solution**: Check if the email address is correct and the user exists in the system

### Token Not Found
**Error**: `Token 'TOKEN_STRING' not found`
**Solution**: The token may have expired or been used. Check active tokens with `--list-tokens`

### Already Verified
**Info**: `User user@example.com is already verified`
**Action**: No action needed, user is already verified

### No Email Files
**Info**: `No email files found in: /app/logs/emails`
**Action**: No emails have been sent yet, or cleanup has been performed

---

## Best Practices

### For Development
1. Use terminal-based verification for quick testing
2. Check email files to ensure correct content
3. Run cleanup regularly to remove old data

### For Production
1. Rely on web-based verification
2. Monitor email delivery
3. Set up automated cleanup for expired tokens

### Security Notes
- Tokens expire after 24 hours
- Each token can only be used once
- Verified users cannot be re-verified with the same token

---

## Complete Verification Workflow Example

```bash
# 1. Check which users need verification
docker-compose exec web python manage.py verify_email --list-tokens

# 2. View the verification email that was sent
docker-compose exec web python manage.py verify_email --list-emails
docker-compose exec web python manage.py verify_email --show-email "FILENAME.log"

# 3. Verify the user (choose one method)
docker-compose exec web python manage.py verify_email --verify "user@example.com"
# OR
docker-compose exec web python manage.py verify_email --verify-token "TOKEN_STRING"

# 4. Confirm verification was successful
docker-compose exec web python manage.py verify_email --list-tokens

# 5. Clean up (optional)
docker-compose exec web python manage.py verify_email --cleanup
```

This dual verification system provides maximum flexibility for both development and production environments!
