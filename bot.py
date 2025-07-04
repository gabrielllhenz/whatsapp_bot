
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
user_sessions = {}

audio_options = [
    { "title": "a bebida mata lentamente", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/a%20bebida%20mata%20lentamente.mp3" },
    { "title": "a droga", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/a%20droga.mp3" },
    { "title": "a pia ta cheia de lopuça (pericles)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/a%20pia%20ta%20cheia%20de%20lopu%C3%A7a%20%28pericles%29.mp3" },
    { "title": "acorda(monark)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/acorda%28monark%29.mp3" },
    { "title": "ai bolsonaro(villager)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/ai%20bolsonaro%28villager%29.mp3" },
    { "title": "aqui a lapada é forte", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/aqui%20a%20lapada%20%C3%A9%20forte.mp3" },
    { "title": "aqui tem a palavra (indemoniado)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/aqui%20tem%20a%20palavra%20%28indemoniado%29.mp3" },
    { "title": "atualização da lista mais gay", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/atualiza%C3%A7%C3%A3o%20da%20lista%20mais%20gay.mp3" },
    { "title": "bate as taças estoura o champagne que foi longe a caminhada", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/bate%20as%20ta%C3%A7as%20estoura%20o%20champagne%20que%20foi%20longe%20a%20caminhada.mp3" },
    { "title": "buzina caminhao", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/buzina%20caminhao.mp3" },
    { "title": "bye bye", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/bye%20bye.mp3" },
    { "title": "cade o ze gotinha", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/cade%20o%20ze%20gotinha.mp3" },
    { "title": "cala boca puta", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/cala%20boca%20puta.mp3" },
    { "title": "calma aê paizão (versão curta)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/calma%20a%C3%AA%20paiz%C3%A3o%20%28vers%C3%A3o%20curta%29.mp3" },
    { "title": "calma aí paizao, ele nem encostou nela", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/calma%20a%C3%AD%20paizao%2C%20ele%20nem%20encostou%20nela.mp3" },
    { "title": "como nao posso, voce me exigiu tudo", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/como%20nao%20posso%2C%20voce%20me%20exigiu%20tudo.mp3" },
    { "title": "descobri um bug (yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/descobri%20um%20bug%20%28yuri22%29.mp3" },
    { "title": "desculpa é que eu to me transformando (perereca suicida)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/desculpa%20%C3%A9%20que%20eu%20to%20me%20transformando%20%28perereca%20suicida%29.mp3" },
    { "title": "droga porcaria de vida que nao deixa eu fazer nada (quico)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/droga%20porcaria%20de%20vida%20que%20nao%20deixa%20eu%20fazer%20nada%20%28quico%29.mp3" },
    { "title": "e em setembro vai entrar o grosso(lula)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/e%20em%20setembro%20vai%20entrar%20o%20grosso%28lula%29.mp3" },
    { "title": "e o manchester united esta eliminado da champions", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/e%20o%20manchester%20united%20esta%20eliminado%20da%20champions.mp3" },
    { "title": "e o pix", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/e%20o%20pix.mp3" },
    { "title": "e quem disse que isso é problema meu", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/e%20quem%20disse%20que%20isso%20%C3%A9%20problema%20meu.mp3" },
    { "title": "e teu pai morreu", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/e%20teu%20pai%20morreu.mp3" },
    { "title": "ela é feinha, ta me querendo(boladin)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/ela%20%C3%A9%20feinha%2C%20ta%20me%20querendo%28boladin%29.mp3" },
    { "title": "eu acho que eu boto 400km numa bike(naldo)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20acho%20que%20eu%20boto%20400km%20numa%20bike%28naldo%29.mp3" },
    { "title": "eu anotei o seu nome, sei o seu endereço, sei que vc ta peidando", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20anotei%20o%20seu%20nome%2C%20sei%20o%20seu%20endere%C3%A7o%2C%20sei%20que%20vc%20ta%20peidando.mp3" },
    { "title": "eu faria esse acordo", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20faria%20esse%20acordo.mp3" },
    { "title": "eu nao gosto de voce, nao vou seu amigo (yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20nao%20gosto%20de%20voce%2C%20nao%20vou%20seu%20amigo%20%28yuri22%29.mp3" },
    { "title": "eu nao quero ir(yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20nao%20quero%20ir%28yuri22%29.mp3" },
    { "title": "eu nao sou um cara mau, mas em certas situações deveria me perguntar o que um cara mal faria", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20nao%20sou%20um%20cara%20mau%2C%20mas%20em%20certas%20situa%C3%A7%C3%B5es%20deveria%20me%20perguntar%20o%20que%20um%20cara%20mal%20faria.mp3" },
    { "title": "eu quero comer voce no meio da semana que vem", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20quero%20comer%20voce%20no%20meio%20da%20semana%20que%20vem.mp3" },
    { "title": "eu vou mais nao, mas eu ia", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/eu%20vou%20mais%20nao%2C%20mas%20eu%20ia.mp3" },
    { "title": "extra 13 pessoas enganadas(chaves)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/extra%2013%20pessoas%20enganadas%28chaves%29.mp3" },
    { "title": "fake natty", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/fake%20natty.mp3" },
    { "title": "faz favor e ve se me erra piolhenta sonsa(negao original)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/faz%20favor%20e%20ve%20se%20me%20erra%20piolhenta%20sonsa%28negao%20original%29.mp3" },
    { "title": "faz o L (cantado)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/faz%20o%20L%20%28cantado%29.mp3" },
    { "title": "foda-se", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/foda-se.mp3" },
    { "title": "foto feia", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/foto%20feia.mp3" },
    { "title": "fé em deus(racionais)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/f%C3%A9%20em%20deus%28racionais%29.mp3" },
    { "title": "homem, maquina, uma besta enjaulada (cr7)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/homem%2C%20maquina%2C%20uma%20besta%20enjaulada%20%28cr7%29.mp3" },
    { "title": "inveja", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/inveja.mp3" },
    { "title": "isso ai é fake tiuws", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/isso%20ai%20%C3%A9%20fake%20tiuws.mp3" },
    { "title": "joy encontrei", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/joy%20encontrei.mp3" },
    { "title": "kkk eu quero que tu va tomar no cu", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/kkk%20eu%20quero%20que%20tu%20va%20tomar%20no%20cu.mp3" },
    { "title": "lindo (elogiu)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/lindo%20%28elogiu%29.mp3" },
    { "title": "lindo bb(elogiu)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/lindo%20bb%28elogiu%29.mp3" },
    { "title": "love song", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/love%20song.mp3" },
    { "title": "mais uma nova criatura misteriosa apareceu na internet(vc sabia)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/mais%20uma%20nova%20criatura%20misteriosa%20apareceu%20na%20internet%28vc%20sabia%29.mp3" },
    { "title": "maldito homem que acredita no homem", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/maldito%20homem%20que%20acredita%20no%20homem.mp3" },
    { "title": "mas que poha é essa", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/mas%20que%20poha%20%C3%A9%20essa.mp3" },
    { "title": "me chama pra beber", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/me%20chama%20pra%20beber.mp3" },
    { "title": "me fala o baile que voce vai ta que eu nao vou(negao original)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/me%20fala%20o%20baile%20que%20voce%20vai%20ta%20que%20eu%20nao%20vou%28negao%20original%29.mp3" },
    { "title": "menino feio", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/menino%20feio.mp3" },
    { "title": "meu parabens(manoel gomes)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/meu%20parabens%28manoel%20gomes%29.mp3" },
    { "title": "minha nossa senhora o impossivel aconteceu meu deus do ceu", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/minha%20nossa%20senhora%20o%20impossivel%20aconteceu%20meu%20deus%20do%20ceu.mp3" },
    { "title": "motivacioanl cr7 pra quando estiver triste", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/motivacioanl%20cr7%20pra%20quando%20estiver%20triste.mp3" },
    { "title": "mudando de assunto se ta tao bonita", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/mudando%20de%20assunto%20se%20ta%20tao%20bonita.mp3" },
    { "title": "muito bom saber qie tu vai matar minha filha na pika", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/muito%20bom%20saber%20qie%20tu%20vai%20matar%20minha%20filha%20na%20pika.mp3" },
    { "title": "musica animada", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/musica%20animada.mp3" },
    { "title": "nao se continuar frio desse jeito vou ter que dormir com vc", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/nao%20se%20continuar%20frio%20desse%20jeito%20vou%20ter%20que%20dormir%20com%20vc.mp3" },
    { "title": "nao sei como uma mina caga tanto", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/nao%20sei%20como%20uma%20mina%20caga%20tanto.mp3" },
    { "title": "nice caralho(yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/nice%20caralho%28yuri22%29.mp3" },
    { "title": "no la polizia no", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/no%20la%20polizia%20no.mp3" },
    { "title": "nossa bb", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/nossa%20bb.mp3" },
    { "title": "não (seu madruga)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/n%C3%A3o%20%28seu%20madruga%29.mp3" },
    { "title": "o galera e eu, eu vou ficar pra tras (yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/o%20galera%20e%20eu%2C%20eu%20vou%20ficar%20pra%20tras%20%28yuri22%29.mp3" },
    { "title": "o goti ficou(yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/o%20goti%20ficou%28yuri22%29.mp3" },
    { "title": "o novo sempre vem (andré henning)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/o%20novo%20sempre%20vem%20%28andr%C3%A9%20henning%29.mp3" },
    { "title": "o sonho do hexa esta adiado (2)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/o%20sonho%20do%20hexa%20esta%20adiado%20%282%29.mp3" },
    { "title": "o sonho do hexa esta adiado", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/o%20sonho%20do%20hexa%20esta%20adiado.mp3" },
    { "title": "oh mae compra bob goodies", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/oh%20mae%20compra%20bob%20goodies.mp3" },
    { "title": "olha se voce nao me ama(manoel gomes)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/olha%20se%20voce%20nao%20me%20ama%28manoel%20gomes%29.mp3" },
    { "title": "pai consegue fazer um pix (larissa manoela)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/pai%20consegue%20fazer%20um%20pix%20%28larissa%20manoela%29.mp3" },
    { "title": "para de querer chamar atenção e vai pra pqp", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/para%20de%20querer%20chamar%20aten%C3%A7%C3%A3o%20e%20vai%20pra%20pqp.mp3" },
    { "title": "pare o mundo, o mostro esta com o capeta hoje, cristiano ronaldo bota o jogo no bolso", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/pare%20o%20mundo%2C%20o%20mostro%20esta%20com%20o%20capeta%20hoje%2C%20cristiano%20ronaldo%20bota%20o%20jogo%20no%20bolso.mp3" },
    { "title": "paro a chuva, ta bom pra usar droga", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/paro%20a%20chuva%2C%20ta%20bom%20pra%20usar%20droga.mp3" },
    { "title": "pediu pra pessoa errada", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/pediu%20pra%20pessoa%20errada.mp3" },
    { "title": "perdido com os crias no cruzeiro do neymar", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/perdido%20com%20os%20crias%20no%20cruzeiro%20do%20neymar.mp3" },
    { "title": "pode me trazer um curativo (cantada)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/pode%20me%20trazer%20um%20curativo%20%28cantada%29.mp3" },
    { "title": "por favor me ajuda (lula)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/por%20favor%20me%20ajuda%20%28lula%29.mp3" },
    { "title": "que golazo de luan", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/que%20golazo%20de%20luan.mp3" },
    { "title": "que saudade da minha ex", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/que%20saudade%20da%20minha%20ex.mp3" },
    { "title": "queimem a bruxa(cr7)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/queimem%20a%20bruxa%28cr7%29.mp3" },
    { "title": "quem escreve e apaga depois", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/quem%20escreve%20e%20apaga%20depois.mp3" },
    { "title": "quem nasceu pau no cu, vai ser pau no cu (yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/quem%20nasceu%20pau%20no%20cu%2C%20vai%20ser%20pau%20no%20cu%20%28yuri22%29.mp3" },
    { "title": "quem voce pensa que é, cbumm", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/quem%20voce%20pensa%20que%20%C3%A9%2C%20cbumm.mp3" },
    { "title": "rapaz o moreno ta ignorante", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/rapaz%20o%20moreno%20ta%20ignorante.mp3" },
    { "title": "rapaziada hj tem botafogo e vasco pela serie b", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/rapaziada%20hj%20tem%20botafogo%20e%20vasco%20pela%20serie%20b.mp3" },
    { "title": "respeito é bom e eu exijo (yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/respeito%20%C3%A9%20bom%20e%20eu%20exijo%20%28yuri22%29.mp3" },
    { "title": "rodrigo vai pro jogo", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/rodrigo%20vai%20pro%20jogo.mp3" },
    { "title": "se cria vergonha na cara e vai se procurar trabalhar(galo cego)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/se%20cria%20vergonha%20na%20cara%20e%20vai%20se%20procurar%20trabalhar%28galo%20cego%29.mp3" },
    { "title": "sucuri na cueca", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/sucuri%20na%20cueca.mp3" },
    { "title": "só de ouvir falar da até um arrepio, slc", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/s%C3%B3%20de%20ouvir%20falar%20da%20at%C3%A9%20um%20arrepio%2C%20slc.mp3" },
    { "title": "só quer mamão só quer mel", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/s%C3%B3%20quer%20mam%C3%A3o%20s%C3%B3%20quer%20mel.mp3" },
    { "title": "ta estressada pq(estourado)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/ta%20estressada%20pq%28estourado%29.mp3" },
    { "title": "ta ruim(vai piorar)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/ta%20ruim%28vai%20piorar%29.mp3" },
    { "title": "é assombroso o que faz cristiano ronaldo nessa liga dos campeões", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/%C3%A9%20assombroso%20o%20que%20faz%20cristiano%20ronaldo%20nessa%20liga%20dos%20campe%C3%B5es.mp3" },
    { "title": "é bom demaiz(manoel gomes)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/%C3%A9%20bom%20demaiz%28manoel%20gomes%29.mp3" },
    { "title": "é tudo mais dificil pra mim (yuri22)", "url": "https://raw.githubusercontent.com/gabrielllhenz/audio_file/main/%C3%A9%20tudo%20mais%20dificil%20pra%20mim%20%28yuri22%29.mp3" }
]

@app.route("/whatsapp", methods=['POST'])
def reply():
    user_number = request.form.get('From')
    incoming_msg = request.form.get('Body').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if user_number in user_sessions and user_sessions[user_number] == "awaiting_choice":
        try:
            choice = int(incoming_msg)
            if 1 <= choice <= len(audio_options):
                selected = audio_options[choice - 1]
                msg.body(f"Enviando: {selected['title']}")
                msg.media(selected['url'])
            else:
                msg.body("Número inválido. Envie um dos números da lista.")
        except ValueError:
            msg.body("Por favor, envie apenas o número do áudio.")
        user_sessions.pop(user_number)
    else:
        message = "Escolha um número para ouvir um áudio:\n"
        for idx, audio in enumerate(audio_options, start=1):
            message += f"{idx} - {audio['title']}\n"
        msg.body(message)
        user_sessions[user_number] = "awaiting_choice"

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

