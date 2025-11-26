$exclude = @("venv", "botcity_challenge.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "botcity_challenge.zip" -Force