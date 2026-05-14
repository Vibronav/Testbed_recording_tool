import wave
from pathlib import Path


def ensure_output_structure(output_folder):
    output_path = Path(output_folder)
    (output_path / "audio").mkdir(parents=True, exist_ok=True)
    return output_path


def prepare_output_folder(output_folder):
    output_path = ensure_output_structure(output_folder)
    return find_reference_chirp(output_path)


def find_reference_chirp(output_folder):
    reference_path = Path(output_folder) / "reference"
    if not reference_path.is_dir():
        raise FileNotFoundError(f"Missing reference folder: {reference_path}")

    files = sorted(path for path in reference_path.iterdir() if path.is_file())
    if not files:
        raise FileNotFoundError(f"No chirp file found in reference folder: {reference_path}")
    if len(files) > 1:
        names = ", ".join(path.name for path in files)
        raise ValueError(f"Expected exactly one chirp file in {reference_path}, found: {names}")

    chirp_path = files[0]
    if chirp_path.suffix.lower() != ".wav":
        raise ValueError(f"Reference chirp must be a wav file: {chirp_path}")

    return chirp_path


def get_wav_sample_rate(path):
    with wave.open(str(path), "rb") as wav:
        return wav.getframerate()
