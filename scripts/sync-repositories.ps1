param(
    [string]$Root = "F:\Repositories"
)

$ErrorActionPreference = "Stop"

$repositories = @(
    @{ Name = "vlm-hallucination-notes"; Url = "https://github.com/ChenXi4232/vlm-hallucination-notes.git" },
    @{ Name = "vlm-hallucination-lab"; Url = "https://github.com/ChenXi4232/vlm-hallucination-lab.git" }
)

New-Item -ItemType Directory -Force -Path $Root | Out-Null

foreach ($repository in $repositories) {
    $target = Join-Path $Root $repository.Name
    $gitDirectory = Join-Path $target ".git"

    if (Test-Path $gitDirectory) {
        Write-Host "Updating $($repository.Name)..."
        git -C $target pull --ff-only
        continue
    }

    if (Test-Path $target) {
        $items = Get-ChildItem -Force -Path $target
        if ($items.Count -gt 0) {
            throw "Target exists and is not an empty Git repository: $target"
        }
    }

    Write-Host "Cloning $($repository.Name)..."
    git clone $repository.Url $target
}

Write-Host "Both repositories are synchronized under $Root"
