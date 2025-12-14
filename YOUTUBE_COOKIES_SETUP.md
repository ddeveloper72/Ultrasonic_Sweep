# YouTube Cookies Setup for Heroku

YouTube requires authentication to bypass bot detection. Here's how to set up cookies for your Heroku deployment.

## Option 1: Set Cookies via Heroku CLI (Recommended)

### Step 1: Export Your YouTube Cookies

1. Install browser extension:
   - **Chrome/Edge**: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - **Firefox**: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Go to [YouTube.com](https://www.youtube.com) (make sure you're logged in)

3. Click the extension icon and export cookies to `cookies.txt`

### Step 2: Set Environment Variable on Heroku

**Windows (PowerShell):**
```powershell
$cookies = Get-Content -Raw cookies.txt
heroku config:set YOUTUBE_COOKIES="$cookies" -a ultrasonic-sweep
```

**Windows (Command Prompt):**
```cmd
heroku config:set YOUTUBE_COOKIES=@cookies.txt -a ultrasonic-sweep
```

**Mac/Linux:**
```bash
heroku config:set YOUTUBE_COOKIES="$(cat cookies.txt)" -a ultrasonic-sweep
```

### Step 3: Restart Your App
```bash
heroku restart -a ultrasonic-sweep
```

## Option 2: Set Cookies via Heroku Dashboard

1. Export cookies as described in Step 1 above

2. Go to your Heroku app dashboard:
   - https://dashboard.heroku.com/apps/ultrasonic-sweep

3. Click **Settings** tab

4. Click **Reveal Config Vars**

5. Add new config var:
   - **KEY**: `YOUTUBE_COOKIES`
   - **VALUE**: Paste the entire contents of your `cookies.txt` file

6. Click **Add** - the app will automatically restart

## Option 3: Local Upload (Local Development Only)

For local development, you can upload cookies directly through the web interface:

1. Export cookies to `cookies.txt`
2. In the app, find the "YouTube URL" section
3. Click "Upload YouTube Cookies"
4. Select your `cookies.txt` file

**Note**: This only works locally - Heroku users cannot upload files through the web interface.

## Troubleshooting

### Cookies Not Working
- Make sure you're logged into YouTube when exporting cookies
- Cookies expire - you may need to re-export every few weeks
- Check Heroku logs: `heroku logs --tail -a ultrasonic-sweep`

### Error: "Invalid cookies file"
- Ensure the file contains YouTube cookies (should have `youtube.com` in it)
- Use the browser extension method - manual export is error-prone

### How to Check if Cookies Are Active
- Check Heroku config: `heroku config:get YOUTUBE_COOKIES -a ultrasonic-sweep`
- Look for "Using cookies from YOUTUBE_COOKIES environment variable" in logs

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `cookies.txt` to git (it's in `.gitignore`)
- Never share your cookies - they contain your login session
- Cookies give access to your YouTube account
- Only set cookies on your own Heroku app

## Alternative: Disable YouTube Download

If you don't want to deal with cookies, you can:
1. Use the "Upload File" option instead
2. Download YouTube audio locally, then upload it
3. Use a different audio source
