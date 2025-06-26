# analyze_diff.py - This script contains the core AI analysis logic.
# It reads input from environment variables, calls the AI API, and writes results to files.

import os
import requests
import json

def construct_gemini_payload(prompt: str, model_name: str) -> dict:
    """
    Constructs the payload for the Google Gemini API.
    Args:
        prompt: The text prompt containing the Git diff and instructions for the AI.
        model_name: The specific Gemini model name (e.g., 'gemini-2.0-flash').
    Returns:
        A dictionary representing the JSON payload for the Gemini API request.
    """
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        # Optional: Add generation config for structured output if needed in the future
        # "generationConfig": {
        #     "responseMimeType": "application/json",
        #     "responseSchema": {
        #         "type": "OBJECT",
        #         "properties": {
        #             "analysisReport": {"type": "STRING"},
        #             "status": {"type": "STRING"}
        #         }
        #     }
        # }
    }
    return payload

def construct_openai_payload(prompt: str, model_name: str) -> dict:
    """
    Constructs the payload for the OpenAI Chat Completions API.
    Args:
        prompt: The text prompt containing the Git diff and instructions for the AI.
        model_name: The specific OpenAI model name (e.g., 'gpt-4o', 'gpt-3.5-turbo').
    Returns:
        A dictionary representing the JSON payload for the OpenAI API request.
    """
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000, # Max tokens for the AI's response
        "temperature": 0.7 # Controls randomness, 0.7 is usually good for analytical tasks
    }
    return payload

# You can add more functions here for other AI providers, e.g.,
# def construct_anthropic_payload(prompt: str, model_name: str) -> dict:
#     # ... Anthropic specific payload ...
#     pass

def analyze_merge_issues(
    diff_content: str,
    ai_provider: str,
    api_key: str,
    model_name: str,
    api_base_url: str = ""
) -> tuple[str, str]:
    """
    Connects to the specified AI provider to analyze Git diff content.

    Args:
        diff_content: The Git diff string to be analyzed.
        ai_provider: The name of the AI service provider (e.g., "gemini", "openai").
        api_key: The API key for the chosen AI service.
        model_name: The specific model name to use.
        api_base_url: Optional base URL for the API.

    Returns:
        A tuple: (analysis_report_text, status_string)
        - analysis_report_text: The detailed report from the AI.
        - status_string: "PASS" or "FAIL" based on AI's overall assessment.
    """
    if not diff_content.strip():
        return "Error: No branch differences provided for analysis.", "FAIL"
    if not api_key:
        return f"Error: API key for {ai_provider} not provided. Please set the 'ai_api_key' input.", "FAIL"

    # Define the comprehensive prompt for the AI.
    # This prompt guides the AI on what to look for and how to format its response.
    prompt = f"""
    You are an AI assistant specialized in identifying potential issues during code merges.
    Analyze the following Git diff content and highlight any potential:
    1.  **Merge Conflicts:** Direct line-by-line conflicts that Git might struggle with, or logical conflicts.
    2.  **Breaking Changes:** Changes that might break existing functionality, APIs, or contracts in the target branch.
    3.  **Architectural Incompatibilities:** Issues related to how new code integrates with the existing architecture, design patterns, or established modules.
    4.  **Dependency Conflicts:** Changes in package versions, new dependencies, or dependency removals that might conflict or cause instability.
    5.  **Logical Errors/Unexpected Side Effects:** Subtle bugs or unintended consequences that might arise from the interaction of the changes.
    6.  **Performance or Scalability Regressions:** Changes that could negatively impact application performance or scalability.
    7.  **Security Vulnerabilities:** New patterns or modifications that introduce potential security risks.

    Consider common development practices, module dependencies, and potential interactions between different parts of the codebase.

    **Git Diff Content for Analysis:**
    ```diff
    {diff_content}
    ```

    Provide a concise summary of potential issues, explain why they are issues, and suggest concrete mitigation strategies.
    If no obvious issues are apparent based on the provided diff, state that explicitly.
    
    IMPORTANT: On a new line at the very end of your response, provide an overall status using one of these exact phrases:
    "Overall Status: PASS" if no significant issues are found that require immediate attention or blocking.
    "Overall Status: FAIL" if significant issues (e.g., breaking changes, critical conflicts, severe vulnerabilities) are detected that warrant blocking or immediate review.
    """

    # Prepare headers for the API request
    headers = {
        'Content-Type': 'application/json',
    }
    final_api_url = ""
    payload = {}

    # Logic to construct API URL and payload based on the AI provider
    if ai_provider.lower() == 'gemini':
        # For Gemini, the API key is typically a query parameter
        base_url = api_base_url if api_base_url else "https://generativelanguage.googleapis.com/v1beta/models"
        final_api_url = f"{base_url}/{model_name}:generateContent?key={api_key}"
        payload = construct_gemini_payload(prompt, model_name)
    elif ai_provider.lower() == 'openai':
        # For OpenAI, the API key is an Authorization header
        base_url = api_base_url if api_base_url else "https://api.openai.com/v1"
        final_api_url = f"{base_url}/chat/completions"
        headers['Authorization'] = f'Bearer {api_key}'
        payload = construct_openai_payload(prompt, model_name)
    # Add more elif blocks here for other providers as needed
    # elif ai_provider.lower() == 'anthropic':
    #     base_url = api_base_url if api_base_url else "https://api.anthropic.com/v1"
    #     final_api_url = f"{base_url}/messages"
    #     headers['x-api-key'] = api_key
    #     headers['anthropic-version'] = '2023-06-01' # Required for Anthropic
    #     payload = construct_anthropic_payload(prompt, model_name)
    else:
        return f"Error: Unsupported AI provider '{ai_provider}'. Supported providers are 'gemini', 'openai'.", "FAIL"

    try:
        # Make the HTTP POST request to the AI API
        response = requests.post(final_api_url, headers=headers, data=json.dumps(payload), timeout=300) # 5 min timeout
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)

        result = response.json()
        analysis_text = ""

        # Extract the AI's generated content based on the provider's JSON structure
        if ai_provider.lower() == 'gemini':
            if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
                analysis_text = result['candidates'][0]['content']['parts'][0]['text']
        elif ai_provider.lower() == 'openai':
            if result.get('choices') and result['choices'][0].get('message') and result['choices'][0]['message'].get('content'):
                analysis_text = result['choices'][0]['message']['content']
        # Add content extraction logic for other providers here

        if not analysis_text:
            return f"No analysis result found from {ai_provider}. API Response: {json.dumps(result, indent=2)}", "FAIL"

        # --- Parse the analysis_text to separate report from status ---
        report_text = analysis_text
        status_value = "FAIL" # Default status

        # Split the response into lines to find the status line at the very end
        report_lines = analysis_text.splitlines()
        
        # Check if the last line contains the status phrase
        if report_lines and "Overall Status:" in report_lines[-1]:
            last_line = report_lines[-1].strip()
            if "PASS" in last_line.upper():
                status_value = "PASS"
            elif "FAIL" in last_line.upper():
                status_value = "FAIL"
            # Remove the status line from the report text for cleaner output
            report_text = "\n".join(report_lines[:-1]).strip()
        else:
            # If the AI didn't explicitly provide the status line, try to infer.
            # This is a fallback and can be less reliable.
            if "no obvious issues" in analysis_text.lower() or \
               "no significant issues" in analysis_text.lower() or \
               "looks good to merge" in analysis_text.lower():
                status_value = "PASS"
            # Otherwise, default to FAIL if issues are discussed but no clear PASS
            # If the AI describes any issues, we consider it a FAIL unless explicitly stated PASS
            # This logic can be refined based on AI's typical response patterns
            # For now, if no "PASS" is found and issues are mentioned, it implies a "FAIL"

        return report_text, status_value

    except requests.exceptions.RequestException as e:
        # Catch network-related errors, timeouts, etc.
        return f"Error calling {ai_provider} API: {e}. Please check network connection, API key, model name, or base URL.", "FAIL"
    except json.JSONDecodeError:
        # Catch errors if the API response is not valid JSON
        return f"Error: Failed to decode JSON response from {ai_provider} API. Response content: {response.text}", "FAIL"
    except Exception as e:
        # Catch any other unexpected errors
        return f"An unexpected error occurred during analysis: {e}", "FAIL"

if __name__ == "__main__":
    # This block executes when the script is run directly (e.g., by GitHub Actions)

    # Retrieve inputs from environment variables set by action.yml
    diff_data = os.environ.get('DIFF_DATA', '')
    ai_provider = os.environ.get('AI_PROVIDER', '').strip().lower()
    api_key = os.environ.get('AI_API_KEY', '').strip()
    api_base_url = os.environ.get('API_BASE_URL', '').strip()
    model_name = os.environ.get('MODEL_NAME', '').strip()

    # Provide default values if not explicitly set (e.g., for local testing or unexpected edge cases)
    if not ai_provider:
        ai_provider = 'gemini' # Fallback provider
    if not model_name:
        if ai_provider == 'gemini':
            model_name = 'gemini-2.0-flash' # Fallback Gemini model
        elif ai_provider == 'openai':
            model_name = 'gpt-3.5-turbo' # Fallback OpenAI model (cost-effective)
        else:
            model_name = 'default-model' # Generic fallback

    # Perform the analysis
    report, status = analyze_merge_issues(diff_data, ai_provider, api_key, model_name, api_base_url)

    # Write the results to files. GitHub Actions will read these files.
    with open('ai_analysis_report.txt', 'w') as f:
        f.write(report)
    with open('ai_analysis_status.txt', 'w') as f:
        f.write(status)

    # Optional: Print to console for debugging purposes in GitHub Actions logs
    # print("\n--- AI Analysis Report ---")
    # print(report)
    # print(f"\n--- AI Analysis Status: {status} ---")