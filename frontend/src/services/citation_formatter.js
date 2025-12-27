/**
 * Format citations according to textbook standards
 */

export const formatCitation = (chapter, section, pageNumber) => {
  if (!chapter || !section || !pageNumber) {
    return '';
  }
  
  return `Chapter ${chapter} - ${section} (p. ${pageNumber})`;
};

export const formatMultipleCitations = (citations) => {
  if (!citations || citations.length === 0) {
    return '';
  }
  
  return citations.join('; ');
};

export const parseCitation = (citationString) => {
  // Parse a citation string to extract chapter, section, and page
  const regex = /Chapter\s+([^-\s]+)\s*-\s*([^(\n]+)(?:\s+\(p\.\s*(\d+)\))?/;
  const match = citationString.match(regex);
  
  if (match) {
    return {
      chapter: match[1].trim(),
      section: match[2].trim(),
      pageNumber: match[3] ? parseInt(match[3], 10) : null
    };
  }
  
  return null;
};

export const validateCitation = (citation) => {
  // Check if the citation follows the expected format
  const regex = /^Chapter\s+.+\s*-\s*.+\s+\(p\.\s*\d+\)$/;
  return regex.test(citation);
};