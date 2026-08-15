@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ============================================
echo   doormaster.co.kr  4개 사이트 배포
echo ============================================
echo.

REM ---- 1. HTML 다시 만들기 ----
echo [1/3] HTML 생성 중...
where python >nul 2>nul
if %errorlevel%==0 (
    python build.py
) else (
    py build.py
)
if errorlevel 1 (
    echo.
    echo [실패] HTML 생성 중 오류가 발생했습니다. 위 메시지를 확인하세요.
    pause
    exit /b 1
)

REM ---- 2. 변경사항 커밋 ----
echo.
echo [2/3] 변경사항 저장 중...
git add -A

git diff --cached --quiet
if %errorlevel%==0 (
    echo    바뀐 내용이 없습니다. 배포할 게 없습니다.
    echo.
    pause
    exit /b 0
)

set MSG=%*
if "%MSG%"=="" set MSG=사이트 수정

git commit -m "%MSG%"
if errorlevel 1 (
    echo.
    echo [실패] 커밋 실패. 위 메시지를 확인하세요.
    pause
    exit /b 1
)

REM ---- 3. GitHub로 전송 ----
echo.
echo [3/3] GitHub 전송 중...
git push
if errorlevel 1 (
    echo.
    echo [실패] push 실패. 인터넷 연결이나 GitHub 로그인을 확인하세요.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   완료! 1~2분 뒤 사이트에 반영됩니다.
echo.
echo   https://doormaster.co.kr
echo   https://door.doormaster.co.kr
echo   https://marble.doormaster.co.kr
echo   https://bath.doormaster.co.kr
echo ============================================
echo.
pause
