#!/bin/bash

input_url="https://www.youtube.com/@ThinkingAccordingToAlanWatts"  # Can be channel, playlist, video URL, or local file path
cookies_file="../data/cookies.txt"
DOWNLOAD_MEDIA=0  # Set to 1 to download video/audio files alongside subtitles

# Check if input is local file
if [ -f "$input_url" ]; then
    video_ids=$(basename "$input_url" | sed 's/\.[^.]*$//')  # Use filename without extension as ID
else
    # Get video IDs from URL
    video_ids=$(yt-dlp --cookies "$cookies_file" --flat-playlist --print "%(id)s" "$input_url")
    num_videos=$(echo "$video_ids" | wc -l)
    echo "Total videos in channel: $num_videos"
    subscribers=$(yt-dlp --cookies "$cookies_file" --print "%(channel_follower_count)s" "$input_url" | head -1)
    echo "Channel subscribers: $subscribers"
fi

mkdir -p subs
cd subs

# Get list of already downloaded video IDs from existing files
downloaded_ids=$(ls *.en.vtt 2>/dev/null | sed 's/.*\[\([^]]*\)\].*/\1/' | sort)

count=0
max_per_run=5
# Prepare list of IDs to download
to_download=""
for id in $video_ids; do
    if echo "$downloaded_ids" | grep -q "^$id$"; then
        echo "Skipping $id (already downloaded)"
    else
        to_download="$to_download $id"
        count=$((count + 1))
        if [ $count -ge $max_per_run ]; then
            break
        fi
    fi
done

# Download in parallel, 3 at a time
echo $to_download | tr ' ' '\n' | xargs -n 1 -P 3 -I {} sh -c '
    yt-dlp --cookies-from-browser chrome --write-auto-subs --sub-langs en,he --skip-download "https://youtu.be/$1"
    vtt_file="Thinking According to Alan Watts/*$1*.en.vtt"
    if [ ! -f "$vtt_file" ] || [ $(stat -f%z "$vtt_file") -lt 100 ]; then
        echo "No subs for $1, downloading audio and transcribing..."
        yt-dlp --cookies-from-browser chrome --extract-audio --audio-format webm --audio-quality 0 -o "audio_$1.%(ext)s" "https://youtu.be/$1"
        python3 ../scripts/transcribe.py "audio_$1.webm"
        mv "audio_$1.txt" "$vtt_file"  # Rename to vtt for consistency
        rm "audio_$1.webm"  # Delete audio file after transcription
    fi
    sleep 5
' -- {}
echo "All subtitles downloaded."

# Combine English subs
cat *.en.vtt > english_subs.vtt 2>/dev/null || echo "No English subs"

# Combine Hebrew subs if exist
cat *.he.vtt > hebrew_subs.vtt 2>/dev/null || echo "No Hebrew subs"