from fastapi import FastAPI, UploadFile, File, HTTPException
import boto3        # AWS SDK
import os
import aws_utility        #custom import
import transaction_processor    #custom import
from langchain import OpenAI
import pymysql


app = FastAPI()

# Database configuration variables
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# Initialize the LLM
llm = OpenAI(temperature=0.5)


s3_client=boto3.client('s3')
BUCKET_NAME=os.getenev("ERROR_BUCKET")


@app.post("/api/transactions/upload")
async def upload_transaction_file(file: UploadFile = File(...)):
    try:
        # Upload the file to S3
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        
        # Optionally trigger processing logic
        # transaction_processor.process_file(file.filename)
        
        return {"message": "File uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Example query: "Get the total revenue for all products sold in the last month"
@app.post("/api/queries")
async def query_data(query: str):
    try:
        # Convert natural language query to SQL
        structured_query = llm.run(f"Convert the following query into SQL: {query}")

        # Establish a database connection
        connection = pymysql.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            db=DATABASE_NAME
        )

        # Execute the structured query and fetch results
        with connection.cursor() as cursor:
            cursor.execute(structured_query)
            results = cursor.fetchall()

        # Format results for response
        response = [{"product_name": row[0], "quantity": row[1], "amount": row[2], "revenue": row[3]} for row in results]
        
        return {"results": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
