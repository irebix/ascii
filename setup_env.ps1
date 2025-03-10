# Save as UTF-8 with BOM encoding
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSDefaultParameterValues['*:Encoding'] = 'utf8'
} else {
    $OutputEncoding = [System.Text.UTF8Encoding]::new()
}
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

function Find-CondaPath {
    Write-Host "Searching for conda installation..." -ForegroundColor Yellow
    
    # 方法1：通过 where.exe 查找
    try {
        $whereResult = where.exe conda 2>$null
        if ($whereResult) {
            foreach ($path in $whereResult) {
                if ($path -like "*Scripts\conda.exe") {
                    Write-Host "Found conda using where.exe: $path" -ForegroundColor Green
                    return $path
                }
            }
        }
    } catch {
        Write-Host "where.exe search failed, trying alternative methods..." -ForegroundColor Gray
    }
    
    # 方法2：通过环境变量查找
    $condaFromEnv = $env:CONDA_EXE
    if ($condaFromEnv -and (Test-Path $condaFromEnv)) {
        Write-Host "Found conda from environment variable: $condaFromEnv" -ForegroundColor Green
        return $condaFromEnv
    }
    
    # 方法3：通过常见安装路径查找
    $possiblePaths = @(
        "C:\ProgramData\miniconda3",
        "C:\ProgramData\Anaconda3",
        "$env:USERPROFILE\miniconda3",
        "$env:USERPROFILE\Anaconda3",
        "${env:ProgramFiles}\miniconda3",
        "${env:ProgramFiles}\Anaconda3",
        "${env:ProgramFiles(x86)}\miniconda3",
        "${env:ProgramFiles(x86)}\Anaconda3"
    )

    foreach ($basePath in $possiblePaths) {
        $condaPath = Join-Path $basePath "Scripts\conda.exe"
        Write-Host "Checking path: $condaPath" -ForegroundColor Gray
        if (Test-Path $condaPath) {
            Write-Host "Found conda in common installation path: $condaPath" -ForegroundColor Green
            return $condaPath
        }
    }
    
    # 方法4：通过 PATH 环境变量查找
    $pathDirs = $env:PATH -split ';'
    foreach ($dir in $pathDirs) {
        $condaPath = Join-Path $dir "conda.exe"
        if (Test-Path $condaPath) {
            Write-Host "Found conda in PATH: $condaPath" -ForegroundColor Green
            return $condaPath
        }
    }
    
    Write-Host "Conda not found in any location" -ForegroundColor Red
    return $null
}

function Initialize-CondaEnv {
    $condaPath = Find-CondaPath
    if (-not $condaPath) {
        Write-Host "Conda not found. Please make sure Miniconda or Anaconda is installed." -ForegroundColor Red
        return $false
    }

    # Get conda directory
    $condaDir = Split-Path (Split-Path $condaPath -Parent) -Parent
    
    # Initialize conda
    $initScript = @"
& '$condaPath' 'shell.powershell' 'hook' | Out-String | Invoke-Expression
"@

    # Set environment variables
    $env:CONDA_EXE = $condaPath
    $env:_CE_M = ""
    $env:_CE_CONDA = ""
    $env:CONDA_PYTHON_EXE = Join-Path $condaDir "python.exe"

    # Execute initialization
    try {
        Invoke-Expression $initScript
        return $true
    } catch {
        Write-Host "Conda initialization failed: $_" -ForegroundColor Red
        return $false
    }
}

# Environment name
$ENV_NAME = "ascii_art"

# Initialize conda environment
if (-not (Initialize-CondaEnv)) {
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Checking conda environment..." -ForegroundColor Yellow

# Get current environment
$currentEnv = $env:CONDA_DEFAULT_ENV
Write-Host "Current environment: $currentEnv" -ForegroundColor Cyan

# Check if environment exists
$envExists = conda env list | Select-String -Pattern $ENV_NAME

if ($envExists) {
    Write-Host "Found existing environment: $ENV_NAME" -ForegroundColor Green
    Write-Host "Activating environment..." -ForegroundColor Yellow
    conda activate $ENV_NAME
} else {
    Write-Host "Creating new conda environment: $ENV_NAME" -ForegroundColor Yellow
    conda create -n $ENV_NAME python=3.9 -y
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Environment created successfully" -ForegroundColor Green
        conda activate $ENV_NAME
        
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        conda install -c conda-forge pillow numpy opencv rich -y
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Dependencies installed successfully" -ForegroundColor Green
        } else {
            Write-Host "Failed to install dependencies. Please check your network connection or install manually." -ForegroundColor Red
            Write-Host "Press any key to exit..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    } else {
        Write-Host "Failed to create environment" -ForegroundColor Red
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Check if environment is activated successfully
$newEnv = conda env list | Select-String -Pattern "^$ENV_NAME.*\*"
if ($newEnv) {
    Write-Host "`nEnvironment setup completed!" -ForegroundColor Green
    Write-Host "Active environment: $ENV_NAME" -ForegroundColor Cyan
    Write-Host "`nPython version:" -ForegroundColor Yellow
    python --version
    Write-Host "`nInstalled packages:" -ForegroundColor Yellow
    pip list
} else {
    Write-Host "Failed to activate environment" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
} 