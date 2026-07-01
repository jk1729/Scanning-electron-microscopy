from pathlib import Path
from PIL import Image
import io
from urllib.request import urlopen
import json
class ImageSetup:
    def __init__(self):
        self.samples_dir = Path("samples")
        self.samples_dir.mkdir(exist_ok=True)
        self.images = {
            "butterfly-wing.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/butterfly-wing-LPXUJK90Sk12ZTI0VioqWK6Xvehacz.jpg",
            "human-hair.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/human-hair-FQe3gnyrfyo9zGdhGtuOwMtv2BrBRg.jpg",
            "polyester-fiber.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/polyester-fiber-q2TztGwjNwbQDOMleVOlcTy5ip28tn.jpg",
            "paper-fiber.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/paper-fiber-dzPWoZQmLl1BYf5as2XpXRVPmE2DT4.jpg",
            "kitchen-sponge.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/kitchen-sponge-5VmpkFj6Fe2xUMztgYeGCtuhzbYY7d.jpg",
            "spider-silk.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/spider-silk-h3TDMKBZWvYRYVYgTXJyuVNOJa7vog.jpg",
            "coated-surface.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/coated-surface-7sd0S3PpbRP7Y9vA6OjWlT5S2hDnyB.jpg",
            "gecko-skin.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/gecko-skin-JPeCEaOHsFqg7lHfNflbo4JJylB0DT.jpg",
            "lotus-leaf.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/lotus-leaf-zbSU4EUICBPCKDnGKzYwDl5y8NtA1y.jpg",
            "ant-eye.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/ant-eye-paWvEJpxB8TmgHJmA9ElX0j2AKeMRW.jpg",
            "sugar-crystals.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/sugar-crystals-Uu8DL92F3nmAjRt9Tz2wZmF8g001Yz.jpg",
            "table-salt.jpg": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/table-salt-E25yAPltz11YBlVHgxSjlToUk4KaEp.jpg",   }
    def download_image(self, filename, url):
        try:
            print(f"Downloading {filename}...", end=" ")
            response = urlopen(url, timeout=10)
            img_data = response.read()
            img = Image.open(io.BytesIO(img_data))
            file_path = self.samples_dir / filename
            img.save(file_path)
            print("✓")
            return True
        except Exception as e:
            print(f" Error: {str(e)}")
            return False
    def setup_all(self):
        print("\n Downloading Virtual SEM Sample Images...\n")
        success_count = 0
        for filename, url in self.images.items():
            if self.download_image(filename, url):
                success_count += 1
        
        print(f"\nDownloaded {success_count}/{len(self.images)} images")
        print(f" Images saved to: {self.samples_dir.absolute()}\n")
        
        if success_count == len(self.images):
            print("Ready to use! Run: python virtual_sem_explorer.py\n")
        else:
            print("Some images failed to download. Check your internet connection.\n")

if __name__ == "__main__":
    setup = ImageSetup()
    setup.setup_all()
