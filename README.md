# README: Customer Support Agent (Coordinated Tools)

This project features an advanced AI-powered support assistant built with the **Agent Development Kit (ADK)**. It demonstrates best practices for **multi-tool coordination**, **strategic instruction design**, and **structured error handling**.

## Project Overview
Unlike basic agents with vague instructions, this agent follows a defined **Multi-Tool Workflow**. It is designed to handle e-commerce tasks by intelligently sequencing tools and managing various return values to ensure a predictable and professional customer experience.

## Agent Identity & Behavior
The agent is defined by five professional instruction patterns to ensure high-quality interactions:
*   **Identity:** Adopts the persona, a Senior Technical Support Specialist with 5 years of experience.
*   **Mission:** Efficiently resolving technical and order-related issues while maintaining professionalism.
*   **Methodology:** Follows a strict 4-step workflow: **Acknowledge** → **Clarify** → **Solve** → **Verify**.
*   **Boundaries:** Strict rules against providing passwords, sharing other customers' data, or giving legal/medical advice.
*   **Few-Shot Examples:** Includes demonstrations of desired tone and troubleshooting steps for common scenarios like login issues or out-of-scope refund requests.

## Integrated Tool Suite
The agent is equipped with custom Python functions that represent core business logic:
1.  **`lookup_customer`**: Retrieves profile information using an email address.
2.  **`check_order_status`**: Provides real-time shipping and tracking updates.
3.  **`process_refund`**: Handles refund requests according to company policy.

## Strategic Orchestration & Error Handling
The agent is specifically instructed on **how** and **when** to use its tools:
*   **Logical Sequencing:** It is taught to call `lookup_customer` or `check_order_status` to verify order details before attempting a refund.
*   **Error Actions:** It follows specific strategies for different return values:
    *   **`not_found`**: Asks the user to double-check their ID instead of hallucinating.
    *   **`invalid_format`**: Explains the correct format (e.g., "Order IDs start with 'ORD'").
    *   **`permission_denied`**: Triggers an immediate escalation path to a human supervisor.

## Prerequisites
*   **Python 3.11 or higher**.
*   **Google ADK Framework** (`pip install google-adk`).
*   A **Gemini 2.0+ Model** (required for advanced tool orchestration features).

## Installation & Setup

1.  **Initialize the Project:**
    ```bash
    adk create customer_support_agent
    cd customer_support_agent
    ```

2.  **Configure Environment Variables:**
    Update your **`.env`** file with your Gemini API key:
    ```text
    GOOGLE_GENAI_USE_VERTEXAI=0
    GOOGLE_API_KEY=your-actual-api-key-here
    ```
    *Note: Never commit this file to version control (Git)*.

3.  **Run the Agent:**
    Launch the web interface to interact with the agent:
    ```bash
    adk web
    ```

## Project Structure
*   **`agent.py`**: The core file containing the `LlmAgent` definition, strategic instructions, and tool functions.
*   **`__init__.py`**: Required for the ADK framework to discover and load the agent.
*   **`.env`**: Secure storage for sensitive API credentials.
