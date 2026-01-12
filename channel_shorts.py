from fastapi import FastAPI, Query
from googleapiclient.discovery import build
import json
import re

app = FastAPI(title="YouTube Channel Shorts API")

# Replace with your own API Key
API_KEY = "AIzaSyAxoDCbFvZkzF7LXtXPkI3ZHOLULI2g0vk"
youtube = build("youtube", "v3", developerKey=API_KEY)


# -------------------------------
# Helper: Get Channel Details
# -------------------------------
def get_channel_details(channel_name: str):
    search = youtube.search().list(
        q=channel_name,
        part="snippet",
        type="channel",
        maxResults=1
    ).execute()

    if not search["items"]:
        raise Exception("Channel not found")

    item = search["items"][0]
    return {
        "channel_id": item["snippet"]["channelId"],
        "channel_name": item["snippet"]["title"],
        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
    }


# -------------------------------
# Helper: Get Thumbnail URL
# -------------------------------
def get_thumbnail_url(thumbnails: dict) -> str:
    """Get the best available thumbnail URL"""
    if not thumbnails:
        return ""
    # Try high, then medium, then default
    for quality in ["high", "medium", "default"]:
        if quality in thumbnails and "url" in thumbnails[quality]:
            return thumbnails[quality]["url"]
    return ""


# -------------------------------
# Helper: Get All Shorts Videos
# -------------------------------
def get_shorts(channel_id: str):
    shorts = []
    video_ids = []
    
    # First get uploads playlist
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=50
    )

    while request:
        resp = request.execute()
        for item in resp.get("items", []):
            s = item["snippet"]
            vid_id = s["resourceId"]["videoId"]
            video_ids.append(vid_id)
            shorts.append({
                "video_title": s.get("title", ""),
                "video_id": vid_id,
                "video_url": f"https://www.youtube.com/watch?v={vid_id}",
                "video_thumbnail": get_thumbnail_url(s.get("thumbnails", {}))
            })
        request = youtube.playlistItems().list_next(request, resp)

    # Get video durations in batches
    def parse_duration(duration_str):
        """Parse ISO 8601 duration to seconds"""
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds

    # Fetch durations in batches of 50 (API limit)
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        video_details = youtube.videos().list(
            part="contentDetails",
            id=",".join(batch_ids)
        ).execute()

        duration_map = {}
        for detail in video_details.get("items", []):
            vid_id = detail["id"]
            duration_iso = detail["contentDetails"]["duration"]
            duration_seconds = parse_duration(duration_iso)
            duration_map[vid_id] = duration_seconds

        # Update shorts with duration info
        for video in shorts[i:i+50]:
            vid_id = video["video_id"]
            if vid_id in duration_map:
                duration_seconds = duration_map[vid_id]
                video["duration_seconds"] = duration_seconds
                video["is_short"] = True
            else:
                video["duration_seconds"] = 0
                video["is_short"] = False
    
    # Filter to only keep shorts (≤ 60 seconds and > 0)
    shorts_filtered = [video for video in shorts if 0 < video.get("duration_seconds", 0) <= 60]

    return shorts_filtered


# -------------------------------
# Endpoint: Get Channel Shorts
# -------------------------------
@app.get("/channel_shorts")
def channel_shorts(channel_name: str = Query(..., description="YouTube Channel Name")):
    channel = get_channel_details(channel_name)
    shorts_list = get_shorts(channel["channel_id"])

    output = {
        "channel_name": channel["channel_name"],
        "channel_thumbnail": channel["thumbnail"],
        "shorts": shorts_list
    }

    filename = f"{channel_name.replace(' ','_').lower()}_shorts.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    return output


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

