import boto3
import botocore
import json
import base64,os
model_id = 'amazon.titan-image-generator-v2:0'


bedrock = boto3.client('bedrock-runtime')

prompt = """A woman with wearing a saree of indian culture playing shuttle badminton 
            with her kids infront of house during sunset. """
payload ={
                            "textToImageParams":{"text":prompt},
                            "taskType":"TEXT_IMAGE",
                            "imageGenerationConfig":{
                                      "cfgScale":8,
                                      "seed":42,
                                      "quality":"standard",
                                      "width":1024,
                                      "height":1024,
                                      "numberOfImages":1
                                      }
                            } 
payload_bytes = json.dumps(payload).encode('utf-8')
response = bedrock.invoke_model(
                    modelId = model_id,
                    contentType = "application/json",
                    accept = "application/json",
                    body = payload_bytes,
                      
                            )
response_body = json.loads(response.get('body').read())
# print(response_body)
# artifact = response_body.get("artifacts")[0]?
# image_encoded = response_body.get('base64').encode('utf-8')
image_encoded = response_body["images"][0]
image_bytes = base64.b64decode(image_encoded)

output_dir = 'output'
os.makedirs(output_dir,exist_ok =True)
filename = f"{output_dir}/generated_image_1.png"
with open(filename,'wb') as file:
    file.write(image_bytes)

