# src/utils/validators.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from .logger import setup_logger
from .error_handlers import ValidationError

logger = setup_logger(__name__)

class Validator:
    @staticmethod
    def validate_state(state: Dict[str, Any]) -> bool:
        """Validate the state structure and data types"""
        required_keys = ["messages", "current_task", "metrics", "timestamp"]
        
        try:
            # Check required keys
            for key in required_keys:
                if key not in state:
                    raise ValidationError(
                        message=f"Missing required key: {key}",
                        error_code="INVALID_STATE_STRUCTURE"
                    )
            
            # Validate timestamp
            if not isinstance(state["timestamp"], datetime):
                raise ValidationError(
                    message="Invalid timestamp format",
                    error_code="INVALID_TIMESTAMP"
                )
            
            return True
            
        except Exception as e:
            logger.error(f"State validation failed: {str(e)}")
            raise

    @staticmethod
    def validate_metrics(metrics: Dict[str, Any]) -> bool:
        """Validate metrics data structure and values"""
        required_categories = [
            "patient_flow",
            "resources",
            "quality",
            "staffing"
        ]
        
        try:
            # Check required categories
            for category in required_categories:
                if category not in metrics:
                    raise ValidationError(
                        message=f"Missing required metrics category: {category}",
                        error_code="INVALID_METRICS_STRUCTURE"
                    )
            
            # Validate numeric values
            Validator._validate_numeric_values(metrics)
            
            return True
            
        except Exception as e:
            logger.error(f"Metrics validation failed: {str(e)}")
            raise

    @staticmethod
    def validate_tool_input(
        tool_name: str,
        params: Dict[str, Any],
        required_params: List[str]
    ) -> bool:
        """Validate input parameters for tools"""
        try:
            # Check required parameters
            for param in required_params:
                if param not in params:
                    raise ValidationError(
                        message=f"Missing required parameter: {param}",
                        error_code="MISSING_PARAMETER",
                        details={"tool": tool_name, "parameter": param}
                    )
            
            return True
            
        except Exception as e:
            logger.error(f"Tool input validation failed: {str(e)}")
            raise

    @staticmethod
    def validate_department_data(department_data: Dict[str, Any]) -> bool:
        """Validate department-specific data"""
        required_fields = [
            "capacity",
            "current_occupancy",
            "staff_count"
        ]
        
        try:
            # Check required fields
            for field in required_fields:
                if field not in department_data:
                    raise ValidationError(
                        message=f"Missing required field: {field}",
                        error_code="INVALID_DEPARTMENT_DATA"
                    )
            
            # Validate capacity constraints
            if department_data["current_occupancy"] > department_data["capacity"]:
                raise ValidationError(
                    message="Current occupancy exceeds capacity",
                    error_code="INVALID_OCCUPANCY"
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Department data validation failed: {str(e)}")
            raise

    @staticmethod
    def _validate_numeric_values(data: Dict[str, Any], path: str = "") -> None:
        """Recursively validate numeric values in nested dictionary"""
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            if isinstance(value, (int, float)):
                if value < 0:
                    raise ValidationError(
                        message=f"Negative value not allowed: {current_path}",
                        error_code="INVALID_NUMERIC_VALUE"
                    )
            elif isinstance(value, dict):
                Validator._validate_numeric_values(value, current_path)# Input validation utilities implementation
