/**
 * Utility function to add IDs to heading elements in HTML content for anchor links
 */

// Helper function to convert heading text to a URL-friendly ID
const createHeadingId = (text: string): string => {
  return text
    .toLowerCase()
    .trim()
    // Replace spaces and special characters with hyphens
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
};

// Process HTML string to add IDs to heading elements
export const addIdsToHeadings = (htmlContent: string): string => {
  // Regular expressions to match heading elements
  const headingRegex = /<(h[1-6])[^>]*>(.*?)<\/\1>/gi;

  return htmlContent.replace(headingRegex, (match, tag, content) => {
    // Extract text content from HTML (stripping any nested tags)
    const textContent = content.replace(/<[^>]*>/g, '').trim();
    
    // Create an ID from the text content
    const id = createHeadingId(textContent);
    
    // Check if the heading already has an ID attribute
    if (match.includes('id="')) {
      return match; // Return unchanged if already has an ID
    }
    
    // Add the id attribute to the heading element
    return match.replace(
      new RegExp(`<${tag}`, 'i'),
      `<${tag} id="${id}"`
    );
  });
};