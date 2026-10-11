"""SQL Read-Only Guardrail & Query Cost Estimator.
100% Python Standard Library.
"""

import re

class SQLReadOnlyGuardrail:
    """Validates SQL queries for strict read-only execution and flags high-cost query antipatterns."""
    
    MUTATION_KEYWORDS = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "EXEC"]
    
    @classmethod
    def validate_query(cls, sql: str) -> dict:
        sql_upper = sql.upper()
        for kw in cls.MUTATION_KEYWORDS:
            if re.search(rf"\b{kw}\b", sql_upper):
                return {
                    "safe_to_execute": False,
                    "violation": f"Prohibited mutation keyword detected: {kw}",
                    "estimated_cost_tier": "BLOCKED"
                }
                
        warnings = []
        cost_score = 10
        if "SELECT *" in sql_upper:
            warnings.append("Unbounded 'SELECT *' increases I/O payload")
            cost_score += 25
        if "JOIN" in sql_upper and "ON " not in sql_upper and "USING" not in sql_upper:
            warnings.append("Potential Cartesian product (JOIN without ON/USING clause)")
            cost_score += 60
        if "LIMIT" not in sql_upper:
            warnings.append("Missing LIMIT clause on SELECT query")
            cost_score += 20
            
        tier = "HIGH" if cost_score >= 60 else ("MEDIUM" if cost_score >= 30 else "LOW")
        return {
            "safe_to_execute": cost_score < 80,
            "estimated_cost_score": cost_score,
            "estimated_cost_tier": tier,
            "optimization_warnings": warnings
        }
