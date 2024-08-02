from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from fpdf import FPDF

# Function to get YouTube subtitles
def get_youtube_subtitles(video_url):
    # Extract YouTube video ID from URL
    video_id = video_url.split("v=")[-1]
    try:
        # Get the transcript (subtitles) for the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        # Format the transcript as plain text
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript)
        return text_formatted
    except Exception as e:
        return str(e)

# Function to format subtitles text
def format_subtitles(text):
    sentences = text.split('\n')
    formatted_text = ""
    for sentence in sentences:
        if sentence.strip():
            formatted_text += sentence.strip().capitalize() + '. '
    return formatted_text

# Example YouTube video URL
video_url = "https://www.youtube.com/watch?v=Debjcl5z9Dw"
# Get and format the subtitles
subtitles = get_youtube_subtitles(video_url)
formatted_subtitles = format_subtitles(subtitles)

# PDF creation class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'YouTube Video Subtitles', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Create and save the PDF
pdf = PDF()
pdf.add_page()
pdf.chapter_title("Subtitles")
pdf.chapter_body(formatted_subtitles)

# Save the PDF to a file
pdf_file_path = "YouTube_Subtitles.pdf"
pdf.output(pdf_file_path)

print(f"PDF saved as {pdf_file_path}")