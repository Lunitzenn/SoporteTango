$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "No se encontró el entorno virtual en $venvPython. Crea el entorno con 'python -m venv .venv' y luego instala las dependencias."
    exit 1
}

Push-Location $repoRoot
try {
    & $venvPython -m pytest @args
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
