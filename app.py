import boto3
import botocore.config
import json
from datetime import datetime

def blog_generate_using_bedrock(blogtopic:str)->str:
    prompt =f"""write a 200 words blog on the topic {blogtopic} """
    body = {
        "messages" : [
                        {
                            "role": "Blog Creator", 
                            "prompt":prompt
                        }
                    ],
        "max_tokens": 256,
        "top_p": 0.8,
        "temperature": 0.7
        }
    try:
        bedrock = botocore.client('bedrock-runtime',region_name='us-east-1',
                                  config=botocore.config.Config(read_timeout=300,retries={"max_attempts":1}))
        response=bedrock.invoke_model(body=json.dumps(body),modelId="ai21.jamba-instruct-v1:0")
        response_content = response.get('body').read()
        blog_data  = json.loads(response_content)
        print(blog_data)
        blog_details = blog_data["generation"]
    except Exception as e:
        print(f"{e=}")
def save_blog_details(s3_key,s3_bucket,generate_blog):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket = s3_bucket,Key=s3_key,Body=generate_blog )
        print("code saved to s3")
    except:
        print("error when saving code to s3")

def lambda_handler(event, context):
    event = json.loads(event['body'])
    blog_topic = event['blog_topic']   
    generate_blog = blog_generate_using_bedrock(blogtopic=blog_topic)

    if generate_blog:
        current_time = current_time.strftime("%H%M%S")
        s3_key = f'blog_output/{current_time}.txt'
        s3_bucket = 'awsbedrockcrse'
        save_blog_details(s3_key,s3_bucket,generate_blog)
    else: print("No blog was generated....")