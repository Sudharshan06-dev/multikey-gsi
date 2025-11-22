# DynamoDB Multi-Attribute Keys Demo

A practical demonstration of how DynamoDB's multi-attribute partition and sort keys reduce schema complexity.

## Problem

When building multi-pattern query systems, you typically need multiple GSIs with different sort key structures:

```
GSI_1: PK(tenantId), SK(eventType)
GSI_2: PK(tenantId), SK(region)
GSI_3: PK(tenantId), SK(zone)
GSI_4: PK(tenantId), SK(eventType#region)
```

This creates maintenance overhead and data duplication.

## Solution

Use multi-attribute partition and sort keys to support multiple queries per GSI:

```
GSI_1: PK(tenantId + eventType), SK(region, zone, resourceId)
GSI_2: PK(tenantId + region), SK(eventType, zone, resourceId)
```

Now query by event type, region, or combinations without creating new GSIs.

## Key Insight

Instead of: "Need new query pattern? Create new GSI"

You now have: "Need new filter? Use the sort key attributes"

## Project Structure

```
dynamo_db_test/
├── audit_logs_multi_attribute.py      # New approach with multi-attribute keys
├── audit_logs_without_multi_attribute.py  # Old approach (concatenated keys)
└── dynamo_instance.py                 # DynamoDB connection

main.py                                # Demo script (generates demo_results.md)
```

## Running the Demo

```bash
python main.py
```

This generates `demo_results.md` showing before/after comparisons.

## Example: Audit Logs

**Old Approach:** `eventType#region#zone#resourceId` concatenated in one field

**New Approach:** Separate `eventType`, `region`, `zone`, `resourceId` attributes

**Benefit:** Query by any combination without adding new GSIs

## GSI Design Pattern

For multi-access-pattern systems:

| Query Pattern | GSI | Partition Key | Sort Key |
|---|---|---|---|
| By event type | GSI_1 | tenantId + eventType | region, zone, timestamp |
| By region | GSI_2 | tenantId + region | eventType, zone, timestamp |
| Both | Either | Use sort key filtering | - |

## When to Use

- Audit logs
- Event streams
- Analytics tables
- Any system with 3+ query patterns

## Files

- `audit_logs_multi_attribute.py` - Correct implementation with 2 GSIs
- `audit_logs_without_multi_attribute.py` - Old approach with root table where sort key is concatenated using '#' seperator
- `main.py` - Generates demo output
- `demo_results.md` - Query results comparison

## Key Takeaway

Multi-attribute keys reduce GSI complexity by letting you filter on sort key attributes instead of creating new indices for each query pattern.

Same flexibility. Fewer GSIs.
