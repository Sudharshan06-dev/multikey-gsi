from dynamo_db_test.audit_logs_multi_attribute import AuditLogsMultiAttribute
from dynamo_db_test.audit_logs_without_multi_attribute import AuditLogsWithoutMultiAttribute
from typing import List, Dict
import json


def main():
    with open('demo_results.md', 'w', encoding='utf-8') as f:
        
        def write_header(title: str):
            f.write(f"# {title}\n\n")
        
        def write_subheader(title: str):
            f.write(f"## {title}\n\n")
        
        def write_results(items: List[Dict]):
            if not items:
                f.write("No results found\n\n")
                return
            
            f.write(f"Found {len(items)} result(s):\n\n")
            for idx, item in enumerate(items, 1):
                f.write("```json\n")
                f.write(json.dumps(item, indent=2) + "\n")
                f.write("```\n\n")
        
        # Write title
        write_header("DynamoDB Multi-Attribute Keys Demo")
        f.write("Comparison: How multi-attribute keys reduce GSI complexity\n\n")
        
        # OLD APPROACH
        write_header("OLD APPROACH: Concatenated Keys")
        f.write("Problem: `eventType#region#zone#resourceId`\n\n")
        
        audit_old = AuditLogsWithoutMultiAttribute()
        
        write_subheader("Query 1: Get all Login events")
        items = audit_old.query_table_by_event("tenant_003")
        write_results(items)
        
        write_subheader("Query 2: Get Login events in US-EAST-2")
        items = audit_old.query_by_event_and_region("tenant_003")
        write_results(items)
        
        write_subheader("Query 3: Get Login events in US-EAST-2, us-east-2a")
        items = audit_old.query_by_event_region_zone("tenant_003")
        write_results(items)
        
        write_subheader("Limitations")
        f.write("- Can't query just by region without event type\n")
        f.write("- Need different GSI for each query pattern\n")
        f.write("- If format changes, must backfill entire table\n\n")
        
        # NEW APPROACH
        write_header("NEW APPROACH: Multi-Attribute Keys")
        f.write("Design: `PK(tenantId + eventType)`, `SK(region, zone, resourceId)`\n\n")
        
        audit_new = AuditLogsMultiAttribute()
        
        write_subheader("Query 1: Get all Login events")
        items = audit_new.query_table_by_event("tenant_003", "Login")
        write_results(items)
        
        write_subheader("Query 2: Get Login events in US-EAST-2")
        items = audit_new.query_by_event_and_region("tenant_003", "Login", "US-EAST-2")
        write_results(items)
        
        write_subheader("Query 3: Get Login events in US-EAST-2, us-east-2a")
        items = audit_new.query_by_event_region_zone("tenant_003", "Login", "US-EAST-2")
        write_results(items)
        f.write("**Benefit:** Used sort keys (region, zone) without new GSI\n\n")
        
        write_subheader("Query 4: Get ALL events in US-EAST-2 (any type)")
        f.write("Using different GSI: `PK(tenantId + region)`, `SK(eventType, zone, resourceId)`\n\n")
        items = audit_new.query_by_region_only("tenant_003", "US-EAST-2")
        write_results(items)
        
        # COMPARISON
        write_header("COMPARISON: Old vs New")
        
        write_subheader("Old Approach")
        f.write("```\n")
        f.write("GSI_1: PK(tenantId), SK(eventType)\n")
        f.write("GSI_2: PK(tenantId), SK(region)\n")
        f.write("GSI_3: PK(tenantId), SK(zone)\n")
        f.write("GSI_4: PK(tenantId), SK(eventType#region)\n")
        f.write("Total: 4 GSIs for 4 query patterns\n")
        f.write("```\n\n")
        
        write_subheader("New Approach")
        f.write("```\n")
        f.write("GSI_1: PK(tenantId + eventType), SK(region, zone, resourceId)\n")
        f.write("GSI_2: PK(tenantId + region), SK(eventType, zone, resourceId)\n")
        f.write("Total: 2 GSIs for multiple query patterns\n")
        f.write("```\n\n")
        
        write_subheader("Key Differences")
        f.write("- Old: Each query pattern = different GSI\n")
        f.write("- New: Use sort key attributes to filter without new GSIs\n")
        f.write("- New: Query eventType + region? Use GSI_1's sort key 'region'\n")
        f.write("- New: Query region + eventType? Use GSI_2's sort key 'eventType'\n\n")
        
        # KEY INSIGHT
        write_header("Key Insight")
        f.write("The real win: Multi-attribute sort keys let you filter by multiple attributes without creating new GSIs.\n\n")
        f.write("- **Old mindset:** Need new query pattern? Create new GSI\n")
        f.write("- **New mindset:** Need new filter? Use the sort key attributes\n\n")
        
        print("Results written to demo_results.md")


if __name__ == "__main__":
    main()