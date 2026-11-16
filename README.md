
# Serverless Task Tracker Application (AWS)

A serverless RESTful task tracking service built using **Amazon API Gateway**, **AWS Lambda (Python/Boto3)**, and **Amazon DynamoDB** for the SOA Programming & Microservices assignment.

## Architecture Overview
- **Amazon DynamoDB (`TASKSDEMO`):** Stores task items with `TASKID` (String) as the Partition Key.
- **AWS Lambda (`TaskDemoTracker`):** Python 3.12 backend handler performing CRUD operations via Boto3.
- **IAM Role:** Configured with `AmazonDynamoDBFullAccess` for secure database interaction.
- **Amazon API Gateway (`TaskTrackerDemo`):** Exposes HTTP endpoints deployed to the `tests` stage.

## API Endpoints

| Method | Endpoint | Description | Request Body (JSON) |
| :--- | :--- | :--- | :--- |
| `POST` | `/tasks` | Create a new task | `{"TaskName": "Complete SOA Assignment", "Status": "In Progress"}` |
| `GET` | `/tasks/{id}` | Retrieve task details by `TASKID` | *None* |
| `PUT` | `/tasks/{id}` | Update status of an existing task | `{"Status": "Completed"}` |

## Sample `curl` Commands

```bash
# 1. Create a Task
curl -X POST "<YOUR_INVOKE_URL>/tasks" \
  -H "Content-Type: application/json" \
  -d '{"TaskName": "Complete SOA Assignment", "Status": "In Progress"}'

# 2. Retrieve a Task
curl -X GET "<YOUR_INVOKE_URL>/tasks/<TASKID>"

# 3. Update Task Status
curl -X PUT "<YOUR_INVOKE_URL>/tasks/<TASKID>" \
  -H "Content-Type: application/json" \
  -d '{"Status": "Completed"}'
```
