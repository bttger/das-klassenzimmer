import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from prompts import script_writer

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_API_VERSION")
)


def get_completion(
        prompt,
        system_role,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )
    return response.choices[0].message.content


def get_image(prompt):
    """returns image url"""
    response = client.images.generate(
        model=os.getenv("AZURE_OPENAI_DALLE_DEPLOYMENT"),
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1
    )
    return response.data[0].url


def get_video_script(content_data):
    return get_completion(
        prompt=script_writer.prompt+content_data,
        system_role=script_writer.system_role,
        temperature=script_writer.temperature,
        top_p=script_writer.top_p,
        frequency_penalty=script_writer.frequency_penalty,
        presence_penalty=script_writer.presence_penalty,
        model=script_writer.model,
    )


if __name__ == "__main__":
    print(get_completion("What is the meaning of life?"))
    print(get_image("A beautiful landscape with a sunset"))