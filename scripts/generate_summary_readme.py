import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# --- Configuration ---
# Load environment variables (e.g., GEMINI_API_KEY from .env file for local testing)
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables or .env file.")
    print("Please set the GEMINI_API_KEY environment variable or create a .env file.")
    exit(1)

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)
# You can choose a different model if 'gemini-pro' doesn't suit your needs, e.g., 'gemini-1.5-flash'
MODEL_NAME = 'gemini-1.5-flash'

# Directory where your docker-compose projects are located
DOCKER_APPS_ROOT = Path(__file__).parent.parent
# Path to the main README.md to be updated
MAIN_README_PATH = DOCKER_APPS_ROOT / "docs" / "index.md"
# Marker for where to insert the AI-generated summaries
SUMMARY_START_MARKER = "<!-- AI_SUMMARY_START -->"
SUMMARY_END_MARKER = "<!-- AI_SUMMARY_END -->"

# --- AI Integration ---
def get_ai_summary(text_content: str, service_name: str) -> str:
    prompt = f"Summarize the following documentation for a home lab portfolio, focusing on the service's purpose, key features, and technologies used, in about 3-4 concise sentences. This summary is for the '{service_name}' service.\n\nContent:\n{text_content}"

    print(f"DEBUG: Calling Gemini API for '{service_name}' summary...")
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        # Access the text from the response object
        summary_text = response.text.strip()
        print(f"DEBUG: Successfully got summary for '{service_name}'.")
        return f"**{service_name}:** {summary_text}"
    except Exception as e:
        print(f"ERROR: AI summarization failed for '{service_name}': {e}")
        return f"**{service_name}:** *AI summary unavailable due to error: {e}*"

# --- Main Script Logic ---
def generate_main_readme():
    summaries = []
    
    # Use rglob to find all docker-compose.yml files recursively
    for docker_compose_path in DOCKER_APPS_ROOT.rglob("docker-compose.yml"):
        service_dir = docker_compose_path.parent
        readme_path = service_dir / "README.md"

        # Exclude top-level directories and specific folders
        if service_dir.name.startswith('.') or any(part in [".git", ".github", "scripts", "docs"] for part in service_dir.parts):
            continue

        if readme_path.exists():
            service_name = service_dir.name.replace("-", " ").title()
            print(f"Found service: {service_name} at {service_dir}")
            
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    sub_readme_content = f.read()
                
                ai_summary = get_ai_summary(sub_readme_content, service_name)
                summaries.append(ai_summary)
            except Exception as e:
                print(f"Error processing {readme_path}: {e}")
                summaries.append(f"**{service_name}:** *Error summarizing this service: {e}*")

    # Read existing main README content
    main_readme_content = ""
    if MAIN_README_PATH.exists():
        with open(MAIN_README_PATH, 'r', encoding='utf-8') as f:
            main_readme_content = f.read()
    else:
        # Initial content if README.md doesn't exist
        main_readme_content = "# Home Lab Docker Services\n\n" \
                              "This repository manages the `docker-compose.yml` configurations and associated files for all containerized applications running in my personal home lab environment.\n\n" \
                              "## Managed Services Overview\n" + SUMMARY_START_MARKER + "\n" + SUMMARY_END_MARKER + "\n"

    # Prepare the new summary block
    new_summary_block = "\n\n".join(summaries)
    
    # Replace content between markers
    if SUMMARY_START_MARKER in main_readme_content and SUMMARY_END_MARKER in main_readme_content:
        # Use re.DOTALL to match across multiple lines
        updated_readme_content = re.sub(
            f"{re.escape(SUMMARY_START_MARKER)}.*{re.escape(SUMMARY_END_MARKER)}",
            f"{SUMMARY_START_MARKER}\n{new_summary_block}\n{SUMMARY_END_MARKER}",
            main_readme_content,
            flags=re.DOTALL
        )
    else:
        # If markers are missing, append the block to the end of the file.
        # You might want to refine this to insert at a specific section if needed.
        updated_readme_content = main_readme_content + "\n\n## Managed Services Overview\n" + \
                                 SUMMARY_START_MARKER + "\n" + new_summary_block + "\n" + SUMMARY_END_MARKER + "\n"

    # Write the updated README.md
    with open(MAIN_README_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_readme_content)
    
    print(f"Successfully updated {MAIN_README_PATH}")

if __name__ == "__main__":
    generate_main_readme()
