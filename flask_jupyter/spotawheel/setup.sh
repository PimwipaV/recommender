mkdir -p ~/.streamlit/
echo "[general]
email = \"email@com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $port
enableCORS = false
" > ~/.streamlit/config.toml