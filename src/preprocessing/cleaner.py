import re

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # remove URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)

    # remove markdown code blocks
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)

    # remove inline code `code`
    text = re.sub(r"`.*?`", " ", text)

    # remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # remove GitHub mentions @user
    text = re.sub(r"@\w+", " ", text)

    # remove issue references #1234
    text = re.sub(r"#\d+", " ", text)

    # remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # lowercase (optional but recommended for ML)
    text = text.lower()

    return text
