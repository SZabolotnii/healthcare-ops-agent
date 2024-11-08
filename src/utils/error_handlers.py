# src/utils/error_handlers.py
from typing import Dict, Any, Optional, Callable
from functools import wraps
import traceback
from .logger import setup_logger

logger = setup_logger(__name__)

class HealthcareError(Exception):
    """Base exception class for healthcare operations"""
    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(HealthcareError):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="INPUT_VALIDATION_ERROR",
            details=details
        )

class ProcessingError(HealthcareError):
    """Raised when processing operations fail"""
    pass

class ResourceError(HealthcareError):
    """Raised when resource-related operations fail"""
    pass

class ErrorHandler:
    @staticmethod
    def validate_input(input_text: str) -> None:
        """Validate input text before processing"""
        if not input_text or not input_text.strip():
            raise ValidationError(
                message="Input text cannot be empty",
                details={"provided_input": input_text}
            )

    @staticmethod
    def handle_error(error: Exception) -> Dict[str, Any]:
        """Handle different types of errors and return appropriate response"""
        if isinstance(error, ValidationError):
            logger.error(f"Validation Error: {error.message}", 
                        extra={"error_code": error.error_code, "details": error.details})
            raise error  # Re-raise ValidationError
        elif isinstance(error, HealthcareError):
            logger.error(f"Healthcare Error: {error.message}", 
                        extra={"error_code": error.error_code, "details": error.details})
            return {
                "error": True,
                "error_code": error.error_code,
                "message": error.message,
                "details": error.details
            }
        else:
            logger.error(f"Unexpected Error: {str(error)}\n{traceback.format_exc()}")
            return {
                "error": True,
                "error_code": "UNEXPECTED_ERROR",
                "message": "An unexpected error occurred",
                "details": {"error_type": type(error).__name__}
            }

    @staticmethod
    def error_decorator(func: Callable) -> Callable:
        """Decorator for handling errors in functions"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError:
                # Let ValidationError propagate up
                raise
            except Exception as e:
                return ErrorHandler.handle_error(e)
        return wrapper
    
    @staticmethod
    def retry_operation(
        operation: Callable,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> Any:
        """
        Retry an operation with exponential backoff
        """
        from time import sleep
        
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                logger.warning(
                    f"Operation failed (attempt {attempt + 1}/{max_retries}): {str(e)}"
                )
                sleep(retry_delay * (2 ** attempt))

    @staticmethod
    def safe_execute(
        operation: Callable,
        error_code: str,
        default_value: Any = None
    ) -> Any:
        """
        Safely execute an operation with error handling
        """
        try:
            return operation()
        except Exception as e:
            logger.error(f"Operation failed: {str(e)}")
            raise HealthcareError(
                message=f"Operation failed: {str(e)}",
                error_code=error_code
            )# Error handling utilities implementation
