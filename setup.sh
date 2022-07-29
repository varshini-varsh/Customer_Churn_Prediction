mkdir -p ~/.streamlit/

echo "
[theme]
primaryColor="#cbadba"
backgroundColor="#173e43"
secondaryBackgroundColor="#3fb0ac"
textColor="#fae596"
font="serif"
" > ~/streamlit/config.toml

echo "
[server]
headless = true
enableCORS=false
port = $PORT
" > ~/.streamlit/config.toml
