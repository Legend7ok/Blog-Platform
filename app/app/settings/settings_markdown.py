MARKDOWN_ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
    "blockquote",
    "code",
    "pre",
    "a",
]

MARKDOWN_ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],
}

MARKDOWN_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

MARKDOWN_EXTENSIONS = ["extra", "sane_lists"]
