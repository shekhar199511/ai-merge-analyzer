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

To integrate Universal AI Merge Issue Analyzer into your project, follow these steps:

### 1. Add the Action to Your Workflow

Create or update your workflow file (e.g., `.github/workflows/ai-merge-analyzer.yml`) with the following content:

```yaml
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

### 2. Store Your API Key

- Go to your repository’s **Settings > Secrets and variables > Actions**.
- Click **New repository secret**.
- Name it `AI_API_KEY` and paste your AI provider API key.

### 3. Configure Inputs

- Set `ai_provider` to your chosen provider (e.g., `openai`, `gemini`).
- Set `model_name` to the model you want to use (e.g., `gpt-4o`, `gemini-2.0-flash`).
- Optionally, set `api_base_url` if you use a custom endpoint.

### 4. Commit and Push

- Commit your workflow file and push it to your repository.
- The action will run automatically on every pull request.

## What changes do other projects need to make?

- **Add API Key:** Store your AI provider API key as a GitHub Secret named `AI_API_KEY`.
- **Update Workflow:** Add the action step to your PR workflow file.
- **Select Provider/Model:** Update workflow inputs to match your preferred AI provider and model.
- **(Optional) Custom Endpoint:** Set `api_base_url` if you use a non-default endpoint.

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

## License