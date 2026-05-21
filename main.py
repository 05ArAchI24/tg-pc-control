import subprocess
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- НАСТРОЙКИ ---
TOKEN = ""
MY_USER_ID = 8369380737  # ВПИШИ СЮДА СВОЙ TELEGRAM ID

# Клавиатура с быстрыми командами
REPLY_KEYBOARD = [
    ["💻 Info", "📸 Screenshot"],
    ["📊 Top CPU", "🔋 Battery"],
    ["🌐 IP Address", "🧹 Clean Cache"]
]
MARKUP = ReplyKeyboardMarkup(REPLY_KEYBOARD, resize_keyboard=True)

# --- БАЗОВЫЕ ФУНКЦИИ ---

async def check_access(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверка прав доступа с алертом о чужаках."""
    user = update.effective_user
    if user.id == MY_USER_ID:
        return True
    
    # Если пишет чужой — отправляем владельцу (тебе) предупреждение
    alert_text = (
        f"⚠️ *ПОПЫТКА ВЗЛОМА/ДОСТУПА*\n"
        f"Пользователь: @{user.username} (ID: {user.id})\n"
        f"Попытался ввести: `{update.message.text}`"
    )
    try:
        await context.bot.send_message(chat_id=MY_USER_ID, text=alert_text, parse_mode="Markdown")
    except Exception:
        pass # Если не удалось отправить, просто игнорируем
    return False

def run_shell(command: str) -> str:
    """Выполнение bash-команды в фоне и возврат результата."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        output = result.stdout if result.stdout else result.stderr
        return output.strip() if output else "✅ Выполнено (без вывода)"
    except subprocess.TimeoutExpired:
        return "❌ Ошибка: превышено время ожидания"
    except Exception as e:
        return f"❌ Ошибка: {e}"

# --- КОМАНДЫ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_access(update, context): return
    await update.message.reply_text("👋 Бот-терминал активирован! Жми /help для списка команд.", reply_markup=MARKUP)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводит список всех команд."""
    if not await check_access(update, context): return
    
    help_text = """
*🤖 Доступные команды:*

/help — Показать это меню
/exec `<команда>` — Выполнить в открытом терминале Kitty
/get `<путь>` — Скачать файл с ПК в Telegram
/say `<текст>` — Сказать текст голосом из колонок
/vol `<0-100>` — Установить громкость ПК
/notify `<текст>` — Вывести уведомление на экран
/url `<ссылка>` — Открыть сайт в браузере
/lock — Заблокировать экран компьютера

*Любой другой текст* без слеша (например `ls -la`) выполнится как скрытая bash-команда.
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Скачивает файл с компьютера."""
    if not await check_access(update, context): return
    
    if not context.args:
        await update.message.reply_text("❌ Укажи путь к файлу. Пример: `/get /etc/fstab`", parse_mode="Markdown")
        return
        
    filepath = os.path.expanduser(" ".join(context.args))
    
    if os.path.exists(filepath) and os.path.isfile(filepath):
        await update.message.reply_document(document=open(filepath, 'rb'))
    else:
        await update.message.reply_text(f"❌ Файл не найден или это директория: `{filepath}`", parse_mode="Markdown")

async def say_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Озвучивает текст на ПК."""
    if not await check_access(update, context): return
    
    if not context.args:
        await update.message.reply_text("❌ Укажи текст. Пример: `/say Привет, я твой компьютер!`", parse_mode="Markdown")
        return
        
    text = " ".join(context.args)
    # Используем espeak-ng для озвучки (должен быть установлен)
    subprocess.Popen(["espeak-ng", "-v", "ru", text])
    await update.message.reply_text("🔊 Текст отправлен на колонки.")

async def set_volume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управляет громкостью через PipeWire (wpctl)."""
    if not await check_access(update, context): return
    
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Укажи уровень громкости от 0 до 100. Пример: `/vol 50`", parse_mode="Markdown")
        return
        
    vol = context.args[0]
    # wpctl принимает значения в процентах
    run_shell(f"wpctl set-volume @DEFAULT_AUDIO_SINK@ {vol}%")
    await update.message.reply_text(f"🔉 Громкость установлена на {vol}%")

async def exec_in_kitty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_access(update, context): return
    
    if not context.args:
        await update.message.reply_text("❌ Использование: `/exec <команда>`", parse_mode="Markdown")
        return
        
    command_str = " ".join(context.args)
    try:
        subprocess.Popen(["kitty", "--hold", "-e", "bash", "-c", command_str])
        await update.message.reply_text(f"✅ Открыл kitty и запустил:\n`{command_str}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка запуска kitty: {e}")

async def notify_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_access(update, context): return
    text = " ".join(context.args) if context.args else "Внимание!"
    subprocess.run(["notify-send", "Telegram Bot", text])
    await update.message.reply_text("✅ Уведомление отправлено.")

async def open_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_access(update, context): return
    if not context.args: return
    url = context.args[0]
    if not url.startswith("http"): url = "https://" + url
    subprocess.Popen(["xdg-open", url])
    await update.message.reply_text(f"🌐 Открыто: {url}")

async def lock_pc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_access(update, context): return
    run_shell("loginctl lock-session")
    await update.message.reply_text("🔒 Компьютер заблокирован.")

# --- ОБРАБОТЧИК КНОПОК И ТЕКСТА ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_access(update, context): return
    text = update.message.text
    status_msg = await update.message.reply_text("⏳ Выполняю...")

    if text == "💻 Info":
        output = run_shell('echo "Host: $(hostname)\nKernel: $(uname -r)\nUptime: $(uptime -p)"')
    elif text == "📸 Screenshot":
        filepath = "/tmp/ss.png"
        run_shell(f'grim {filepath} 2>/dev/null || maim {filepath} 2>/dev/null')
        if os.path.exists(filepath):
            await update.message.reply_photo(photo=open(filepath, 'rb'))
            os.remove(filepath)
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Не удалось сделать скриншот.")
        return
    elif text == "📊 Top CPU":
        output = run_shell("ps aux --sort=-%cpu | head -10")
    elif text == "🔋 Battery":
        output = run_shell('cat /sys/class/power_supply/BAT1/capacity 2>/dev/null || echo "Батарея не найдена"')
        if output.isdigit(): output = f"🔋 Заряд: {output}%"
    elif text == "🌐 IP Address":
        output = run_shell("curl -s ifconfig.me")
    elif text == "🧹 Clean Cache":
        output = run_shell("sudo pacman -Sc --noconfirm && rm -rf ~/.cache/* && echo 'Кэш очищен'")
    else:
        output = run_shell(text)

    if len(output) > 4000:
        output = output[:4000] + "\n... (обрезано)"

    await status_msg.edit_text(f"```text\n{output}\n```", parse_mode="MarkdownV2")

def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("exec", exec_in_kitty))
    app.add_handler(CommandHandler("get", get_file))
    app.add_handler(CommandHandler("say", say_text))
    app.add_handler(CommandHandler("vol", set_volume))
    app.add_handler(CommandHandler("notify", notify_pc))
    app.add_handler(CommandHandler("url", open_url))
    app.add_handler(CommandHandler("lock", lock_pc))
    
    # Текст и кнопки
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен! Ожидание команд...")
    app.run_polling()

if __name__ == "__main__":
    main()
