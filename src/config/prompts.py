# src/config/prompts.py
PROMPTS = {
    "system": """You are an expert Healthcare Operations Management Assistant.
Your role is to optimize hospital operations through:
- Patient flow management
- Resource allocation
- Quality monitoring
- Staff scheduling

Always maintain HIPAA compliance and healthcare standards in your responses.
Base your analysis on the provided metrics and department data.""",

    "input_analyzer": """Analyze the following input and determine:
1. Primary task category (patient_flow, resource_management, quality_monitoring, staff_scheduling)
2. Required context information
3. Priority level (1-5, where 5 is highest)
4. Relevant department(s)

Current input: {input}""",

    "patient_flow": """Analyze patient flow based on:
- Current occupancy: {occupancy}%
- Waiting times: {wait_times} minutes
- Department capacity: {department_capacity}
- Admission rate: {admission_rate} per hour

Provide specific recommendations for optimization.""",

    "resource_manager": """Evaluate resource utilization:
- Equipment availability: {equipment_status}
- Supply levels: {supply_levels}
- Resource allocation: {resource_allocation}
- Budget constraints: {budget_info}

Recommend optimal resource distribution.""",

    "quality_monitor": """Review quality metrics:
- Patient satisfaction: {satisfaction_score}/10
- Care outcomes: {care_outcomes}
- Compliance rates: {compliance_rates}%
- Incident reports: {incident_count}

Identify areas for improvement.""",

    "staff_scheduler": """Optimize staff scheduling considering:
- Staff availability: {staff_available}
- Department needs: {department_needs}
- Skill mix requirements: {skill_requirements}
- Work hour regulations: {work_hours}

Provide scheduling recommendations.""",

    "output_synthesis": """Synthesize findings and provide:
1. Key insights
2. Actionable recommendations
3. Priority actions
4. Implementation timeline

Context: {context}"""
}

# Error message templates
ERROR_MESSAGES = {
    "invalid_input": "Invalid input provided. Please ensure all required information is included.",
    "processing_error": "An error occurred while processing your request. Please try again.",
    "data_validation": "Data validation failed. Please check the input format.",
    "system_error": "System error encountered. Please contact support."
}

# Response templates
RESPONSE_TEMPLATES = {
    "confirmation": "Request received and being processed. Priority level: {priority}",
    "completion": "Analysis complete. {summary}",
    "error": "Error: {error_message}. Error code: {error_code}"
}# System prompts implementation
