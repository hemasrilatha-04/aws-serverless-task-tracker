import json
import uuid
from datetime import datetime, timezone
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TASKSDEMO')

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod')
    path_params = event.get('pathParameters') or {}
    task_id = path_params.get('id')

    try:
        # 1. Create a Task (POST /tasks)
        if http_method == 'POST':
            body = json.loads(event.get('body') or '{}')
            task_name = body.get('TaskName')
            if not task_name:
                return response(400, {'error': 'Please provide TaskName'})

            new_id = str(uuid.uuid4())
            created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            status = body.get('Status', 'Pending')

            item = {
                'TASKID': new_id,
                'TaskName': task_name,
                'Status': status,
                'CreatedAt': created_at
            }
            table.put_item(Item=item)
            return response(201, {'message': 'Task added!', 'task': item})

        # 2. Retrieve a Task by ID (GET /tasks/{id})
        elif http_method == 'GET' and task_id:
            res = table.get_item(Key={'TASKID': task_id})
            item = res.get('Item')
            if not item:
                return response(404, {'error': 'Task not found'})
            return response(200, item)

        # 3. Update Task Status (PUT /tasks/{id})
        elif http_method == 'PUT' and task_id:
            body = json.loads(event.get('body') or '{}')
            new_status = body.get('Status')
            if not new_status:
                return response(400, {'error': 'Please provide Status'})

            res = table.update_item(
                Key={'TASKID': task_id},
                UpdateExpression='SET #s = :val',
                ExpressionAttributeNames={'#s': 'Status'},
                ExpressionAttributeValues={':val': new_status},
                ReturnValues='ALL_NEW'
            )
            return response(200, {'message': 'Status updated!', 'updated_task': res.get('Attributes')})

        else:
            return response(400, {'error': 'Invalid request'})

    except Exception as e:
        return response(500, {'error': str(e)})

def response(code, body):
    return {
        'statusCode': code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }
