# variable "subnet_ids" {
#   description = "This refers to the private subnets in the vpc module"
# }
variable "lambda_function_handler" {
  description = "This is the name of the lambda function handler"
}
variable "lambda_function_name" {
  description = "This is the name of the lambda function"
}
  
variable "lambda_memory_size" {
  description = "This specifies the amount of memory allocated to the lambda function "
}
variable "lambda_runtime" {
  description = "It specifies the runtime that runs the lambda function's handler methodgit commit"
}

variable "tags" {
  description = "Tags for resources"
}

variable "env_vars" {
 
}
variable "source_code_file_location" {
  
}
variable "timeout" {
  
}
variable "schedule_rate" {
  default = "rate(5 minutes)"
}