resource "aws_cloudwatch_event_rule" "event_rule" {
  name                = "${var.lambda_function_name}_er"
  description         = "Lambda EventBridge rule"
  schedule_expression = var.schedule_rate  # Adjust the cron expression as needed
}
resource "aws_cloudwatch_event_target" "func" {
  rule      = aws_cloudwatch_event_rule.event_rule.name
  target_id = "Lambda_target"
  arn       = aws_lambda_function.func.arn
}

resource "aws_lambda_permission" "example" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.func.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.event_rule.arn
}