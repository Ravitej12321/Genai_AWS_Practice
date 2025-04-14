import json
import boto3

prompt = "What is the Capital of India?"

bedrock = boto3.client('bedrock-runtime')

payload = json.dumps({
                "inputText":prompt,
                "dimensions":512,
                "normalize":True
                })
"""{
 "modelId": "amazon.titan-embed-text-v2:0",
 "contentType": "application/json",
 "accept": "*/*",
 "body": "{\"inputText\":\"this is where you place your input text\", \"dimensions\": 512, \"normalize\": true}"
}"""
model_id = "amazon.titan-embed-text-v2:0"
response  = bedrock.invoke_model(

        modelId = model_id,
        body= payload,
        contentType='application/json',
        accept="*/*"
)
respnse_body = json.loads(response['body'].read())
print('embedding_vectors for the prompt is ',respnse_body.get('embedding'))

#### Hurray !!!! I have acheived to create the embeddings using the aws embedding model


