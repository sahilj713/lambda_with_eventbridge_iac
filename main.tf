module "lambda" {
  source= "./modules/lambda"
  for_each = var.lambda_functions
  lambda_function_handler = var.lambda_function_handler
  lambda_memory_size = var.lambda_memory_size
  timeout = var.lambda_timeout
  lambda_runtime = var.lambda_runtime
  schedule_rate = each.value.schedule_rate
  source_code_file_location = "${path.root}/${trimsuffix("${each.value.source_code_file_location}","py")}zip"
  lambda_function_name = each.key
  tags = each.value.tags
  env_vars = each.value.env_vars
}

data "archive_file" "notifier_package" {
  for_each = var.lambda_functions
  type        = "zip"
  source_file = "${path.root}/${each.value.source_code_file_location}"
  output_path = "${path.root}/${trimsuffix("${each.value.source_code_file_location}","py")}zip"
}


