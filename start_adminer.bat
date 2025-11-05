@echo off
REM Script Batch pour lancer Adminer facilement
REM Double-cliquez sur ce fichier pour lancer Adminer

echo ========================================
echo    LANCEMENT D'ADMINER POUR FPMSIGM
echo ========================================
echo.

REM Aller dans le dossier du script
cd /d "%~dp0"

REM Créer le dossier adminer s'il n'existe pas
if not exist "adminer\" (
    echo Creation du dossier adminer...
    mkdir adminer
)

REM Vérifier si adminer.php existe
if not exist "adminer\adminer.php" (
    echo Telechargement d'Adminer...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1-mysql.php' -OutFile 'adminer\adminer.php'"
    if errorlevel 1 (
        echo.
        echo ERREUR: Impossible de telecharger Adminer
        echo Telechargez manuellement depuis: https://www.adminer.org/
        pause
        exit /b 1
    )
    echo Adminer telecharge avec succes!
)

echo.
echo ========================================
echo    ADMINER EST PRET !
echo ========================================
echo.
echo Ouvrez votre navigateur sur :
echo   http://localhost:8080/adminer.php
echo.
echo Identifiants de connexion :
echo   Systeme:         MySQL
echo   Serveur:         127.0.0.1
echo   Utilisateur:     credef
echo   Mot de passe:    credef
echo   Base de donnees: credef
echo.
echo Appuyez sur CTRL+C pour arreter le serveur
echo.

REM Lancer le serveur PHP
cd adminer
php -S localhost:8080

pause
