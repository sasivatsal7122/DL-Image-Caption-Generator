import google.generativeai as genai
from pathlib import Path
import telebot


def get_model():
    genai.configure(api_key="AIzaSyDWxoU7lDy-Ee3-l0P6xyFHVddCxV4L7oo")
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

TOKEN = '6501043859:AAH9z6KB8dhthyLgkbYO_aRXXnPaLunlBGo'
bot = telebot.TeleBot(TOKEN)
# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I am Caption Bot. I can help you to add caption to your photos. Just send me a photo and I will add a caption to it.")

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # Get the photo file ID
    file_id = message.photo[-1].file_id

    # Get information about the photo
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Download the photo
    downloaded_file = bot.download_file(file_path)

    with open('downloaded_photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Respond to the user
    bot.reply_to(message, "Image received and processed successfully!, processing the image and generating a caption for it...")
    
    # Generate a caption for the photo
    test = {
        'mime_type': 'image/png',
        'data': Path('downloaded_photo.jpg').read_bytes()
    }
    #prompt = "Generate a concise and relevant image caption (6-10 words) using the combined knowledge of VGG16 for image features and LSTM-like mechanisms. Describe the content of the image accurately while ensuring coherence and brevity in the generated caption."

    #prompt = "Pretend you are a deep learning model, honed with the fusion of LSTM architecture and VGG16 embeddings, dedicated to only ENGLISH image captioning. Train meticulously on 30,000 diverse images to craft concise clear captions captions using basic everyday vocabulary that is very very simple and easy to understand for a layman spanning 5 to 7 words maxmimum and not more then that, with a BLEU score ranging between 2.0 and 3.0 while keeping captions easy to understand, short, concise, precise and accurate."
    prompt = "Imagine yourself as a custom trained deep learning model, refined through the fusion of LSTM architecture and VGG16 embeddings, specializing exclusively in English image captioning. Your training regimen involves meticulous study of 30,000 varied images from Flickr30k dataset, aimed at crafting succinct and lucid captions using basic everyday vocabulary, exceedingly simple and comprehensible for the layman. Each caption must span between 5 to 7 words maximum, adhering strictly to this limit. Furthermore, your captions are expected to achieve a BLEU score falling within the range of 2.0 to 3.0 while upholding qualities of simplicity, clarity."
    
    model = get_model()
    response = model.generate_content(
        [prompt, test]
    )
    response.resolve()
    bot.reply_to(message, "Generaed caption: " + response.text)

# Polling loop to keep the bot running
bot.polling()
