import boto3
import json


class Notifications:

    def publish_notification(self, sns_topic, json_message):
        sns_client = boto3.client("sns",
                                  region_name="us-east-1",
                                  aws_access_key_id='AKIA5RBIT6FSU6YXRCFH',
                                  aws_secret_access_key='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')
        res = sns_client.publish(
            TopicArn= sns_topic,
            Message = json.dumps(json_message, indent=2, default=str),
            Subject = 'Something Happened'
        )
        print("publish_notification response = ",
              json.dumps(res, indent=2, default=str))

    def check_publish(self, request, response):
        if request.method in ['PUT', 'POST', 'DELETE']:
            event = {
                "URL": request.url,
                "Method": request.method
            }
            print(request.json)
            if request.json:
                event["new_data"] = request.json
                self.publish_notification("arn:aws:sns:us-east-1:929945612645:course-notifications", event)