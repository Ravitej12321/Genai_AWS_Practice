import json
import boto3
import botocore

prompt_data  = '''Act as a Psychologist and give suggestion for better mental health in 100 words.'''

bedrock = boto3.client(service_name = 'bedrock-runtime')

payload =  {
                "messages":[{"role":"user","content":prompt_data}],
                "max_tokens":256,
                "temperature":0.5,
                "top_p":0.9
            }

model_id='ai21.jamba-instruct-v1:0'
body = json.dumps(payload)
response = bedrock.invoke_model(
        body=body,

        modelId=model_id,
        contentType= "application/json",
        accept= "application/json",

)
response_body = json.loads(response.get('body').read())

# response_text_body = response_body.get('choices')?
message_content = response_body['choices'][0]['message']['content']
print(message_content)

### Hurray! i am able to access the foundation model using aws bedrock.


