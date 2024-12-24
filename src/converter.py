import os
from pathlib import Path
import subprocess
import logging
import tqdm

class FlacConverter:
    def __init__(self):
        self.check_ffmpeg()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def check_ffmpeg(self):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("ffmpeg not found. Please install ffmpeg first.")
    
    def convert_file(self, input_file: str, output_dir: str) -> bool:
        """Convert a single FLAC file to ALAC format."""
        try:
            input_path = Path(input_file).resolve()
            if not input_path.exists():
                self.logger.error(f"Input file does not exist: {input_path}")
                return False
                
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            output_file = output_path / input_path.name
            output_file = output_file.with_suffix('.m4a')
            
            self.logger.info(f"Converting {input_path} to {output_file}")
            
            result = subprocess.run([
                "ffmpeg",
                "-i", str(input_path),
                "-map", "0:a",
                "-map", "0:v?",
                "-c:a", "alac",
                "-c:v", "copy",
                "-map_metadata", "0",
                "-movflags", "+faststart",
                "-y",
                str(output_file)
            ], capture_output=True, text=True, check=True)
            
            if output_file.exists():
                self.logger.info(f"Successfully converted {input_path}")
                return True
            return False
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error converting {input_path}: {e.stderr}")
            raise RuntimeError(f"Conversion failed: {e.stderr}")
            
    def convert_folder(self, input_dir: str, output_dir: str) -> dict:
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = {'success': [], 'failed': []}
        flac_files = list(input_path.rglob("*.flac"))
        
        for flac_file in tqdm(flac_files, desc="Converting files"):
            relative_path = flac_file.relative_to(input_path)
            output_file = output_path / relative_path.with_suffix('.m4a')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                subprocess.run([
                    "ffmpeg", "-i", str(flac_file),
                    "-map", "0:a", "-map", "0:v?",
                    "-c:a", "alac", "-c:v", "copy",
                    "-map_metadata", "0",
                    "-movflags", "+faststart",
                    "-y", str(output_file)
                ], check=True, capture_output=True)
                results['success'].append(str(flac_file))
            except subprocess.CalledProcessError:
                results['failed'].append(str(flac_file))
                
        return results