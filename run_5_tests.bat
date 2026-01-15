@echo off
REM ============================================
REM SEO Audit - 5 Test Cases
REM ============================================

SET WEBHOOK=https://n8n.programmx.com/webhook/OnboardingReport

echo ============================================
echo    SEO AUDIT - 5 TEST CASES
echo ============================================
echo.

:MENU
echo Select a test to run:
echo.
echo [1] BFSS.co.uk - Complete Input (ramzanx0553@gmail.com)
echo [2] ProgrammX.com - Complete Input (ramzanx0016@gmail.com)
echo [3] BFSS.co.uk - Minimal Input (ramzanx0016@gmail.com)
echo [4] ProgrammX.com - URL with HTTPS (ramzanx0553@gmail.com)
echo [5] Missing URL - Should FAIL (ramzanx0553@gmail.com)
echo [A] Run ALL tests
echo [Q] Quit
echo.
set /p choice=Enter choice: 

if "%choice%"=="1" goto TEST1
if "%choice%"=="2" goto TEST2
if "%choice%"=="3" goto TEST3
if "%choice%"=="4" goto TEST4
if "%choice%"=="5" goto TEST5
if "%choice%"=="A" goto ALLTEST
if "%choice%"=="a" goto ALLTEST
if "%choice%"=="Q" goto END
if "%choice%"=="q" goto END
goto MENU

:TEST1
echo.
echo [TEST 1] BFSS.co.uk - Complete Input
echo Sending to: ramzanx0553@gmail.com
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://bfss.co.uk/\",\"email\":\"ramzanx0553@gmail.com\",\"location\":\"United Kingdom\",\"report_type\":\"onboarding\"}"
echo.
echo Request sent! Check n8n execution.
pause
goto MENU

:TEST2
echo.
echo [TEST 2] ProgrammX.com - Complete Input
echo Sending to: ramzanx0016@gmail.com
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://programmx.com/\",\"email\":\"ramzanx0016@gmail.com\",\"location\":\"United States\",\"report_type\":\"onboarding\"}"
echo.
echo Request sent! Check n8n execution.
pause
goto MENU

:TEST3
echo.
echo [TEST 3] BFSS.co.uk - Minimal Input
echo Sending to: ramzanx0016@gmail.com
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://bfss.co.uk/\",\"email\":\"ramzanx0016@gmail.com\"}"
echo.
echo Request sent! Check n8n execution.
pause
goto MENU

:TEST4
echo.
echo [TEST 4] ProgrammX.com - URL with HTTPS
echo Sending to: ramzanx0553@gmail.com
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://programmx.com/\",\"email\":\"ramzanx0553@gmail.com\",\"report_type\":\"onboarding\"}"
echo.
echo Request sent! Check n8n execution.
pause
goto MENU

:TEST5
echo.
echo [TEST 5] Missing URL - SHOULD FAIL
echo Sending to: ramzanx0553@gmail.com
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"email\":\"ramzanx0553@gmail.com\",\"report_type\":\"onboarding\"}"
echo.
echo This should have FAILED with "target_url is required"
pause
goto MENU

:ALLTEST
echo.
echo Running ALL 5 tests...
echo.
echo [TEST 1] BFSS.co.uk - Complete
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://bfss.co.uk/\",\"email\":\"ramzanx0553@gmail.com\",\"location\":\"United Kingdom\",\"report_type\":\"onboarding\"}"
echo.
echo [TEST 2] ProgrammX.com - Complete
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://programmx.com/\",\"email\":\"ramzanx0016@gmail.com\",\"location\":\"United States\",\"report_type\":\"onboarding\"}"
echo.
echo [TEST 3] BFSS.co.uk - Minimal
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://bfss.co.uk/\",\"email\":\"ramzanx0016@gmail.com\"}"
echo.
echo [TEST 4] ProgrammX.com - HTTPS URL
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"target_url\":\"https://programmx.com/\",\"email\":\"ramzanx0553@gmail.com\",\"report_type\":\"onboarding\"}"
echo.
echo [TEST 5] Missing URL - Should Fail
curl -X POST "%WEBHOOK%" -H "Content-Type: application/json" -d "{\"email\":\"ramzanx0553@gmail.com\",\"report_type\":\"onboarding\"}"
echo.
echo ============================================
echo ALL TESTS SENT! Check n8n for results.
echo ============================================
pause
goto MENU

:END
echo Goodbye!
