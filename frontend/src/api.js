// api.js
// Fetch API integration for the AI Comment Moderation backend.
// Set REACT_APP_API_URL in your .env file for production.

const BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Analyze a comment through the moderation API.
 * @param {string} comment
 * @returns {Promise<{comment, toxicity, spam, sentiment, confidence, all_scores}>}
 */
export async function moderateComment(comment) {
  const response = await fetch(`${BASE_URL}/moderate-comment`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ comment }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Health-check the backend.
 * @returns {Promise<{status: string}>}
 */
export async function healthCheck() {
  const response = await fetch(`${BASE_URL}/health`);
  return response.json();
}
