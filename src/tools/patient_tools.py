# src/tools/patient_tools.py
#from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from typing import Dict, List, Optional
from langchain_core.tools import tool
from datetime import datetime
from ..utils.logger import setup_logger
from ..models.state import Department

logger = setup_logger(__name__)

class PatientTools:
    @tool
    def calculate_wait_time(
        self,
        department: str,
        current_queue: int,
        staff_available: int
    ) -> float:
        """Calculate estimated wait time for a department based on queue and staff"""
        try:
            # Average time per patient (in minutes)
            AVG_TIME_PER_PATIENT = 15
            
            # Factor in staff availability
            wait_time = (current_queue * AVG_TIME_PER_PATIENT) / max(staff_available, 1)
            
            return round(wait_time, 1)
            
        except Exception as e:
            logger.error(f"Error calculating wait time: {str(e)}")
            raise

    @tool
    def analyze_bed_capacity(
        self,
        total_beds: int,
        occupied_beds: int,
        pending_admissions: int
    ) -> Dict:
        """Analyze bed capacity and provide utilization metrics"""
        try:
            capacity = {
                "total_beds": total_beds,
                "occupied_beds": occupied_beds,
                "available_beds": total_beds - occupied_beds,
                "utilization_rate": (occupied_beds / total_beds) * 100,
                "pending_admissions": pending_admissions,
                "status": "Normal"
            }
            
            # Determine status based on utilization
            if capacity["utilization_rate"] > 90:
                capacity["status"] = "Critical"
            elif capacity["utilization_rate"] > 80:
                capacity["status"] = "High"
            
            return capacity
            
        except Exception as e:
            logger.error(f"Error analyzing bed capacity: {str(e)}")
            raise

    @tool
    def predict_discharge_time(
        self,
        admission_date: datetime,
        condition_type: str,
        department: str
    ) -> datetime:
        """Predict expected discharge time based on condition and department"""
        try:
            # Average length of stay (in days) by condition
            LOS_BY_CONDITION = {
                "routine": 3,
                "acute": 5,
                "critical": 7,
                "emergency": 2
            }
            
            # Get base length of stay
            base_los = LOS_BY_CONDITION.get(condition_type.lower(), 4)
            
            # Adjust based on department
            if department.lower() == "icu":
                base_los *= 1.5
            
            # Calculate expected discharge date
            discharge_date = admission_date + timedelta(days=base_los)
            
            return discharge_date
            
        except Exception as e:
            logger.error(f"Error predicting discharge time: {str(e)}")
            raise

    @tool
    def optimize_patient_flow(
        self,
        departments: List[Department],
        waiting_patients: List[Dict]
    ) -> Dict:
        """Optimize patient flow across departments"""
        try:
            optimization_result = {
                "department_recommendations": {},
                "patient_transfers": [],
                "capacity_alerts": []
            }
            
            for dept in departments:
                # Calculate department capacity
                utilization = dept["current_occupancy"] / dept["capacity"]
                
                if utilization > 0.9:
                    optimization_result["capacity_alerts"].append({
                        "department": dept["name"],
                        "alert": "Critical capacity",
                        "utilization": utilization
                    })
                
                # Recommend transfers if needed
                if utilization > 0.85:
                    optimization_result["patient_transfers"].append({
                        "from_dept": dept["name"],
                        "recommended_transfers": max(1, int((utilization - 0.8) * dept["capacity"]))
                    })
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error optimizing patient flow: {str(e)}")
            raise

    @tool
    def assess_admission_priority(
        self,
        patient_condition: str,
        wait_time: float,
        department_load: float
    ) -> Dict:
        """Assess admission priority based on multiple factors"""
        try:
            # Base priority scores
            CONDITION_SCORES = {
                "critical": 10,
                "urgent": 8,
                "moderate": 5,
                "routine": 3
            }
            
            # Calculate priority score
            base_score = CONDITION_SCORES.get(patient_condition.lower(), 3)
            wait_factor = min(wait_time / 30, 2)  # Cap wait time factor at 2
            load_penalty = department_load if department_load > 0.8 else 0
            
            final_score = base_score + wait_factor - load_penalty
            
            return {
                "priority_score": round(final_score, 2),
                "priority_level": "High" if final_score > 7 else "Medium" if final_score > 4 else "Low",
                "factors": {
                    "condition_score": base_score,
                    "wait_factor": round(wait_factor, 2),
                    "load_penalty": round(load_penalty, 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error assessing admission priority: {str(e)}")
            raise# patient_tools implementation
