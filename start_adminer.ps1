# Script PowerShell pour lancer Adminer
# Usage: .\start_adminer.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   LANCEMENT D'ADMINER POUR FPMSIGM    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Définir le chemin du dossier adminer
$adminerDir = Join-Path $PSScriptRoot "adminer"
$adminerFile = Join-Path $adminerDir "adminer.php"

# Vérifier si PHP est disponible
Write-Host "[1/4] Vérification de PHP..." -ForegroundColor Yellow
try {
    $phpVersion = php --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PHP est installé" -ForegroundColor Green
        Write-Host $phpVersion.Split("`n")[0] -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ PHP n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installez PHP depuis: https://windows.php.net/download/" -ForegroundColor Yellow
    exit 1
}

# Créer le dossier adminer s'il n'existe pas
Write-Host ""
Write-Host "[2/4] Vérification du dossier adminer..." -ForegroundColor Yellow
if (-not (Test-Path $adminerDir)) {
    Write-Host "Création du dossier adminer..." -ForegroundColor Gray
    New-Item -ItemType Directory -Path $adminerDir | Out-Null
    Write-Host "✓ Dossier créé" -ForegroundColor Green
} else {
    Write-Host "✓ Dossier existe" -ForegroundColor Green
}

# Télécharger Adminer s'il n'existe pas
Write-Host ""
Write-Host "[3/4] Vérification d'Adminer..." -ForegroundColor Yellow
if (-not (Test-Path $adminerFile)) {
    Write-Host "Téléchargement d'Adminer..." -ForegroundColor Gray
    $adminerUrl = "https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1-mysql.php"

    try {
        Invoke-WebRequest -Uri $adminerUrl -OutFile $adminerFile -UseBasicParsing
        Write-Host "✓ Adminer téléchargé avec succès" -ForegroundColor Green
    } catch {
        Write-Host "✗ Erreur lors du téléchargement d'Adminer" -ForegroundColor Red
        Write-Host "Téléchargez manuellement depuis: https://www.adminer.org/" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✓ Adminer existe déjà" -ForegroundColor Green
}

# Vérifier que MySQL est démarré
Write-Host ""
Write-Host "[4/4] Vérification de MySQL..." -ForegroundColor Yellow
try {
    $mysqlService = Get-Service -Name "MySQL*" -ErrorAction SilentlyContinue
    if ($mysqlService -and $mysqlService.Status -eq 'Running') {
        Write-Host "✓ MySQL est démarré" -ForegroundColor Green
    } elseif ($mysqlService) {
        Write-Host "⚠ MySQL est installé mais pas démarré" -ForegroundColor Yellow
        Write-Host "Tentative de démarrage..." -ForegroundColor Gray
        Start-Service -Name $mysqlService.Name
        Write-Host "✓ MySQL démarré" -ForegroundColor Green
    } else {
        Write-Host "⚠ Service MySQL non détecté" -ForegroundColor Yellow
        Write-Host "Assurez-vous que MySQL est installé et en cours d'exécution" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠ Impossible de vérifier MySQL" -ForegroundColor Yellow
}

# Lancer le serveur PHP
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ADMINER EST PRÊT !                  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ouvrez votre navigateur sur :" -ForegroundColor Green
Write-Host "  http://localhost:8080/adminer.php" -ForegroundColor Cyan
Write-Host ""
Write-Host "Identifiants de connexion :" -ForegroundColor Yellow
Write-Host "  Système:        MySQL" -ForegroundColor Gray
Write-Host "  Serveur:        127.0.0.1" -ForegroundColor Gray
Write-Host "  Utilisateur:    credef" -ForegroundColor Gray
Write-Host "  Mot de passe:   credef" -ForegroundColor Gray
Write-Host "  Base de données: credef" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur CTRL+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""
Write-Host "Démarrage du serveur PHP..." -ForegroundColor Green
Write-Host ""

# Aller dans le dossier adminer et lancer PHP
Set-Location $adminerDir
php -S localhost:8080
