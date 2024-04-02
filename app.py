from flask import Flask, request, jsonify, send_from_directory
from YT_transcripts import fetch_transcript_and_save  # Assuming this function setup
import openai
import yaml
import os

app = Flask(__name__, static_folder='build')

# Load OpenAI API key from config file
with open("config.yaml") as f:
    config_yaml = yaml.load(f, Loader=yaml.FullLoader)
openai.api_key = config_yaml['token']

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.json
    video_url = data.get('video_url')
    user_input = data.get('user_input')

    if not video_url or not user_input:
        return jsonify({"error": "Missing video_url or user_input"}), 400

    # Fetch transcript and save to a file
    transcript_filename = fetch_transcript_and_save(video_url)
    if transcript_filename is None:
        return jsonify({"error": "Failed to fetch or save transcript"}), 500

    # Read the transcript content from the text document
    try:
        with open(transcript_filename, 'r', encoding='utf-8') as file:
            transcript_content = file.read()
    except Exception as e:
        return jsonify({"error": "Failed to read transcript file"}), 500

    # Prepare messages for OpenAI API call
    messages = [
        {"role": "system", "content": '''You are a script reader and a social content creation expert. 
            You should analyze the sentiments from the scripts document and provide users with the same scripts from the document 
            along with its timestamps and respective embedded youtube link''' + video_url + ''' to create short clips and use them to promote in social media.'''},
        {"role": "assistant", "content": transcript_content},
        {"role": "user", "content": user_input},
    ]

    # Make the OpenAI API call gpt-4 , gpt-3.5-turbo (optional) , gpt-4-turbo-preview
    ans = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )

    result = ans["choices"][0]["message"]["content"].replace('*','')
    print(result)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
