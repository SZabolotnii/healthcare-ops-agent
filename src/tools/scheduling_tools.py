# src/tools/scheduling_tools.py
#from typing import Dict, List, Optional
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from langchain_core.tools import tool
from datetime import datetime, timedelta
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class SchedulingTools:
    @tool
    def optimize_staff_schedule(
        self,
        staff_availability: List[Dict],
        department_needs: Dict[str, Dict],
        shift_preferences: Optional[List[Dict]] = None
    ) -> Dict:
        """Generate optimized staff schedules based on availability and department needs"""
        try:
            schedule = {
                "shifts": {},
                "coverage_gaps": [],
                "recommendations": [],
                "staff_assignments": {}
            }
            
            # Process each department's needs
            for dept, needs in department_needs.items():
                schedule["shifts"][dept] = {
                    "morning": [],
                    "afternoon": [],
                    "night": []
                }
                
                required_staff = needs.get("required_staff", {})
                
                # Match available staff to shifts
                for staff in staff_availability:
                    if staff["department"] == dept and staff["available"]:
                        preferred_shift = "morning"  # Default
                        if shift_preferences:
                            for pref in shift_preferences:
                                if pref["staff_id"] == staff["id"]:
                                    preferred_shift = pref["preferred_shift"]
                        
                        schedule["shifts"][dept][preferred_shift].append(staff["id"])
                
                # Identify coverage gaps
                for shift in ["morning", "afternoon", "night"]:
                    required = required_staff.get(shift, 0)
                    assigned = len(schedule["shifts"][dept][shift])
                    
                    if assigned < required:
                        schedule["coverage_gaps"].append({
                            "department": dept,
                            "shift": shift,
                            "shortage": required - assigned
                        })
            
            return schedule
            
        except Exception as e:
            logger.error(f"Error optimizing staff schedule: {str(e)}")
            raise

    @tool
    def analyze_workforce_metrics(
        self,
        staff_data: List[Dict],
        time_period: str
    ) -> Dict:
        """Analyze workforce metrics including overtime, satisfaction, and skill mix"""
        try:
            analysis = {
                "workforce_metrics": {
                    "total_staff": len(staff_data),
                    "overtime_hours": 0,
                    "skill_distribution": {},
                    "satisfaction_score": 0,
                    "turnover_rate": 0
                },
                "recommendations": []
            }
            
            total_satisfaction = 0
            total_overtime = 0
            
            for staff in staff_data:
                # Analyze overtime
                total_overtime += staff.get("overtime_hours", 0)
                
                # Track skill distribution
                role = staff.get("role", "unknown")
                analysis["workforce_metrics"]["skill_distribution"][role] = \
                    analysis["workforce_metrics"]["skill_distribution"].get(role, 0) + 1
                
                # Track satisfaction
                total_satisfaction += staff.get("satisfaction_score", 0)
            
            # Calculate averages
            if staff_data:
                analysis["workforce_metrics"]["overtime_hours"] = total_overtime / len(staff_data)
                analysis["workforce_metrics"]["satisfaction_score"] = \
                    total_satisfaction / len(staff_data)
            
            # Generate recommendations
            if analysis["workforce_metrics"]["overtime_hours"] > 10:
                analysis["recommendations"].append("Reduce overtime hours through better scheduling")
            
            if analysis["workforce_metrics"]["satisfaction_score"] < 7:
                analysis["recommendations"].append("Implement staff satisfaction improvement measures")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing workforce metrics: {str(e)}")
            raise

    @tool
    def calculate_staffing_needs(
        self,
        patient_census: Dict[str, int],
        acuity_levels: Dict[str, float],
        staff_ratios: Dict[str, float]
    ) -> Dict:
        """Calculate staffing needs based on patient census and acuity"""
        try:
            staffing_needs = {
                "required_staff": {},
                "current_gaps": {},
                "recommendations": []
            }
            
            for department, census in patient_census.items():
                # Calculate base staffing need
                acuity = acuity_levels.get(department, 1.0)
                ratio = staff_ratios.get(department, 4)  # default 1:4 ratio
                
                required_staff = ceil(census * acuity / ratio)
                
                staffing_needs["required_staff"][department] = {
                    "total_needed": required_staff,
                    "acuity_factor": acuity,
                    "patient_ratio": ratio
                }
                
                # Generate staffing recommendations
                if required_staff > current_staff.get(department, 0):
                    staffing_needs["recommendations"].append({
                        "department": department,
                        "action": "increase_staff",
                        "amount": required_staff - current_staff.get(department, 0)
                    })
            
            return staffing_needs
            
        except Exception as e:
            logger.error(f"Error calculating staffing needs: {str(e)}")
            raise# scheduling_tools implementation
