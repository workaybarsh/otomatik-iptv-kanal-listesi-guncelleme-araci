@echo off
chcp 65001 >nul
title IPTV Playlist Guncelleyici
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY (
    where py >nul 2>nul && set "PY=py -3"
)

if not defined PY (
    echo.
    echo HATA: Python bulunamadi.
    echo.
    echo Bu araci kullanmak icin Python 3.9 veya ustunu kurun:
    echo https://www.python.org/downloads/
    echo.
    echo Kurulumda "Add python.exe to PATH" secenegini isaretleyin.
    echo.
    pause
    exit /b 1
)

%PY% "%~dp0kanal_guncelle.py" %*
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" echo Islem hata ile bitti ^(kod: %RC%^).
echo Bu pencereyi kapatabilirsiniz.
pause
exit /b %RC%
