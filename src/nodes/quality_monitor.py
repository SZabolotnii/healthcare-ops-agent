# src/nodes/quality_monitor.py

from typing import Dict, List, Optional, Any
from typing_extensions import TypedDict  # If using TypedDict
from langchain_core.messages import SystemMessage
from ..models.state import HospitalState
from ..config.prompts import PROMPTS
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class QualityMonitorNode:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompt = PROMPTS["quality_monitor"]

    def __call__(self, state: HospitalState) -> Dict:
        try:
            # Get current quality metrics
            metrics = state["metrics"]["quality"]
            
            # Format prompt with current metrics
            formatted_prompt = self.system_prompt.format(
                satisfaction_score=metrics["patient_satisfaction"],
                care_outcomes=self._format_care_outcomes(metrics),
                compliance_rates=metrics["compliance_rate"] * 100,
                incident_count=metrics["incident_count"]
            )
            
            # Get LLM analysis
            response = self.llm.invoke([
                SystemMessage(content=formatted_prompt)
            ])
            
            # Process quality assessment
            analysis = self._analyze_quality_metrics(response.content, metrics)
            
            return {
                "analysis": analysis,
                "messages": [response],
                "context": {
                    "quality_scores": metrics["quality_scores"],
                    "last_audit": metrics["last_audit_date"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error in quality monitoring analysis: {str(e)}")
            raise

    def _format_care_outcomes(self, metrics: Dict) -> str:
        """Format care outcomes into readable text"""
        outcomes = []
        for metric, value in metrics["care_outcomes"].items():
            outcomes.append(f"{metric}: {value:.1f}")
        return ", ".join(outcomes)

    def _analyze_quality_metrics(self, response: str, metrics: Dict) -> Dict:
        """Analyze quality metrics and identify areas for improvement"""
        return {
            "satisfaction_analysis": self._analyze_satisfaction(metrics),
            "compliance_analysis": self._analyze_compliance(metrics),
            "incident_analysis": self._analyze_incidents(metrics),
            "recommendations": self._extract_recommendations(response),
            "priority_improvements": []
        }

    def _analyze_satisfaction(self, metrics: Dict) -> Dict:
        """Analyze patient satisfaction trends"""
        satisfaction = metrics["patient_satisfaction"]
        return {
            "current_score": satisfaction,
            "status": "Good" if satisfaction >= 8.0 else "Needs Improvement",
            "trend": "Unknown"  # Would need historical data
        }

    def _analyze_compliance(self, metrics: Dict) -> Dict:
        """Analyze compliance rates"""
        return {
            "rate": metrics["compliance_rate"],
            "status": "Compliant" if metrics["compliance_rate"] >= 0.95 else "Review Required"
        }

    def _analyze_incidents(self, metrics: Dict) -> Dict:
        """Analyze incident reports"""
        return {
            "count": metrics["incident_count"],
            "severity": "High" if metrics["incident_count"] > 5 else "Low"
        }

    def _extract_recommendations(self, response: str) -> List[str]:
        """Extract recommendations from LLM response"""
        recommendations = []
        for line in response.split('\n'):
            if 'recommend' in line.lower() or 'suggest' in line.lower():
                recommendations.append(line.strip())
        return recommendations