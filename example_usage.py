"""Example usage for SQL Read-Only Guardrail."""
from client import SQLReadOnlyGuardrail

if __name__ == "__main__":
    q1 = "SELECT id, email FROM accounts WHERE status = 'active' LIMIT 25"
    print("Query 1 Check:", SQLReadOnlyGuardrail.validate_query(q1))
    q2 = "DELETE FROM accounts WHERE id = 10"
    print("Query 2 Check:", SQLReadOnlyGuardrail.validate_query(q2))
