## yt-clipper – YouTube Highlight Clipper

CLI tool that searches YouTube from a prompt, downloads source videos, finds highlight-relevant segments using ASR + scene detection + semantic similarity, trims them into clips, and emits a JSON manifest.

### Usage

```bash
uv run yt-clipper --prompt "Caitlin Clark buzzer beater" --max-clips 6
```

Or:

```bash
python -m yt_clipper.cli --prompt "Caitlin Clark buzzer beater" --max-clips 6
```

Outputs under `outputs/<slug>/clips/*.mp4` and `outputs/<slug>/manifest.json`.

### YouTube Authentication

YouTube may require authentication to download videos. You have two options to provide cookies:

**Option 1: Cookies file**
```bash
uv run yt-clipper --prompt "your prompt" --cookies /path/to/cookies.txt
```

**Option 2: Browser cookies**
```bash
uv run yt-clipper --prompt "your prompt" --cookies-from-browser chrome
```

**Security Requirements:**
- On macOS, when using `--cookies-from-browser`, you may be prompted to grant Python terminal access to your keychain to read browser cookies. This is safe and required for the browser cookie extraction to work.
- If you deny access, the download will fail. You can grant access in System Preferences > Privacy & Security > Full Disk Access (or wherever the prompt directs you).

**Getting a cookies file:**
- Export cookies using a browser extension (e.g., "Get cookies.txt" for Chrome)
- Or use yt-dlp's instructions: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies

### Disclaimer

Ensure you have rights to download, trim, and use any content. Respect YouTube Terms of Service and any applicable copyright laws.



### License

MIT © 2025 Dylan Powers. See `LICENSE` for details.
