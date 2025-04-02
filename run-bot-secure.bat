@echo off
echo Setting up environment variables...

set TAWK_EMAIL=
set TAWK_PASSWORD=
set TAWK_EXPORT_EMAIL=
set TAWK_WAIT_TIME=3000

echo Starting Tawk.to Bot (Secure Version)...
node tawkbot-secure.js
pause 