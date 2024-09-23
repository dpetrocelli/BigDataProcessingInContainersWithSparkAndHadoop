
# YouTube video ID
video_id = 'pK8u4QfdLx0&t'

from youtube_transcript_api import YouTubeTranscriptApi


try:
    # Try fetching the Spanish transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
    print("Spanish transcript found.")
except Exception:
    # If Spanish is not available, fetch the English transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    print("Spanish transcript not available. Fetched English transcript instead.")

# Convert the transcript into plain text
transcript_text = '\n'.join([entry['text'] for entry in transcript])

# Print the transcript
print(transcript_text)

# Optionally, save the transcript to a file
with open(f'{video_id}_transcript4.txt', 'w', encoding='utf-8') as file:
    file.write(transcript_text)
