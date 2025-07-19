# LangFlow Examples Repo

Clean repository with basic LangFlow workflow examples for AI models.

## Table of Contents
- [Overview](#overview)
- [Examples](#examples)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview
This repo provides 3 simple, importable JSON workflows for LangFlow, each using a single AI model in a basic Chat Input -> Model -> Chat Output pipeline. No extras – clean and focused.

## Examples
- [GPT-4o Workflow](./examples/gpt-4o-workflow.json): For OpenAI's GPT-4o.
- [Gemini 2.5 Flash Workflow](./examples/gemini-2.5-flash-workflow.json): For Google's Gemini 2.5 Flash.
- [Claude Sonnet 4 Workflow](./examples/claude-sonnet-4-workflow.json): For Anthropic's Claude Sonnet 4.

## Usage
1. Import the JSON into LangFlow.
2. Add your API key.
3. Run the flow for basic chat testing.

## Deployment
Deploy to Kubernetes using the /helm chart:
1. Install Helm.
2. Run `helm install my-release ./helm` (customize values.yaml for PostgreSQL and MCP scaling).
3. Scale MCP servers by updating replicas in values.yaml and re-deploying with `helm upgrade my-release ./helm --set mcp.replicas=3`.

## Contributing
Fork and submit PRs for improvements, but keep it clean – no adding extra files/scripts.