TABLE_NAME = 'product_sale_summary'
RDS_COLUMN_HEADERS = "product_name, quantity, amount, revenue, file_name"

FAILED_SNS_SUBJECT = 'Error Summarizing File'
SUCCESS_SNS_SUBJECT = 'File Summarization Successful'
