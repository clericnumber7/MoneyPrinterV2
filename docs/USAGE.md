# MoneyPrinter V2 - Usage Guide

Complete guide for operating MoneyPrinter V2 and all its features.

## Table of Contents

1. [Getting Started](#getting-started)
2. [YouTube Shorts Automation](#youtube-shorts-automation)
3. [Twitter Bot](#twitter-bot)
4. [Affiliate Marketing](#affiliate-marketing)
5. [Outreach](#outreach)
6. [CRON Jobs & Scheduling](#cron-jobs--scheduling)
7. [Best Practices](#best-practices)
8. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### First Run

1. **Launch the application:**
   ```bash
   python src/main.py
   ```

2. **You'll see the main menu:**
   ```
   ============ OPTIONS ============
    1. YouTube Shorts Automation
    2. Twitter Bot
    3. Affiliate Marketing
    4. Outreach
    5. Quit
   =================================
   ```

3. **Select an option** by entering the number (1-5)

### Firefox Profile Setup

**Important:** Before using social media features, you need a Firefox profile:

1. **Open Firefox**
2. **Type in URL bar:** `about:profiles`
3. **Create a new profile:** Click "Create a New Profile"
4. **Name it:** e.g., "MoneyPrinterBot"
5. **Find the profile path:**
   - Windows: `C:\Users\YourName\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxx.MoneyPrinterBot`
   - Linux: `~/.mozilla/firefox/xxxxx.MoneyPrinterBot`
6. **Log into your social accounts** using this profile
7. **Copy the profile path** to use in the application

---

## YouTube Shorts Automation

Automatically generates and uploads YouTube Shorts videos.

### Setup

1. **Select option 1** from main menu
2. **Create an account** (first time):
   ```
   Generated ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   Enter a nickname: My Gaming Channel
   Enter Firefox profile path: /path/to/firefox/profile
   Enter account niche: Gaming
   Enter account language: English
   ```

3. **Choose image generation method:**
   - **Option 1: G4F (SDXL Turbo)** - Free, no setup required (recommended)
   - **Option 2: Cloudflare Worker** - Faster, requires Cloudflare setup

### Generating Videos

Once account is set up:

1. **Select "Upload Short"** (Option 1)
2. **Wait for generation:**
   - Topic generation (~5 seconds)
   - Script writing (~10 seconds)
   - Metadata creation (~5 seconds)
   - Image generation (~2-5 minutes)
   - TTS generation (~10 seconds)
   - Video compilation (~30-60 seconds)
3. **Review the video** (saved in `.mp/` folder)
4. **Upload to YouTube** when prompted

### Video Options

**Option 1: Upload Short**
- Generates new video
- Optionally uploads to YouTube
- Saves metadata to cache

**Option 2: Show all Shorts**
- Lists previously generated videos
- Shows title, date, and upload status

**Option 3: Setup CRON Job**
- Automate video uploads
- Options:
  - Once a day
  - Twice a day (10 AM and 4 PM)

**Option 4: Quit**
- Returns to main menu

### Customization

Edit `config.json` to customize:

```json
{
  "llm": "gpt35_turbo",           // AI model for scripts
  "image_prompt_llm": "gpt35_turbo", // AI for image prompts
  "image_model": "prodia",         // Image generation model
  "threads": 2,                    // Video processing threads
  "is_for_kids": false,            // YouTube kids setting
  "script_sentence_length": 4      // Script length (sentences)
}
```

---

## Twitter Bot

Automates Twitter posting based on your chosen topic.

### Setup

1. **Select option 2** from main menu
2. **Create an account** (first time):
   ```
   Generated ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   Enter a nickname: Tech News Bot
   Enter Firefox profile path: /path/to/firefox/profile
   Enter account topic: Technology and AI
   ```

3. **Important:** Make sure you're logged into Twitter in the Firefox profile

### Posting

**Option 1: Post something**
- Generates AI post about your topic
- Automatically posts to Twitter
- Saves to cache

**Option 2: Show all Posts**
- Lists post history
- Shows date and content

**Option 3: Setup CRON Job**
- Automate posting schedule
- Options:
  - Once a day
  - Twice a day (10 AM and 4 PM)
  - Thrice a day (8 AM, 12 PM, 6 PM)

**Option 4: Quit**
- Returns to main menu

### Tweet Customization

Configure in `config.json`:

```json
{
  "twitter_language": "English",   // Tweet language
  "llm": "gpt35_turbo",            // AI model for tweets
  "headless": false                 // Show/hide browser
}
```

### Tips for Better Tweets

- **Specific topics work best:** "Machine Learning" > "Technology"
- **Niche focus:** "Python Programming" > "Programming"
- **Keep it relevant:** AI learns from your topic to generate engaging content

---

## Affiliate Marketing

Promotes Amazon affiliate products on Twitter.

### Setup

**Prerequisites:**
- Twitter account set up (see Twitter Bot section)
- Amazon affiliate link

### Creating a Campaign

1. **Select option 3** from main menu
2. **Enter affiliate link:**
   ```
   Enter the affiliate link: https://amazon.com/dp/PRODUCT?tag=youraffid-20
   ```
3. **Enter Twitter Account UUID:**
   ```
   Enter the Twitter Account UUID: [from Twitter setup]
   ```

### How It Works

1. **Scrapes product information** from Amazon
2. **Generates compelling pitch** using AI
3. **Posts to Twitter** with affiliate link
4. **Tracks in cache** for monitoring

### Example Workflow

```
You: [Paste Amazon affiliate link]
Bot: Scraping product information...
Bot: Product: "Wireless Gaming Mouse RGB..."
Bot: Generating pitch...
Bot: Generated: "Level up your gaming setup with this incredible wireless mouse! Features RGB lighting, 20000 DPI..."
Bot: Posting to Twitter...
Bot: ✓ Posted successfully!
```

### Best Practices

- Use products relevant to your account's niche
- Don't spam - limit to 1-2 affiliate posts per day
- Mix affiliate content with regular posts
- Monitor engagement and adjust strategy

---

## Outreach

Finds local businesses and sends outreach emails.

### Setup

**Prerequisites:**
- Go programming language installed (see Installation guide)
- SMTP email configuration in `config.json`

### Email Configuration

Edit `config.json`:

```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your.email@gmail.com",
    "password": "your-app-password"
  },
  "google_maps_scraper_niche": "restaurants in New York",
  "scraper_timeout": 300,
  "outreach_message_subject": "I have a question about {{COMPANY_NAME}}",
  "outreach_message_body_file": "outreach_message.html"
}
```

**Gmail App Password:**
1. Go to Google Account settings
2. Security > 2-Step Verification
3. App passwords > Generate
4. Use generated password in config

### Creating Email Template

Create `outreach_message.html`:

```html
<!DOCTYPE html>
<html>
<body>
  <p>Hi {{COMPANY_NAME}} team,</p>

  <p>I noticed your business on Google Maps and wanted to reach out...</p>

  <p>Best regards,<br>
  Your Name</p>
</body>
</html>
```

**Variables:**
- `{{COMPANY_NAME}}` - Replaced with business name

### Running Outreach

1. **Select option 4** from main menu
2. **Process starts automatically:**
   - Downloads Google Maps scraper
   - Builds scraper
   - Scrapes businesses in your niche
   - Extracts email addresses from websites
   - Sends personalized emails
3. **Monitor progress** in console

### Ethical Considerations

⚠️ **Important:**
- Only scrape businesses you have legitimate reason to contact
- Follow anti-spam laws (CAN-SPAM, GDPR)
- Provide opt-out option in emails
- Limit outreach volume
- Ensure emails provide value

---

## CRON Jobs & Scheduling

Automate your content generation and posting.

### How CRON Jobs Work

1. **Set up schedule** through the app menu
2. **Script runs in background**
3. **Executes at specified times**
4. **No manual intervention needed**

### YouTube CRON Options

**Once a day:**
- Uploads 1 video every 24 hours
- Best for maintaining consistent schedule

**Twice a day:**
- Uploads at 10 AM and 4 PM
- Increases channel activity

### Twitter CRON Options

**Once a day:**
- Posts 1 tweet daily
- Consistent presence

**Twice a day:**
- Posts at 10 AM and 4 PM
- Moderate activity

**Thrice a day:**
- Posts at 8 AM, 12 PM, 6 PM
- High activity level

### Important Notes

⚠️ **CRON jobs run continuously** - keep the terminal/app running

**To stop CRON jobs:**
- Press `Ctrl+C` in terminal
- Or close the application

**System Requirements:**
- Computer must stay on
- Internet connection required
- Don't close terminal window

### Alternative: System CRON (Linux/Mac)

For production use, set up system cron:

```bash
# Edit crontab
crontab -e

# Add entry (example: run at 10 AM daily)
0 10 * * * cd /path/to/MoneyPrinterV2 && python src/cron.py youtube account-uuid

# Save and exit
```

---

## Best Practices

### Content Quality

1. **Review before posting:** Check generated content before auto-posting
2. **Set headless: false** initially to monitor browser behavior
3. **Use specific niches:** Better content generation
4. **Monitor performance:** Check analytics regularly

### Account Safety

1. **Use dedicated Firefox profiles** - Don't use personal profile
2. **Don't run 24/7 initially** - Start slow, increase gradually
3. **Humanize behavior:** Add random delays (future feature)
4. **Follow platform guidelines:** Stay within TOS

### System Maintenance

1. **Clear temp files regularly:** Run app's temp file cleanup
2. **Monitor disk space:** Videos can accumulate
3. **Update dependencies:** Keep packages up to date
4. **Backup cache files:** Save `.mp/*.json` files

### Performance Optimization

1. **Adjust threads:** More threads = faster video processing
2. **Choose faster models:** `gpt35_turbo` is faster than `gpt4`
3. **Use G4F images:** Free and works well for most use cases
4. **Limit CRON frequency:** Balance growth vs. resource usage

---

## Tips & Tricks

### YouTube Shorts

**Viral Content Tips:**
- Choose trending niches (e.g., "AI News", "Life Hacks")
- Keep scripts short (4-6 sentences max)
- Use attention-grabbing topics
- Add hashtags in descriptions

**Technical Tips:**
- Set `threads: 4` for faster processing (if you have CPU cores)
- Use `image_model: prodia` for good quality/speed balance
- Enable subtitles with AssemblyAI API key

### Twitter Bot

**Engagement Tips:**
- Post during peak hours (use thrice-daily CRON)
- Use hashtags sparingly (1-2 max)
- Ask questions to boost engagement
- Mix content types (tips, news, questions)

**Technical Tips:**
- Use `twitter_language` to target specific audiences
- Test with `headless: false` to debug issues
- Monitor post performance in analytics

### Troubleshooting

**Video generation fails:**
- Check ImageMagick installation
- Verify font file exists
- Try fewer images (shorter script)

**Browser automation fails:**
- Verify Firefox profile path
- Check if logged into account
- Try `headless: false` to see what's happening

**Posts don't appear:**
- Check internet connection
- Verify account isn't rate-limited
- Look for error messages in verbose mode

---

## Quick Reference

### Main Menu
- `1` - YouTube Shorts
- `2` - Twitter Bot
- `3` - Affiliate Marketing
- `4` - Outreach
- `5` - Quit

### Config Files
- `config.json` - Main configuration
- `.mp/*.json` - Account cache
- `outreach_message.html` - Email template

### Important Paths
- Videos: `.mp/*.mp4`
- Songs: `Songs/*.mp3`
- Cache: `.mp/youtube.json`, `.mp/twitter.json`

---

## Getting Help

**Enable Verbose Logging:**
```json
{
  "verbose": true
}
```

**Check System:**
```bash
python setup.py check
```

**Run Tests:**
```bash
python tests/run_all_tests.py
```

**Community Support:**
- GitHub Issues
- Discord Server
- Documentation Wiki

---

**Happy automating!** 🚀

For more details, see:
- [INSTALLATION.md](INSTALLATION.md) - Setup instructions
- [Configuration.md](Configuration.md) - Detailed config options
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
