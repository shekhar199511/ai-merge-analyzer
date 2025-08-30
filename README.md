# Universal AI Merge Issue Analyzer

An AI-powered GitHub Action designed to proactively identify potential issues during code merges, specifically targeting Pull Request (PR) workflows within Git-based repositories.

## What is this project?

**Universal AI Merge Issue Analyzer** uses generative AI models to analyze code diffs in PRs. It helps detect merge conflicts, breaking changes, logical errors, and provides actionable suggestions before code is merged.

## Use Cases

- Automated code review for PRs
- Early detection of merge conflicts and breaking changes
- AI-powered suggestions for resolving code issues
- Supports multiple AI providers and models

## Technical Details

- **GitHub Action:** Implemented as a composite action for easy integration.
- **AI Providers:** Supports any LLM provider (e.g., Gemini, OpenAI, Anthropic) via configurable inputs.
- **Flexible Model Selection:** Choose your preferred model (e.g., `gemini-2.0-flash`, `gpt-4o`).
- **Secure API Key Handling:** Requires API keys to be stored as GitHub Secrets.
- **Customizable Endpoints:** Optionally specify custom API endpoints for self-hosted or proxy models.
- **Markdown-formatted Reports:** Comments on PRs with a clear, readable, and collapsible AI analysis.

## How can other projects use it?

1. **Add the Action to Your Workflow:**

   ```yaml
   # .github/workflows/ai-merge-analyzer.yml
   name: AI Merge Analysis

   on:
     pull_request:

   jobs:
     ai-merge-analysis:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: AI Merge Analyzer
           uses: shekhar199511/ai-merge-analyzer@v1.0.0
           with:
             ai_provider: "openai" # or "gemini"
             ai_api_key: ${{ secrets.AI_API_KEY }}
             model_name: "gpt-4o" # or "gemini-2.0-flash"
             api_base_url: "" # Optional
   ```

2. **Store Your API Key:**
   - Add your AI provider API key as a secret in your repository settings (e.g., `AI_API_KEY`).

3. **Configure Inputs:**
   - Choose your provider and model via workflow inputs.
   - Optionally set a custom API endpoint.

## What changes do other projects need to make?

- **API Key:** Add your AI provider API key as a GitHub Secret.
- **Workflow Update:** Add the action step to your PR workflow.
- **Model/Provider Selection:** Update inputs to match your preferred AI provider and model.

## Flexibility Provided

- **Multi-provider Support:** Easily switch between supported LLMs (Gemini, OpenAI, etc.).
- **Custom Models:** Use any model supported by your provider.
- **Custom Endpoints:** Point to self-hosted or proxy endpoints.
- **Configurable Prompts:** (Future) Customize the prompt sent to the AI for tailored analysis.

## Example Output

The action will comment on your PR with a report like:

<details>
<summary>Full AI Analysis Report</summary>

```
Problem: <Brief description of the detected issue>
Mitigation: <Explanation of why this issue may cause problems>
---
Problem: <Another detected issue>
Mitigation: <Explanation>
---
```
</details>

**Overall Status:** 🟢 PASSED (No major issues detected)  
or  
**Overall Status:** 🔴 FAILED (Potential issues detected)

## Contributing

Contributions and suggestions are welcome! Please open issues or PRs for improvements.

##