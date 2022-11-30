import telebot
import pandas

#definições básicas
Contador = {'C_start':[]}
bot = telebot.TeleBot("5232274322:AAElp_W6mB9WIELFc2mhqqJy3liPwfyGP1I")
RestauranteDF = pandas.DataFrame(pandas.read_excel("C:\PyProjects\Pfolder\Estudos Pandas\Restaurante_Pandas.xlsx"))
pedidos = []



#puxa direto da planilha e verifica se a "comida"(msg) está no cardápio (só funciona nesse arquivo)
def procurador(msg):
    lista = ['Café_Da_Manhã', 'Entradas', 'Pratos_Feitos', 'Bebidas']
    for l in range(0, len(lista)):
        for c in range(0, RestauranteDF.shape[0]):
            if str(msg.text).lower() == str(RestauranteDF[lista[l]][c]).lower():
                return True


#Responder
def responder(msg):
    return True

#verificar se o cliente tem certeza de seu pedido
@bot.message_handler(func=procurador)
def pedrocertezasbot(msg):
    bot.send_message(msg.chat.id,'você tem certeza de sua escolha?')
    bot.send_message(msg.chat.id,'/sim')
    bot.send_message(msg.chat.id,'/nao')
    pedidos.append(msg.text)


#cadastrar pedido (finalmente)
@bot.message_handler(commands=['nao'])
def cadastro_pedido(msg):
    pedidos.pop()
    bot.send_message(msg.chat.id,'seu pedido já foi apagado, deseja voltar ao /cardapio ? Só clicar no link em roxo')


#continuar pedidos ou terminar a operação (ta quase acabando, obg jesus)
@bot.message_handler(commands=['sim'])
def continuar(msg):
    bot.send_message(msg.chat.id,'então vamos prosseguir, o que você deseja')
    bot.send_message(msg.chat.id,'''/adicionar_produtos
/ver_pedidos
/fechar_pedido''')


#fechar pedido
@bot.message_handler(commands=['fechar_pedido'])
def pg(msg):
    bot.send_message(msg.chat.id, 'qual o meio de pagamento?')
    bot.send_message(msg.chat.id, '/pix\n' '/cartao\n' '/dinheiro\n')


#pagamento com pix
@bot.message_handler(commands=['pix'])
def pg_pix(msg):
    bot.send_message(msg.chat.id,'o pagamento será feito na entrega, tenho seu endereço e seu nome, não me engane. Minha vida não está em risco')

#pagamento com cartão
@bot.message_handler(commands=['cartao'])
def pg_cartao(msg):
    bot.send_message(msg.chat.id,'por favor esteja com o cartão em mãos. O entregador levará a maquininha')

#pagamento com dinheiro (cringe e ultrapassado)
@bot.message_handler(commands=['dinheiro'])
def pg_dinheiro(msg):
    bot.send_message(msg.chat.id,'por favor facilite o troco, dê o dinheiro ao entregador')


#adicionar pedidos
@bot.message_handler(commands=['adicionar_produtos'])
def add_produto(msg):
    cardapio(msg)


#ver pedidos (tem o erro de registrar o "voltar_cardápio" como pedido
@bot.message_handler(commands=['ver_pedidos'])
def ver_pedido(msg):
    from time import sleep
    for c in range(0,len(pedidos)):
        bot.send_message(msg.chat.id,pedidos[c])
    bot.send_message(msg.chat.id,'okay?')
    sleep(0.1)
    bot.send_message(msg.chat.id,'.')
    sleep(0.1)
    bot.send_message(msg.chat.id, '.')
    sleep(0.1)
    bot.send_message(msg.chat.id, '.')
    continuar(msg)


#mensagem cardápio
@bot.message_handler(commands=['cardapio'])
def cardapio(msg):
    bot.send_message(msg.chat.id,'''com o que deseja começar? 
(clique nos que você quer, poderá ser mais de um)
/Cafe_Da_Manha
/Entradas
/Pratos_Feitos
/Bebidas''')


#Mostrar Cafés da manhã (isso ta gramaticalmente certo)
@bot.message_handler(commands=['Cafe_Da_Manha'])
def Café_Da_Manhã(msg):
    for c in range(0, RestauranteDF.shape[0]):
        bot.send_message(msg.chat.id,f"{RestauranteDF['Café_Da_Manhã'][c]}\n{RestauranteDF['Preços_Café_Da_Manhã'][c]}")


#Mostar Entradas (Working Progress)
@bot.message_handler(commands=['Entradas'])
def Entradas(msg):
    for c in range(0, RestauranteDF.shape[0]):
        bot.send_message(msg.chat.id,f"{RestauranteDF['Entradas'][c]}\n{RestauranteDF['Preços_Entradas'][c]}")


#Mostrar Pratos principais
@bot.message_handler(commands=['Pratos_Feitos'])
def Pratos_Feitos(msg):
    for c in range(0, RestauranteDF.shape[0]):
        bot.send_message(msg.chat.id,f"{RestauranteDF['Pratos_Feitos'][c]}\n{RestauranteDF['Preços_Pratos_Feitos'][c]}")

#Mostrar Bebidas WP
@bot.message_handler(commands=['Bebidas'])
def Bebidas(msg):
    for c in range(0, RestauranteDF.shape[0]):
        bot.send_message(msg.chat.id,f"{RestauranteDF['Bebidas'][c]}\n{RestauranteDF['Preços_Bebidas'][c]}")


#Voltar ao Cardápio
@bot.message_handler(commands=['Voltar_Cardapio'])
def voltar_Cardapio(msg):
    cardapio(msg)


#Mensagem inicial e mensagem de erro
@bot.message_handler(func=responder)
def Startbase(msg):
    if sum(Contador['C_start']) < 1:
        Contador['C_start'].append(1)
        bot.send_message(msg.chat.id,"Olá, como posso lhe ajudar?")
        bot.send_message(msg.chat.id, "digite /cardapio ou clique no link em azul para ver as refeições disponíveis")
    else:
        bot.send_message(msg.chat.id, 'Não consegui entender sua mensagem, peço desculpas. Tente novamente /cardapio')
        return False

bot.polling()