import json
import os
import boto3
import datetime as dt
from datetime import date
import datetime
import time
from dateutil.tz import tzlocal
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    iam = boto3.client('iam')
    sns = boto3.client('sns')
    users = iam.list_users()
    sns_arn = "Place your sns topic arn here"

    defaulter_users_75_days = [["Please send an email to the mentioned IAM Users and ask them to rotate the Access Keys."]]
    defaulter_users_82_days = [["Please send an email to the mentioned IAM Users and ask them to rotate the Access Keys."]]

    for user in users['Users']:
        access_keys = iam.list_access_keys(UserName=user['UserName'])

        for key in access_keys['AccessKeyMetadata']:
            today_date = datetime.date.today()
            code_date = key['CreateDate']
            age_of_key = (today_date - code_date.date()).days

            if ( age_of_key == 75 ):
                users_data = []
                users_data.append(user['UserName'])
                users_data.append(key['AccessKeyId'])
                users_data.append(age_of_key)
                defaulter_users_75_days.append(users_data)

            if ( age_of_key == 82 ):
                users_data = []
                users_data.append(user['UserName'])
                users_data.append(key['AccessKeyId'])
                users_data.append(age_of_key)
                defaulter_users_82_days.append(users_data)

    json_string_75_days = json.dumps(defaulter_users_75_days)
    json_string_82_days = json.dumps(defaulter_users_82_days)


    if ( len(defaulter_users_75_days) > 1 ):
        print(json_string_75_days)
        response_1 = sns.publish(TopicArn=sns_arn,Message=json_string_75_days,Subject='IAM Users with Access Keys older than 75 days')

    if ( len(defaulter_users_82_days) > 1 ):
        print(json_string_82_days)
        response_2 = sns.publish(TopicArn=sns_arn,Message=json_string_82_days,Subject='IAM Users with Access Keys older than 82 days')

    if ( len(defaulter_users_75_days) == 1 ) and ( len(defaulter_users_82_days) == 1 ):
        print("There is no IAM User whose Access Key is older than 75 or 82 days.")


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }




