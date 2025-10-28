import transformers
from transformers import pipeline
import sys

def summarize_text(input_text: str) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python summarizer.py <input_text_file>")
    #     sys.exit(1)

    # input_file_path = sys.argv[1]
    # try:
    #     with open(input_file_path, "r", encoding="utf-8") as f:
    #         input_text = f.read()

    #     summary = summarize_text(input_text)
    #     print("Summary:")
    #     print(summary)
    # except Exception as e:
    #     print(f"Error reading file or summarizing text: {e}")
    #     sys.exit(1)
    with open("data/ocr_text/output.txt", "r", encoding="utf-8") as f:
        text = f.read()
    summary = summarize_text(text)
    with open("data/summaries/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Summary saved to data/summaries/summary.txt")