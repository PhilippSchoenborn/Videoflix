/**
 * Extracts error messages from various error response formats.
 * @param errorData - The error data from the API response.
 * @returns Array of error messages as strings.
 */
export function extractErrorMessages(errorData: any): string[] {
  const messages: string[] = [];
  if (typeof errorData === 'string') return [errorData];
  if (Array.isArray(errorData)) return errorData.flat();
  if (typeof errorData === 'object' && errorData !== null) {
    Object.values(errorData).forEach(value => {
      if (Array.isArray(value)) messages.push(...value);
      else if (typeof value === 'string') messages.push(value);
      else if (typeof value === 'object' && value !== null) {
        messages.push(...extractErrorMessages(value));
      }
    });
  }
  return messages;
}
