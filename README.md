# fastapi

[Edit in StackBlitz next generation editor ⚡️](https://stackblitz.com/~/github.com/zinxon/fastapi)

# MoonReader API

A FastAPI-based microservice for managing MoonReader highlights with PostgreSQL storage.

## Features

- ✨ Async API endpoints using FastAPI
- 🗃️ PostgreSQL database integration
- 📝 CRUD operations for highlights
- 🔐 Token-based authentication
- 📁 File-based storage backup
- 🧪 Comprehensive test suite

## Prerequisites

- Python 3.8+
- PostgreSQL
- Poetry (recommended) or pip

## Installation

1. Clone the repository:

```bash
git clone git@github.com:zinxon/fastapi.git moonreader-api
cd moonreader-api
```

2. Create and activate virtual environment & install dependencies:

```bash
python3 -m venv fastapi
source fastapi/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```
APP_ENV=development
LOG_LEVEL=debug
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
MOONREADER_TOKEN=your_moonreader_token_here
```

4. Initialize the database:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Build docker image:

```bash
docker build -t fastapi-app .
```

6. Run docker container:

```bash
docker run -p 8000:8000 fastapi-app
# docker run -p 8000:8000 -w /app/src fastapi-app
```

## Running the Application (Local)

Start the development server:

```bash
python3 src/main.py
```

The API will be available at `http://localhost:8000`

## Build the container for AWS Lambda

Now we can build the container for AWS Lambda which will use the Mangum handler. We use another Dockerfile which will use a base image provided by AWS :

```bash
docker build -t zinxon/fastapi:latest . -f Dockerfile.aws.lambda
```

## Run the AWS Lambda container for local test

Let's start the container to test the lambda locally :

```bash
docker run -p 9000:8080 zinxon/fastapi:latest
```

### Test the Lambda

We send the input event that the lambda would receive from the API Gateway with the following command :

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
"resource": "/",
"path": "/",
"httpMethod": "GET",
"headers": {
"Accept": "_/_",
"Accept-Encoding": "gzip, deflate",
"cache-control": "no-cache",
"CloudFront-Forwarded-Proto": "https",
"CloudFront-Is-Desktop-Viewer": "true",
"CloudFront-Is-Mobile-Viewer": "false",
"CloudFront-Is-SmartTV-Viewer": "false",
"CloudFront-Is-Tablet-Viewer": "false",
"CloudFront-Viewer-Country": "US",
"Content-Type": "application/json",
"headerName": "headerValue",
"Host": "gy415nuibc.execute-api.us-east-1.amazonaws.com",
"Postman-Token": "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f",
"User-Agent": "PostmanRuntime/2.4.5",
"Via": "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)",
"X-Amz-Cf-Id": "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==",
"X-Forwarded-For": "54.240.196.186, 54.182.214.83",
"X-Forwarded-Port": "443",
"X-Forwarded-Proto": "https"
},
"multiValueHeaders":{
"Accept":[
"*/*"
],
"Accept-Encoding":[
"gzip, deflate"
],
"cache-control":[
"no-cache"
],
"CloudFront-Forwarded-Proto":[
"https"
],
"CloudFront-Is-Desktop-Viewer":[
"true"
],
"CloudFront-Is-Mobile-Viewer":[
"false"
],
"CloudFront-Is-SmartTV-Viewer":[
"false"
],
"CloudFront-Is-Tablet-Viewer":[
"false"
],
"CloudFront-Viewer-Country":[
"US"
],
"":[
""
],
"Content-Type":[
"application/json"
],
"headerName":[
"headerValue"
],
"Host":[
"gy415nuibc.execute-api.us-east-1.amazonaws.com"
],
"Postman-Token":[
"9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f"
],
"User-Agent":[
"PostmanRuntime/2.4.5"
],
"Via":[
"1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)"
],
"X-Amz-Cf-Id":[
"pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A=="
],
"X-Forwarded-For":[
"54.240.196.186, 54.182.214.83"
],
"X-Forwarded-Port":[
"443"
],
"X-Forwarded-Proto":[
"https"
]
},
"queryStringParameters": {
},
"multiValueQueryStringParameters":{
},
"pathParameters": {
},
"stageVariables": {
"stageVariableName": "stageVariableValue"
},
"requestContext": {
"accountId": "12345678912",
"resourceId": "roq9wj",
"stage": "testStage",
"requestId": "deef4878-7910-11e6-8f14-25afc3e9ae33",
"identity": {
"cognitoIdentityPoolId": null,
"accountId": null,
"cognitoIdentityId": null,
"caller": null,
"apiKey": null,
"sourceIp": "192.168.196.186",
"cognitoAuthenticationType": null,
"cognitoAuthenticationProvider": null,
"userArn": null,
"userAgent": "PostmanRuntime/2.4.5",
"user": null
},
"resourcePath": "/hello/",
"httpMethod": "GET",
"apiId": "gy415nuibc"
},
"body": "{}",
"isBase64Encoded": false
}'
```

## API Endpoints

### Highlights

- `POST /highlights` - Create a new highlight
- `GET /highlights` - List all highlights
- `GET /highlights/{highlight_id}` - Get a specific highlight
- `GET /highlights/by-title/{title}` - Get highlights by book title
- `PUT /highlights/{highlight_id}` - Update a highlight
- `DELETE /highlights/{highlight_id}` - Delete a highlight

## Testing

Run the test suite:

```bash
python -m pytest tests
```

## Project Structure

```
├── src/
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # Database configuration
│   └── services/        # Business logic services
├── tests/               # Test suite
├── alembic/             # Database migrations
└── requirements.txt     # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
