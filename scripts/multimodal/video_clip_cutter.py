import csv, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(ROOT, "downloads")
CLIPS_DIR = os.path.join(ROOT, "clips")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)

YTDLP = "yt-dlp"
FFMPEG = "ffmpeg"  # ffmpeg must be on PATH (installed via: winget install Gyan.FFmpeg)


def ffmpeg_on_path():
    """Try to locate ffmpeg.exe (winget installs under %LOCALAPPDATA%)."""
    ffdir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        r"Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
        r"\ffmpeg-8.1.2-full_build\bin",
    )
    candidates = [
        FFMPEG,
        os.path.join(ffdir, "ffmpeg.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""),
                     r"Microsoft\WinGet\Links\ffmpeg.exe"),
    ]
    for c in candidates:
        try:
            subprocess.run([c, "-version"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, check=True)
            return c
        except Exception:
            continue
    return None


def load_annotated_definition():
    path = os.path.join(ROOT, "annotated_videos_definition.csv")
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


def group_by_video(defs):
    by_video = {}
    for r in defs:
        by_video.setdefault(r["youtube_video_id"], []).append(r)
    return by_video


def download_video(video_id):
    """Download one source video. Uses the android client to avoid DRM/429 blocks."""
    out = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
    cmd = [YTDLP,
           "--extractor-args", "youtube:player_client=android",
           "-f", "b",
           "-o", out,
           f"https://www.youtube.com/watch?v={video_id}"]
    print(f"[download] {video_id}")
    subprocess.run(cmd, check=True)
    # locate produced file
    base = os.path.join(DOWNLOAD_DIR, video_id)
    for ext in (".mp4", ".mkv", ".webm", ".m4a"):
        p = base + ext
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"downloaded file not found for {video_id}")


def find_downloaded(video_id):
    base = os.path.join(DOWNLOAD_DIR, video_id)
    for ext in (".mp4", ".mkv", ".webm", ".m4a"):
        p = base + ext
        if os.path.exists(p):
            return p
    return None


def cut_clip(video_file, clip_id, start, end, out_dir=CLIPS_DIR):
    """Cut one clip with accurate seek (0.5s pre-roll) + re-encode."""
    out = os.path.join(out_dir, f"{clip_id}.mp4")
    start = float(start)
    end = float(end)
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
           "-ss", str(max(0.0, start - 0.5)),
           "-i", video_file,
           "-ss", str(start), "-t", str(round(end - start, 3)),
           "-c:v", "libx264", "-c:a", "aac", out]
    subprocess.run(cmd, check=True)
    return out


def main():
    ffmpeg = ffmpeg_on_path()
    if not ffmpeg:
        print("ffmpeg not found. Install with: winget install Gyan.FFmpeg")
        sys.exit(1)
    global FFMPEG
    FFMPEG = ffmpeg

    import argparse
    ap = argparse.ArgumentParser(description="Download source videos and cut annotated clips")
    ap.add_argument("--videos", nargs="*", default=None,
                    help="YouTube video ids to process. Default: all 23 from the annotated definition")
    ap.add_argument("--clips-only", action="store_true",
                    help="Only cut clips (skip downloading if file exists)")
    args = ap.parse_args()

    defs = load_annotated_definition()
    by_video = group_by_video(defs)

    if args.videos:
        video_ids = args.videos
    else:
        video_ids = list(by_video.keys())

    log = {}
    for vid in video_ids:
        video_file = find_downloaded(vid)
        if not video_file:
            if args.clips_only:
                print(f"[skip] {vid} not downloaded (clips-only mode)")
                continue
            video_file = download_video(vid)
        clips = sorted(by_video[vid], key=lambda r: float(r["start_time"]))
        for c in clips:
            try:
                out = cut_clip(video_file, c["clip_id"], c["start_time"], c["end_time"])
                log[c["clip_id"]] = {"video_id": vid, "start": c["start_time"],
                                     "end": c["end_time"], "source": video_file,
                                     "out": out, "status": "ok"}
                print(f"OK   {c['clip_id']}  [{c['start_time']}-{c['end_time']}] <- {vid}")
            except Exception as e:
                log[c["clip_id"]] = {"video_id": vid, "start": c["start_time"],
                                     "end": c["end_time"], "source": video_file,
                                     "out": os.path.join(CLIPS_DIR, f"{c['clip_id']}.mp4"),
                                     "status": f"fail: {e}"}
                print(f"FAIL {c['clip_id']}  [{c['start_time']}-{c['end_time']}] <- {vid}: {e}")

    with open(os.path.join(ROOT, "clip_cut_log.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, indent=1)
    print("\nwrote clip_cut_log.json")


if __name__ == "__main__":
    main()