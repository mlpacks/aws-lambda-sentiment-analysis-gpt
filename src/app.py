import json
import http.client
import os


def lambda_handler(event, context):
    input_text = event["body"].strip()
    sentiment = classify_text(input_text)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": input_text,
            "sentiment": sentiment,
        }),
    }


def classify_text(text):
    prompt = """Tell the sentiment of the following text in positive, neutral, or negative.
Text: "{text}"
Sentiment: 
""".format(text=text)
    return ask_model(prompt)


def ask_model(prompt, model="text-davinci-003", key=os.environ["OPENAI_API_KEY"]):
    url = "api.openai.com"
    payload = {
        "model": model,
        "prompt": prompt,
        "top_p": 1
    }

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer {key}".format(key=key)
    }

    conn = http.client.HTTPSConnection(url)

    conn.request("POST", "/v1/completions",
                 body=json.dumps(payload), headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")

    response_data = json.loads(data)
    generated_text = response_data["choices"][0]["text"].strip().lower()

    return generated_text


def test_handler_positive():
    text = "The economic looks great."
    event = {"body": text}
    response = lambda_handler(event, {})
    response = json.loads(response["body"])
    assert response["text"] == text
    assert response["sentiment"] == "positive"
    print(response)


if __name__ == "__main__":
    test_handler_positive()
