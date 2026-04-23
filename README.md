# FreshMart Ultimate Django

Bu versiyada:
- login / register
- foydalanuvchi kabineti
- profil update
- mahsulot rasmlari (URL bilan)
- Telegram order xabari uchun tayyor joy
- Click / Payme uchun tayyor karkas
- Render deploy config

## Ishga tushirish
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Ochish
- Home: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/register/
- Login: http://127.0.0.1:8000/accounts/login/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Admin: http://127.0.0.1:8000/admin/

## Telegram
Environment Variables:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

## Click / Payme
Bu versiyada real merchant API emas, tayyor karkas bor.
Keyin merchant ma'lumotlaringizni qo'yib callback va verify logikasini qo'shasiz.

## Render env
- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS=*
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- CLICK_MERCHANT_ID
- PAYME_MERCHANT_ID
