#!/usr/bin/env python3
"""
Example: Complete invoice download and extraction workflow
"""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.orchestrator import AutomationOrchestrator
from src.utils.logger import get_logger

logger = get_logger("example_invoice")


async def main():
    """Run an invoice automation example"""
    logger.info("Starting invoice automation example")

    orchestrator = AutomationOrchestrator()
    await orchestrator.initialize()

    try:
        # Create task for invoice extraction
        task_id = orchestrator.create_task(
            objective="""
                Navigate to the accounting dashboard at https://accounting.example.com
                Log in with provided credentials
                Navigate to the Invoices section
                Download the most recent invoice PDF
                Wait for download to complete
                Extract vendor name, invoice number, and total amount
                Output results as structured JSON
            """,
            params={
                "extraction_schema": {
                    "vendor_name": "Name of vendor/company",
                    "invoice_number": "Invoice reference number",
                    "invoice_date": "Date issued",
                    "due_date": "Payment due date",
                    "total_amount": "Total amount in currency",
                    "line_items": "List of purchased items",
                }
            },
        )

        logger.info(f"Created invoice task: {task_id}")

        # Execute task
        result = await orchestrator.execute_task(task_id)

        logger.info(f"Result: {json.dumps(result, indent=2)}")

        # Retrieve extracted data
        task = orchestrator.tasks[task_id]
        if task.extracted_data:
            logger.info("Extracted data:")
            for filename, data in task.extracted_data.items():
                logger.info(f"  {filename}: {json.dumps(data, indent=2)}")

        # Get audit log for compliance
        audit_log = orchestrator.get_task_audit_log(task_id)
        if audit_log:
            logger.info(f"Audit log: {len(audit_log)} entries")

    finally:
        await orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
