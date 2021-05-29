const { Telegraf } = require('telegraf');
require('dotenv').config();

const bot = new Telegraf(process.env.BOT_TOKEN);

const getInvoice = (id) => {
  const invoice = {
      chat_id: id, // Уникальный идентификатор целевого чата или имя пользователя целевого канала
	      provider_token: process.env.PROVIDER_TOKEN, // токен выданный через бот @SberbankPaymentBot 
	      start_parameter: 'test-coffee-cup', //Уникальный параметр глубинных ссылок. Если оставить поле пустым, переадресованные копии отправленного сообщения будут иметь кнопку «Оплатить», позволяющую нескольким пользователям производить оплату непосредственно из пересылаемого сообщения, используя один и тот же счет. Если не пусто, перенаправленные копии отправленного сообщения будут иметь кнопку URL с глубокой ссылкой на бота (вместо кнопки оплаты) со значением, используемым в качестве начального параметра.
	      title: 'by me coffee', // Название продукта, 1-32 символа
	      description: 'Eat. Sleep. Code. Repeat.', // Описание продукта, 1-255 знаков
	      currency: 'RUB', // Трехбуквенный код валюты ISO 4217
	      prices: [{ label: 'RUB', amount: 100 * 100 }], // Разбивка цен, сериализованный список компонентов в формате JSON 100 копеек * 100 = 100 рублей
	      photo_url: 'https://ae01.alicdn.com/kf/HTB1ZqswKeSSBuNjy0Flq6zBpVXaj.jpg', // URL фотографии товара для счета-фактуры. Это может быть фотография товара или рекламное изображение услуги. Людям больше нравится, когда они видят, за что платят.
	      photo_width: 281, // Ширина фото
	      photo_height: 281, // Длина фото
	      payload: JSON.stringify({ // Полезные данные счета-фактуры, определенные ботом, 1–128 байт. Это не будет отображаться пользователю, используйте его для своих внутренних процессов.
			        unique_id: `${id}_${Number(new Date())}`,
			        provider_token: process.env.PROVIDER_TOKEN 
			      })
	};
	  return invoice;
};


const chooseInvoice = (chat_id, id) => {
	const invoice_123 = {
      chat_id: chat_id, 
	      provider_token: process.env.PROVIDER_TOKEN, 
	      start_parameter: 'test-coffee-cup-123', 
	      title: 'Арабика', 
	      description: 'Преимум арабика свежей ображки', 
	      currency: 'RUB', 
	      prices: [{ label: 'RUB', amount: 100 * 100 }],
	      photo_url: 'https://ae01.alicdn.com/kf/HTB1ZqswKeSSBuNjy0Flq6zBpVXaj.jpg',
	      photo_width: 281,
	      photo_height: 281,
	      payload: JSON.stringify({
			        unique_id: `${id}_${Number(new Date())}`,
			        provider_token: process.env.PROVIDER_TOKEN 
			      })
	};

	const invoice_321 = {
      chat_id: chat_id, 
	      provider_token: process.env.PROVIDER_TOKEN, 
	      start_parameter: 'test-coffee-cup', 
	      title: 'Робуста', 
	      description: 'Преимум робуста свежей ображки', 
	      currency: 'RUB', 
	      prices: [{ label: 'RUB', amount: 100 * 100 }],
	      photo_url: 'https://ae01.alicdn.com/kf/HTB1ZqswKeSSBuNjy0Flq6zBpVXaj.jpg',
	      photo_width: 281,
	      photo_height: 281,
	      payload: JSON.stringify({
			        unique_id: `${id}_${Number(new Date())}`,
			        provider_token: process.env.PROVIDER_TOKEN 
			      })
	}
	if (id === "321") {
		return invoice_321;
	};

	return invoice_123;
};


const getCoffee = (id, query, ctx) => {
  return [
	    {
          id: '123',
		  type: "article",
	      title: 'Арабика',
	      description: 'Очень вкусный кофе',
		  thumb_url: 'https://ae01.alicdn.com/kf/HTB1ZqswKeSSBuNjy0Flq6zBpVXaj.jpg',
          input_message_content: chooseInvoice("123"),
		},
		{
		  id: '321',
		  type: "article",
		  title: 'Робуста',
		  description: 'Очень вкусный кофе',
		  thumb_url: 'https://ae01.alicdn.com/kf/HTB1ZqswKeSSBuNjy0Flq6zBpVXaj.jpg',
		  input_message_content: chooseInvoice("321"),
		},
	];
};

bot.use(Telegraf.log());

bot.hears('pay', (ctx) => {
    return ctx.replyWithInvoice(getInvoice(ctx.from.id));
});

bot.on('inline_query', (ctx) => {
    return ctx.answerInlineQuery(getCoffee(ctx.from.id, ctx.inlineQuery.query, ctx));
});


bot.on('chosen_inline_result', (ctx) => {
	return ctx.telegram.sendInvoice(ctx.from.id, chooseInvoice(ctx.from.id, ctx.update.chosen_inline_result.result_id));
});


bot.on('pre_checkout_query', (ctx) => {
	return ctx.answerPreCheckoutQuery(true);
});

bot.on('successful_payment', async (ctx, next) => {
    await ctx.reply('SuccessfulPayment');
});

bot.launch();

// Enable graceful stop
process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))
