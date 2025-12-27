import re
from typing import List
from .logging_config import logger


def estimate_token_count(text: str) -> int:
    """
    Estimate the number of tokens in a text string.
    This is a rough approximation: 1 token ≈ 4 characters in English text.
    For more accurate token counting, a specific tokenizer for the target model would be needed.

    Args:
        text: Input text string

    Returns:
        Estimated number of tokens
    """
    return len(text) // 4


def chunk_text(text: str, max_tokens: int = 1000, min_tokens: int = 500) -> List[str]:
    """
    Split text into chunks with sizes specified in token range (500-1000 tokens).
    Uses character-based approximation since actual tokenization is computationally expensive.

    Args:
        text: Text string to be chunked
        max_tokens: Maximum tokens per chunk (default 1000, corresponds to ~4000 characters)
        min_tokens: Minimum tokens per chunk before forcing a split (default 500, ~2000 characters)

    Returns:
        List of text chunks
    """
    if not text:
        return []

    # Convert token estimates to character approximations
    # 1 token ≈ 4 characters for English text
    max_chars = max_tokens * 4
    min_chars = min_tokens * 4

    # Split text into sentences to avoid breaking in the middle of sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding the sentence exceeds the max size, start a new chunk
        if len(current_chunk) + len(sentence) > max_chars:
            # If current chunk is already larger than min_chunk_size, save it
            if len(current_chunk) >= min_chars:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            # If the sentence by itself is longer than max_chunk_size, we need to split it
            elif len(current_chunk) == 0 and len(sentence) > max_chars:
                # Split the long sentence into smaller parts
                sentence_parts = split_long_sentence(sentence, max_chars)
                chunks.extend(sentence_parts[:-1])  # Add all but the last part
                current_chunk = sentence_parts[-1]  # Keep the last part for further processing
            else:
                # Add to current chunk and continue
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    # Add the final chunk if it has content
    if current_chunk:
        chunks.append(current_chunk.strip())

    logger.info(f"Text chunked into {len(chunks)} chunks (target: {min_tokens}-{max_tokens} tokens per chunk)")
    return chunks


def split_long_sentence(sentence: str, max_chars: int) -> List[str]:
    """
    Split a sentence that is longer than max_chars into smaller parts

    Args:
        sentence: A single long sentence to split
        max_chars: Maximum characters per part

    Returns:
        List of sentence parts
    """
    parts = []
    for i in range(0, len(sentence), max_chars):
        part = sentence[i:i + max_chars]
        parts.append(part)

    return parts