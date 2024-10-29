### REST API Endpoints

1. **Upload Transaction File**
   - **Endpoint**: `POST /api/transactions/upload`
   - **Description**: Accepts a CSV file containing transaction data, uploads it to the designated S3 bucket, and triggers processing.
   - **Request Body**: `multipart/form-data` containing the file.
   - **Response**: Confirmation message with status.

2. **Get Transaction Summary**
   - **Endpoint**: `GET /api/transactions/summary`
   - **Description**: Retrieves the aggregated summary of transactions processed, possibly filtered by date range or product name.
   - **Query Parameters**:
     - `start_date`: (optional) Filter by the starting date.
     - `end_date`: (optional) Filter by the ending date.
     - `product_name`: (optional) Filter by product name.
   - **Response**: JSON object containing the transaction summary.

3. **Get All Processed Transactions**
   - **Endpoint**: `GET /api/transactions`
   - **Description**: Fetches all processed transactions from the database.
   - **Response**: JSON array of transaction records.

4. **Get Transaction by ID**
   - **Endpoint**: `GET /api/transactions/{transaction_id}`
   - **Description**: Retrieves detailed information about a specific transaction based on its unique ID.
   - **Response**: JSON object containing transaction details.

5. **Delete Transaction**
   - **Endpoint**: `DELETE /api/transactions/{transaction_id}`
   - **Description**: Deletes a specific transaction record from the database.
   - **Response**: Confirmation message with the status of the delete operation.

6. **Get Processing Status**
   - **Endpoint**: `GET /api/transactions/status`
   - **Description**: Provides the status of the last transaction processing operation (e.g., success, error).
   - **Response**: JSON object with status details.

7. **Get Error Logs**
   - **Endpoint**: `GET /api/errors`
   - **Description**: Retrieves a list of error logs generated during transaction processing for review and debugging.
   - **Response**: JSON array of error log entries.

8. **Health Check**
   - **Endpoint**: `GET /api/health`
   - **Description**: Simple health check endpoint to verify if the API is running.
   - **Response**: A message indicating the health status (e.g., "Healthy").