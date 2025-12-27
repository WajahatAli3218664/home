"""
Content chunking service for the AI-powered book RAG system
"""
import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ContentChunk:
    """Represents a chunk of content with metadata"""
    id: str
    text: str
    metadata: Dict[str, Any]
    index: int


class ContentChunkingService:
    """
    Service for implementing intelligent chunking algorithms for books
    """
    
    def __init__(self, default_chunk_size: int = 512, overlap_size: int = 50):
        """
        Initialize the content chunking service
        
        Args:
            default_chunk_size: Default size for content chunks (in characters)
            overlap_size: Size of overlap between chunks to maintain context
        """
        self.default_chunk_size = default_chunk_size
        self.overlap_size = overlap_size
    
    def chunk_by_paragraph(self, content: str, max_chunk_size: int = None) -> List[ContentChunk]:
        """
        Chunk content by paragraphs
        
        Args:
            content: The content to chunk
            max_chunk_size: Maximum size for each chunk (uses default if None)
        
        Returns:
            List of ContentChunk objects
        """
        if max_chunk_size is None:
            max_chunk_size = self.default_chunk_size
            
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        current_index = 0
        
        for para in paragraphs:
            # If adding the paragraph would exceed the max size, save the current chunk
            if len(current_chunk) + len(para) > max_chunk_size and current_chunk:
                chunks.append(ContentChunk(
                    id=f"chunk_{len(chunks)}",
                    text=current_chunk.strip(),
                    metadata={"type": "paragraph", "index": current_index},
                    index=current_index
                ))
                current_chunk = para
                current_index += 1
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
        
        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(ContentChunk(
                id=f"chunk_{len(chunks)}",
                text=current_chunk.strip(),
                metadata={"type": "paragraph", "index": current_index},
                index=current_index
            ))
        
        return chunks
    
    def chunk_by_sentences(self, content: str, max_chunk_size: int = None) -> List[ContentChunk]:
        """
        Chunk content by sentences, trying to keep chunks within the max size
        
        Args:
            content: The content to chunk
            max_chunk_size: Maximum size for each chunk (uses default if None)
        
        Returns:
            List of ContentChunk objects
        """
        if max_chunk_size is None:
            max_chunk_size = self.default_chunk_size
            
        # Split content into sentences
        sentence_pattern = r'[.!?]+\s+'
        sentences = re.split(sentence_pattern, content)
        
        # Add back the punctuation
        sentence_matches = list(re.finditer(sentence_pattern, content))
        sentences_with_punct = []
        start = 0
        for i, match in enumerate(sentence_matches):
            sentence = content[start:match.start()] + match.group().strip()
            sentences_with_punct.append(sentence)
            start = match.end()
        
        # Handle the last part
        if start < len(content):
            sentences_with_punct.append(content[start:])
        
        chunks = []
        current_chunk = ""
        current_index = 0
        
        for sentence in sentences_with_punct:
            # If adding the sentence would exceed the max size
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                chunks.append(ContentChunk(
                    id=f"chunk_{len(chunks)}",
                    text=current_chunk.strip(),
                    metadata={"type": "sentence", "index": current_index},
                    index=current_index
                ))
                current_chunk = sentence
                current_index += 1
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        
        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(ContentChunk(
                id=f"chunk_{len(chunks)}",
                text=current_chunk.strip(),
                metadata={"type": "sentence", "index": current_index},
                index=current_index
            ))
        
        return chunks
    
    def chunk_by_size(self, content: str, max_chunk_size: int = None) -> List[ContentChunk]:
        """
        Chunk content by a specific character size
        
        Args:
            content: The content to chunk
            max_chunk_size: Maximum size for each chunk (uses default if None)
        
        Returns:
            List of ContentChunk objects
        """
        if max_chunk_size is None:
            max_chunk_size = self.default_chunk_size
            
        chunks = []
        current_index = 0
        
        for i in range(0, len(content), max_chunk_size - self.overlap_size):
            # Calculate the end position for this chunk
            end_pos = min(i + max_chunk_size, len(content))
            
            # Get the chunk text
            chunk_text = content[i:end_pos]
            
            # Add overlap if it's not the last chunk
            if end_pos < len(content) and self.overlap_size > 0:
                overlap_end = min(end_pos + self.overlap_size, len(content))
                # Find a good breaking point (space) to avoid cutting words
                while overlap_end > end_pos and not content[overlap_end-1].isspace():
                    overlap_end -= 1
                if overlap_end > end_pos:
                    chunk_text = content[i:overlap_end]
            
            chunks.append(ContentChunk(
                id=f"chunk_{len(chunks)}",
                text=chunk_text,
                metadata={"type": "size-based", "index": current_index},
                index=current_index
            ))
            current_index += 1
        
        return chunks
    
    def intelligent_chunk(self, content: str, strategy: str = "sentence", max_chunk_size: int = None) -> List[ContentChunk]:
        """
        Apply intelligent chunking based on the specified strategy
        
        Args:
            content: The content to chunk
            strategy: The chunking strategy to use ("sentence", "paragraph", or "size")
            max_chunk_size: Maximum size for each chunk (uses default if None)
        
        Returns:
            List of ContentChunk objects
        """
        if strategy == "sentence":
            return self.chunk_by_sentences(content, max_chunk_size)
        elif strategy == "paragraph":
            return self.chunk_by_paragraph(content, max_chunk_size)
        elif strategy == "size":
            return self.chunk_by_size(content, max_chunk_size)
        else:
            raise ValueError(f"Unknown chunking strategy: {strategy}")