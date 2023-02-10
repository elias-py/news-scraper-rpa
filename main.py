import os
from ExtractNewsInfo import ExtractNewsInfo


if __name__ == "__main__":
    extract_news_info = ExtractNewsInfo(
        os.getenv('PHRASE_TO_SEARCH'),
        os.getenv('SECTION_TO_SELECT'),
        os.getenv('MONTHS_BEFORE')
    )

    extract_news_info.extract_info()
