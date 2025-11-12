{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"dynamodb:UpdateItem",
				"dynamodb:GetItem"
			],
			"Resource": "arn:aws:dynamodb:us-east-2:<account-id>:table/awsCloudResumeChallange"
		}
	]
}

#permissoin to access lambda to access dynamodb table