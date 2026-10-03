def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Handle paragraphs larger than the chunk size.
        if len(paragraph) > chunk_size:
            words = paragraph.split()
            current_part = ""

            for word in words:
                candidate = (
                    current_part + " " + word
                    if current_part
                    else word
                )

                if len(candidate) <= chunk_size:
                    current_part = candidate
                else:
                    if current_part:
                        chunks.append(current_part)

                    # Start the next part with overlap words.
                    overlap_words = []
                    overlap_length = 0

                    for previous_word in reversed(current_part.split()):
                        if overlap_length + len(previous_word) + 1 > chunk_overlap:
                            break

                        overlap_words.insert(0, previous_word)
                        overlap_length += len(previous_word) + 1

                    current_part = " ".join(overlap_words + [word])

            if current_part:
                current_chunk = current_part

            continue

        candidate = (
            current_chunk + "\n\n" + paragraph
            if current_chunk
            else paragraph
        )

        if len(candidate) <= chunk_size:
            current_chunk = candidate

        else:
            chunks.append(current_chunk.strip())

            # Create word-aware overlap.
            overlap_words = []
            overlap_length = 0

            for word in reversed(current_chunk.split()):
                if overlap_length + len(word) + 1 > chunk_overlap:
                    break

                overlap_words.insert(0, word)
                overlap_length += len(word) + 1

            current_chunk = " ".join(overlap_words)
            current_chunk += "\n\n" + paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks