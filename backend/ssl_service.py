openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout selfsigned.key -out selfsigned.crt -subj "/CN=$(curl -s https://api64.ipify.org)"
