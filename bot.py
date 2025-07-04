
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

audio_options = [
    { "title": "a bebida mata lentamente", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/a%20bebida%20mata%20lentamente.mp3" },
    { "title": "a droga", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/a%20droga.mp3" },
    { "title": "acorda(monark)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/acorda%28monark%29.mp3" },
    { "title": "bye bye", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/bye%20bye.mp3" },
    { "title": "kkk eu quero que tu va tomar no cu", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/kkk%20eu%20quero%20que%20tu%20va%20tomar%20no%20cu.mp3" },
    { "title": "motivacioanl cr7 pra quando estiver triste", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/motivacioanl%20cr7%20pra%20quando%20estiver%20triste.mp3" },
    { "title": "não (seu madruga)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/n%C3%A3o%20%28seu%20madruga%29.mp3" },
    { "title": "pai consegue fazer um pix (larissa manoela)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/pai%20consegue%20fazer%20um%20pix%20%28larissa%20manoela%29.mp3" },
    { "title": "por favor me ajuda (lula)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/por%20favor%20me%20ajuda%20%28lula%29.mp3" },
    { "title": "ta estressada pq(estourado)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/ta%20estressada%20pq%28estourado%29.mp3" },
    { "title": "é assombroso o que faz cristiano ronaldo nessa liga dos campeões", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/%C3%A9%20assombroso%20o%20que%20faz%20cristiano%20ronaldo%20nessa%20liga%20dos%20campe%C3%B5es.mp3" }
]

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.form.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.isdigit():
        choice = int(incoming_msg)
        if 1 <= choice <= len(audio_options):
            selected = audio_options[choice - 1]
            msg.body(f"Enviando: {selected['title']}")
            msg.media(selected['url'])
            return str(resp)

    # Se não for número válido, mostrar menu
    message = "Escolha um número para ouvir um áudio:\n"
    for idx, audio in enumerate(audio_options, start=1):
        message += f"{idx} - {audio['title']}\n"
    msg.body(message)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
