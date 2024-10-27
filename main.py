from fastapi import FastAPI, UploadFile, File, HTTPException
import boto3
import os
import aws_utility
import transaction_processor


app = FastAPI()

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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)