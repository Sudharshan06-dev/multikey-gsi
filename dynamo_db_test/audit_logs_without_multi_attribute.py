import boto3
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key, Attr
from dynamo_db_test.dynamo_instance import DynamoDBConnection

class AuditLogsWithoutMultiAttribute:
    
    def __init__(self):
        self.root_table = DynamoDBConnection.get_instance().get_table()
    
    def query_table_by_event(self, tenant_id: str):
        # Query all Login events for tenant_003
        table_response = self.root_table.query(
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                & Key("eventType#region#zone#resourceId").begins_with("Login"),
        )
        return table_response['Items']

    def query_by_event_and_region(self, tenant_id: str):
        # Query all Login events in US-EAST region
        table_response = self.root_table.query(
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                & Key("eventType#region#zone#resourceId").begins_with("Login#US-EAST-2"),
        )
        return table_response['Items']

    def query_by_event_region_zone(self, tenant_id: str):
        # Query all Login events in US-EAST region, us-east-2a zone
        table_response = self.root_table.query(
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                & Key("eventType#region#zone#resourceId").begins_with("Login#US-EAST-2#us-east-2a"),
        )
        return table_response['Items']

    '''
    PROBLEM HERE WHAT IF THE USER WANTS TO GET ALL THE DATA FOR PARTICULAR REGION ONLY
    '''
    def query_by_region_zone(self, tenant_id: str):
        # Query all Login events in US-EAST region
        table_response = self.root_table.query(
            KeyConditionExpression=Key("tenantId").eq(tenant_id) 
                                & Key("eventType#region#zone#resourceId").begins_with("US-EAST-2#us-east-2a"),
        )
        return table_response['Items']