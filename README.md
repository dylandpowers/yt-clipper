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

### Disclaimer

Ensure you have rights to download, trim, and use any content. Respect YouTube Terms of Service and any applicable copyright laws.



### License

MIT © 2025 Dylan Powers. See `LICENSE` for details.
