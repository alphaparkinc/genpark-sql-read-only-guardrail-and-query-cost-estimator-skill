"""MCP server for SQL Read-Only Guardrail."""
import sys
import json
from client import SQLReadOnlyGuardrail

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "validate_sql_query",
                "description": "Enforces read-only SQL execution and estimates query cost tier",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sql": {"type": "string"}
                    },
                    "required": ["sql"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "validate_sql_query":
            sql = params.get("arguments", {}).get("sql", "")
            res = SQLReadOnlyGuardrail.validate_query(sql)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
