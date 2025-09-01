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

### 1. Create the Workflow File

Create a workflow file in your repository at `.github/workflows/pr-ai-analysis.yml` (or any name you prefer):

```yaml
name: AI Pull Request Merge Check

on:
  pull_request:
    branches:
      - main # Replace 'main' with your default branch name if different
    types: [opened, synchronize, reopened]

jobs:
  ai_merge_analysis:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      - name: Checkout Pull Request Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run AI-Powered Merge Analysis
        uses: shekhar199511/ai-merge-analyzer@v1.0.2
        id: ai_analysis_step
        with:
          ai_provider: 'gemini' # Or 'openai', etc.
          ai_api_key: ${{ secrets.GEMINI_API_KEY }} # Ensure this matches your secret name!
          model_name: 'gemini-2.0-flash'
          # api_base_url: 'https://api.my-custom-ai-service.com/v1' # Optional

      - name: Set Pull Request Status Check
        if: steps.ai_analysis_step.outputs.analysis_status == 'FAIL'
        shell: bash
        run: |
          echo "AI analysis reported issues. This job will fail to block the merge."
          exit 1
```

### 2. Store Your API Key

- Go to your repository’s **Settings > Secrets and variables > Actions**.
- Click **New repository secret**.
- Name it according to your provider (e.g., `GEMINI_API_KEY`, `OPENAI_API_KEY`) and paste your API key.

### 3. Configure Inputs

- Set `ai_provider` to your chosen provider (e.g., `gemini`, `openai`).
- Set `model_name` to the model you want to use (e.g., `gemini-2.0-flash`, `gpt-4o`).
- Optionally, set `api_base_url` if you use a custom endpoint.

### 4. Folder and File Setup

You only need to create the workflow file in `.github/workflows/` in your repository.  
No other folders or files are required; the action handles all logic internally.

### 5. Commit and Push

- Commit your workflow file and push it to your repository.
- The action will run automatically on every pull request.

## What changes do other projects need to make?

- **Add API Key:** Store your AI provider API key as a GitHub Secret.
- **Workflow Update:** Add the action step to your PR workflow file.
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
Why: <Explanation of why this issue may cause problems>
Solution: <Suggested fix or improvement>
---
Problem: <Another detected issue>
Why: <Explanation>
Solution: <Suggestion>
---
```
</details>

**Overall Status:** 🟢 PASSED (No major issues detected)  
or  
**Overall Status:** 🔴 FAILED (Potential issues detected)

## Contributing

Contributions and suggestions are welcome! Please open issues or PRs for improvements.

## License

MIT License