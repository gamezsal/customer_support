"""
Customer Support Agent with Coordinated Tools
Demonstrates strategic tool combination, error handling, and agent instructions.

Reference: https://google.github.io/adk-docs/tools-custom/
"""

from google.adk.agents import LlmAgent

# Simulated database
ORDERS_DB = {
    "ORD123": {"status": "delivered", "total": 99.99, "items": ["Widget A"]},
    "ORD456": {"status": "processing", "total": 49.50, "items": ["Widget B"]}
}

# Tool 1: Check order status
def check_order_status(order_id: str) -> dict:
    """Checks the current status of a customer's order.

    Use this when a customer asks about their order status or delivery.

    Args:
        order_id (str): The order ID (e.g., "ORD123").

    Returns:
        dict: Order status information.
    """
    # Validate format
    if not order_id.startswith("ORD"):
        return {
            "status": "error",
            "error_type": "invalid_format",
            "error_message": "Order IDs must start with 'ORD' (e.g., ORD123)"
        }

    # Look up order
    if order_id not in ORDERS_DB:
        return {
            "status": "error",
            "error_type": "not_found",
            "error_message": f"Order {order_id} not found in system"
        }

    # Success
    order = ORDERS_DB[order_id]
    return {
        "status": "success",
        "order_id": order_id,
        "order_status": order["status"],
        "details": order
    }

# Tool 2: Process refund
def process_refund(order_id: str, reason: str) -> dict:
    """Processes a refund request for an order.
    Use this ONLY after verifying the order exists with check_order_status.
    """
    if order_id not in ORDERS_DB:
        return {
            "status": "error",
            "error_type": "order_not_found",
            "error_message": f"Cannot process refund - order {order_id} not found"
        }

    order = ORDERS_DB[order_id]

    if order["status"] == "delivered":
        return {
            "status": "success",
            "refund_amount": order["total"],
            "reference": f"REF{order_id[3:]}",
            "estimated_days": 5,
            "message": "Refund processed successfully"
        }
    else:
        return {
            "status": "error",
            "error_type": "cannot_refund",
            "error_message": f"Cannot refund order in '{order['status']}' status. Only delivered orders can be refunded."
        }

# Tool 3: Escalate to supervisor
def escalate_to_supervisor(issue_summary: str, order_id: str) -> dict:
    """Escalates complex issues to a human supervisor."""
    ticket_id = f"TICKET{hash(issue_summary) % 10000:04d}"
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": "Issue escalated to supervisor",
        "estimated_response": "within 2 hours",
        "order_id": order_id if order_id else "N/A"
    }

# Create customer support agent with strategic instructions
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='customer_support_agent',
    description='Handles customer inquiries about orders and refunds with comprehensive error handling.',
    instruction="""
    You are a helpful and empathetic customer support agent for an e-commerce company.

    # Your Capabilities
    You have three tools available:
    1. check_order_status(order_id)
    2. process_refund(order_id, reason)
    3. escalate_to_supervisor(issue_summary, order_id)

    # Workflow Guidelines
    ## For Order Status Inquiries:
    1. Greet the customer warmly
    2. Use check_order_status with the order ID
    3. Handle results (success, not_found, or invalid_format)

    ## For Refund Requests:
    1. Express empathy
    2. FIRST use check_order_status to verify the order exists
    3. If exists, use process_refund with order_id and reason
    4. Handle refund result (confirm success or explain policy if cannot_refund)

    ## Error Handling Strategy:
    - 'not_found': Ask to double-check or offer email search.
    - 'invalid_format': Explain the "ORD" prefix requirement.
    - 'cannot_refund': Explain policy (delivered only) and offer escalation.
    """,
    tools=[check_order_status, process_refund, escalate_to_supervisor]
)