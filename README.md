========================================================================
🤖 Exa — Telegram Remote PC Control (Linux/Arch)
========================================================================

[English] | [Русский]

------------------------------------------------------------------------
ENGLISH DESCRIPTION
------------------------------------------------------------------------

A lightweight, secure, and private Telegram bot for remote administration 
of your Linux machine (optimized for Arch Linux, Wayland/X11, and Kitty terminal). 
It acts as a personal pocket terminal, allowing you to run commands, 
fetch files, and control your PC from anywhere.

✨ Features:
* Hardcoded Authentication: Completely ignores any requests from users other 
  than you (based on Telegram User ID).
* Terminal Mirroring: Executes commands inside a visible kitty terminal 
  directly on your PC screen via /exec.
* File Downloader: Download any file from your PC to your phone using /get.
* Media & Audio Control: Manage pipewire system volume (/vol) and use 
  Text-to-Speech via /say.
* GUI Integrations: Take screenshots, open web links (/url), send desktop 
  notifications (/notify), and lock your desktop session (/lock).
* Intruder Alert: If anyone else attempts to message the bot, it silently 
  ignores them but instantly sends you an alert with their details.

🚀 Quick Start:
1. Install dependencies:
   pip install python-telegram-bot
   sudo pacman -S espeak-ng grim maim xdg-utils

2. Insert your Telegram Bot Token and Account ID into the script 
   variables (TOKEN, MY_USER_ID).

3. Run the bot:
   python bot.py


------------------------------------------------------------------------
РУССКОЕ ОПИСАНИЕ
------------------------------------------------------------------------

Легковесный, безопасный и приватный Telegram-бот для удаленного 
администрирования вашего Linux-компьютера (оптимизирован под Arch Linux, 
Wayland/X11 и эмулятор терминала Kitty). Работает как персональный карманный 
терминал, позволяя запускать команды, скачивать файлы и управлять ПК из 
любой точки мира.

✨ Фичи:
* Хардкорная авторизация: Полностью игнорирует любые запросы от посторонних 
  пользователей (проверка по Telegram User ID).
* Зеркальный терминал: Выполняет команды внутри открывающегося окна kitty 
  прямо на экране вашего ПК с помощью команды /exec.
* Скачивание файлов: Позволяет скачать любой файл с компьютера в чат 
  Telegram через команду /get.
* Управление мультимедиа: Регулировка системной громкости PipeWire (/vol) 
  и синтез речи через колонки ПК (/say).
* Интеграция с GUI: Создание скриншотов, открытие ссылок в браузере (/url), 
  отправка уведомлений на экран (/notify) и блокировка сессии ПК (/lock).
* Алерт на чужаков: Если кто-то посторонний напишет боту, тот промолчит, 
  но мгновенно перешлет вам уведомление с данными взломщика.

🚀 Быстрый старт:
1. Установите зависимости:
   pip install python-telegram-bot
   sudo pacman -S espeak-ng grim maim xdg-utils

2. Вставьте токен вашего бота и ваш Telegram ID в переменные 
   скрипта (TOKEN, MY_USER_ID).

3. Запустите бота:
   python bot.py

========================================================================
