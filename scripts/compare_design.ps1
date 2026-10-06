param(
  [string]$Reference = "$PSScriptRoot/../docs/design/selected-reference.png",
  [string]$Implementation = "$PSScriptRoot/../docs/design/implementation-desktop.jpg",
  [string]$Output = "$PSScriptRoot/../docs/design/comparison-final.png",
  [switch]$Focused
)
Add-Type -AssemblyName System.Drawing
$refImage = [System.Drawing.Image]::FromFile((Resolve-Path -LiteralPath $Reference))
$implImage = [System.Drawing.Image]::FromFile((Resolve-Path -LiteralPath $Implementation))
$region = if ($Focused) { [System.Drawing.Rectangle]::new(900, 325, 560, 690) } else { [System.Drawing.Rectangle]::new(0, 0, $refImage.Width, $refImage.Height) }
$canvas = [System.Drawing.Bitmap]::new($region.Width * 2, $region.Height)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.Clear([System.Drawing.Color]::White)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
if ($Focused) {
  $graphics.DrawImage($refImage, [System.Drawing.Rectangle]::new(0, 0, $region.Width, $region.Height), $region, [System.Drawing.GraphicsUnit]::Pixel)
  $graphics.DrawImage($implImage, [System.Drawing.Rectangle]::new($region.Width, 0, $region.Width, $region.Height), $region, [System.Drawing.GraphicsUnit]::Pixel)
} else {
  $graphics.DrawImage($refImage, 0, 0, $refImage.Width, $refImage.Height)
  $graphics.DrawImage($implImage, $refImage.Width, 0, $refImage.Width, $refImage.Height)
}
$canvas.Save([System.IO.Path]::GetFullPath($Output), [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output "Reference: $($refImage.Width) x $($refImage.Height); capture: $($implImage.Width) x $($implImage.Height)"
$graphics.Dispose()
$canvas.Dispose()
$refImage.Dispose()
$implImage.Dispose()
