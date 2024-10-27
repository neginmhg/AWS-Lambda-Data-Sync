## Natural Language Queries

### Overview
The **Natural Language Queries** feature allows users to interact with the data stored in the database using natural language. This functionality leverages LangChain's language model to interpret user queries and convert them into structured SQL queries, enabling a more intuitive way to retrieve information.

### API Endpoint
- **Endpoint**: `/api/queries`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "query": "string"  // A natural language query to be interpreted.
  }
  ```

#### Example Request
To retrieve the total revenue for all products sold in the last month, you can send a request as follows:
```bash
curl -X POST "http://127.0.0.1:8000/api/queries" -H "Content-Type: application/json" -d '{"query": "Get the total revenue for all products sold in the last month"}'
```

#### Response
The API will return a JSON object containing the results of the query:
```json
{
  "results": [
    {
      "product_name": "Zara T-Shirt",
      "quantity": 10,
      "amount": 200.00,
      "revenue": 2000.00
    },
    {
      "product_name": "Zara Jeans",
      "quantity": 5,
      "amount": 150.00,
      "revenue": 750.00
    }
  ]
}
```

### Usage
1. **Make a POST request** to the `/api/queries` endpoint with your natural language query.
2. **Receive the structured data** in response, formatted as a JSON object.

### Requirements
Ensure that LangChain is installed in your environment. Add it to your `requirements.txt`:
```plaintext
langchain
```
