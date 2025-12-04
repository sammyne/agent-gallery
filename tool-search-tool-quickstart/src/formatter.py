from langchain.messages import ContentBlock


def get_msg_title_repr(title: str, *, bold: bool = False) -> str:
    """Get a title representation for a message.

    Args:
        title: The title.
        bold: Whether to bold the title.

    Returns:
        The title representation.

    """
    padded = " " + title + " "
    sep_len = (80 - len(padded)) // 2
    sep = "=" * sep_len
    second_sep = sep + "=" if len(padded) % 2 else sep
    if bold:
        padded = f"\033[1m{padded}\033[0m"
    return f"{sep}{padded}{second_sep}"


def pretty_print_content_blocks(type: str, blocks: list[ContentBlock]):
    title = get_msg_title_repr(f"{type.title()} Message")
    print(f"{title}\n")

    if len(blocks) == 1:
        print(f"\n{stringify_content_block(blocks[0])}")
        return

    for i, b in enumerate(blocks):
        print(f"\n=== {b.__class__.__name__}[{i}]===\n{stringify_content_block(b)}")


def stringify_content_block(block: ContentBlock) -> str:
    t = block["type"]
    if t == "text":
        return block["text"]
    else:
        raise ValueError(f"Unsupported ContentBlock\n: {t}")
