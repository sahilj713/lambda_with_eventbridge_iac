resource "aws_lambda_function" "func" {
    # If the file is not in the current working directory you will need to include a
    # path.module in the filename.
    filename      = var.source_code_file_location
    function_name = var.lambda_function_name
    role          = aws_iam_role.iam_for_lambda.arn
    handler       = var.lambda_function_handler
    runtime       = var.lambda_runtime
    memory_size   = var.lambda_memory_size
    timeout = var.timeout
    
    # vpc_config {
    #   subnet_ids         = var.subnet_ids
    #   security_group_ids = [aws_security_group.allow_tls.id]
    # }

      
     environment {
      
      variables = var.env_vars

      }

      tags = var.tags
       
}


