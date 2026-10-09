from ddgs import DDGS


def web_search(query: str) -> str:
    """
    Web Search Tool.

    Searches the web using DuckDuckGo and returns
    a concise list of search results.
    """

    if not query or not query.strip():
        return "Error: Search query cannot be empty."

    try:
        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            body = result.get("body", "No description")
            url = result.get("href", "No URL")

            formatted_results.append(
                f"{index}. {title}\n"
                f"Description: {body}\n"
                f"URL: {url}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:
        return f"Web search failed: {error}"
