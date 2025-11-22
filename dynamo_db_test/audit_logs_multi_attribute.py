from boto3.dynamodb.conditions import Key, Attr
from dynamo_db_test.dynamo_instance import DynamoDBConnection
from typing import Dict, List


class AuditLogsMultiAttribute:
    
    def __init__(self):
        self.root_table = DynamoDBConnection.get_instance().get_table()
    
    # ============ PATTERN 1: Query by Event Type (any region) ============
    def query_table_by_event(self, tenant_id: str, event_type: str) -> List[Dict]:
        """
        Get all events of a specific type across ALL regions
        
        Uses: GSI_TenantEvent (PK: tenantId + eventType)
        Advantage: Native query, NO string parsing
        
        Before:  Would need to query by tenantId then manually filter
        After:   Direct query on event type also we can query other keys like region, zone, resourceId
        """
        
        response = self.root_table.query(
            IndexName="GSI_TenantEvent",
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                   & Key("eventType").eq(event_type)
        )
        
        items = response.get('Items', [])
        print(f"   Found {len(items)} items (Login, ModifyResource, DeleteResource across ALL regions)")
        return items

    # ============ PATTERN 2: Query by Event + Region (composite) ============
    def query_by_event_and_region(self, tenant_id: str, event_type: str, region: str) -> List[Dict]:
        """
        Get events of a specific type in a specific region
        
        Uses: GSI_TenantEvent (PK: tenantId + eventType)
        Advantage: Most specific query, distributed across partitions
        """
        
        response = self.root_table.query(
            IndexName="GSI_TenantEvent",
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                   & Key("eventType").eq(event_type)
                                   & Key("region").eq(region)
        )
        
        items = response.get('Items', [])
        print(f"   Found {len(items)} {event_type} events in {region}")
        return items

    # ============ PATTERN 3: Query by Event + Region (composite) ============
    def query_by_event_region_zone(self, tenant_id: str, event_type: str, region: str) -> List[Dict]:
        """
        Get events of a specific type in a specific region
        
        Uses: GSI_TenantEvent (PK: tenantId + eventType)
        Advantage: Most specific query, distributed across partitions
        """
       
        response = self.root_table.query(
            IndexName="GSI_TenantEvent",
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                   & Key("eventType").eq(event_type)
                                   & Key("region").eq(region) & Key('zone').eq('us-east-2a')
        )
        
        items = response.get('Items', [])
        print(f"   Found {len(items)} {event_type} events in {region}")
        return items
    
    # ============ PATTERN 4: Query by Region (any event type) ============
    def query_by_region_only(self, tenant_id: str, region: str) -> List[Dict]:
        """
        Get ALL events in a specific region (Login, ModifyResource, DeleteResource, etc.)
        
        Uses: GSI_TenantRegion (PK: tenantId + region)
        
        Now with multi-attribute PK, you have a different GSI for this pattern.
        And with multi-attribute SK, we can query event and zone
        """
        
        response = self.root_table.query(
            IndexName="GSI_TenantRegion",
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                   & Key("region").eq(region)
        )
        
        items = response.get('Items', [])
        print(f"   Found {len(items)} items (all event types in {region})")
        return items