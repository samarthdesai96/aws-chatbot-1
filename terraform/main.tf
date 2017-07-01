provider "aws" {
  profile = "${var.profile}"
  region  = "${var.region}"
}

resource "aws_lambda_function" "lambda" {
  function_name = "${var.lambda_name}"


}
