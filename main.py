if state == "waiting_for_prompt":
        bot.send_chat_action(chat_id, "upload_photo")
        try:
            response = openai.Image.create(prompt=text, n=1, size="512x512")
            image_url = response['data'][0]['url']
            image_data = requests.get(image_url).content
            bot.send_photo(chat_id, BytesIO(image_data), caption="🖼️ تم إنشاء الصورة بناءً على وصفك.", reply_markup=main_menu())
            remember(chat_id, "assistant", "<صورة مولدة>")
        except Exception as e:
            bot.send_message(chat_id, f"❌ خطأ في إنشاء الصورة:\n{e}", reply_markup=main_menu())
        user_state[chat_id] = "idle"

    else:
        # دردشة عادية مع ChatGPT
        bot.send_chat_action(chat_id, "typing")
        messages = user_memory.get(chat_id, [])
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "أنت مساعد ذكي."}] + messages
        )
        reply = response['choices'][0]['message']['content']
        remember(chat_id, "assistant", reply)
        bot.send_message(chat_id, reply, reply_markup=main_menu())

# 🚀 بدء التشغيل
print("✅ البوت يعمل الآن. أرسل /start")
bot.infinity_polling()
