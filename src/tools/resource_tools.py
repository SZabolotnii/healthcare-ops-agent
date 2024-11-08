# src/tools/resource_tools.py
#from typing import Dict, List
from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from langchain_core.tools import tool
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ResourceTools:
    @tool
    def analyze_supply_levels(
        self,
        current_inventory: Dict[str, float],
        consumption_rate: Dict[str, float],
        reorder_thresholds: Dict[str, float]
    ) -> Dict:
        """Analyze supply levels and generate reorder recommendations"""
        try:
            analysis = {
                "critical_items": [],
                "reorder_needed": [],
                "adequate_supplies": [],
                "recommendations": []
            }
            
            for item, level in current_inventory.items():
                threshold = reorder_thresholds.get(item, 0.2)
                consumption = consumption_rate.get(item, 0)
                
                # Days of supply remaining
                days_remaining = level / consumption if consumption > 0 else float('inf')
                
                if level <= threshold:
                    if days_remaining < 2:
                        analysis["critical_items"].append({
                            "item": item,
                            "current_level": level,
                            "days_remaining": days_remaining
                        })
                    else:
                        analysis["reorder_needed"].append({
                            "item": item,
                            "current_level": level,
                            "days_remaining": days_remaining
                        })
                else:
                    analysis["adequate_supplies"].append(item)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing supply levels: {str(e)}")
            raise

    @tool
    def track_equipment_utilization(
        self,
        equipment_logs: List[Dict],
        equipment_capacity: Dict[str, int]
    ) -> Dict:
        """Track and analyze equipment utilization rates"""
        try:
            utilization = {
                "equipment_stats": {},
                "underutilized": [],
                "optimal": [],
                "overutilized": []
            }
            
            for equip, capacity in equipment_capacity.items():
                usage = len([log for log in equipment_logs if log["equipment"] == equip])
                utilization_rate = usage / capacity
                
                utilization["equipment_stats"][equip] = {
                    "usage": usage,
                    "capacity": capacity,
                    "utilization_rate": utilization_rate
                }
                
                if utilization_rate < 0.3:
                    utilization["underutilized"].append(equip)
                elif utilization_rate > 0.8:
                    utilization["overutilized"].append(equip)
                else:
                    utilization["optimal"].append(equip)
            
            return utilization
            
        except Exception as e:
            logger.error(f"Error tracking equipment utilization: {str(e)}")
            raise

    @tool
    def optimize_resource_allocation(
        self,
        department_demands: Dict[str, Dict],
        available_resources: Dict[str, int]
    ) -> Dict:
        """Optimize resource allocation across departments"""
        try:
            allocation = {
                "recommended_distribution": {},
                "unmet_demands": [],
                "resource_sharing": []
            }
            
            total_demand = sum(dept["demand"] for dept in department_demands.values())
            
            for dept, demand in department_demands.items():
                # Calculate fair share based on demand
                for resource, available in available_resources.items():
                    dept_share = int((demand["demand"] / total_demand) * available)
                    
                    allocation["recommended_distribution"][dept] = {
                        resource: dept_share
                    }
                    
                    if dept_share < demand.get("minimum", 0):
                        allocation["unmet_demands"].append({
                            "department": dept,
                            "resource": resource,
                            "shortfall": demand["minimum"] - dept_share
                        })
            
            return allocation
            
        except Exception as e:
            logger.error(f"Error optimizing resource allocation: {str(e)}")
            raise# resource_tools implementation
