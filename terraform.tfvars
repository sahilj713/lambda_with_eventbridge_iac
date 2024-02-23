lambda_function_handler = "lambda_function.lambda_handler"
lambda_memory_size = 512
lambda_runtime = "python3.10"
lambda_timeout = 3

lambda_functions= {
  DEV_environment_upscaler={
    
    source_code_file_location = "code/upscaler/lambda_function.py"
    schedule_rate = "cron(0 4 ? * MON-FRI *)"
    env_vars ={
      environment = "DEV"
    }
    tags = {
      "ENV" = "DEV"
      "Terraform" = "true"
    }
  },

  DEV_environment_downscaler={
    source_code_file_location = "code/downscaler/lambda_function.py"
    schedule_rate = "cron(0 14 ? * MON-FRI *)"
    env_vars ={
      environment = "DEV"
    }
    tags = {
      "ENV" = "DEV"
      "Terraform" = "true"
    }
  },

  UAT_environment_upscaler={
    source_code_file_location = "code/upscaler/lambda_function.py"
    schedule_rate = "cron(0 4 ? * MON-FRI *)"
    env_vars ={
      environment = "UAT"
    }
    tags = {
      "ENV" = "UAT"
      "Terraform" = "true"
    }
  },

    UAT_environment_downscaler={
    source_code_file_location = "code/downscaler/lambda_function.py"
    schedule_rate = "cron(0 14 ? * MON-FRI *)"
    env_vars ={
      environment = "UAT"
    }
    tags = {
      "ENV" = "UAT"
      "Terraform" = "true"
    }
  },

  DEMO_environment_upscaler={
    source_code_file_location = "code/upscaler/lambda_function.py"
    schedule_rate = "cron(0 4 ? * MON-FRI *)"
    env_vars ={
      environment = "DEMO"
    }
    tags = {
      "ENV" = "DEMO"
      "Terraform" = "true"
    }
  },

  DEMO_environment_downscaler={
    source_code_file_location = "code/downscaler/lambda_function.py"
    schedule_rate = "cron(0 14 ? * MON-FRI *)"
    env_vars ={
      environment = "DEMO"
    }
    tags = {
      "ENV" = "DEMO"
      "Terraform" = "true"
    }
  },  
}