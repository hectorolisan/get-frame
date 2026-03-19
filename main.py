#!/usr/bin/env python3

import argparse
import cv2
import numpy as np
import sys

from imgcat import imgcat
from io import BytesIO
from pathlib import Path
from typing import Optional

from decorators import handle_errors, print_styled

OUTPUT_DIR = Path("output")

@handle_errors("Error al validar el frame")
def validate_frame(
    video: cv2.VideoCapture,
    frame_number: int
) -> None:
    """
    Verifica que el frame sea válido.
    """
    total_frames: int = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if (frame_number < 1) or (total_frames < frame_number):
        raise ValueError(
            f"({frame_number}) Debe ser mayor a 0 y menor a {total_frames}."
        )

@handle_errors("Error al extraer el frame del video")
def extract_frame(
    video: cv2.VideoCapture,
    frame_number: int
) -> np.ndarray:
    """
    Obtiene el frame especificado del video.
    """
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    ret: bool
    frame: np.ndarray
    ret, frame = video.read()
    if not ret: raise ValueError()
    return frame

@handle_errors("Error al guardar el frame como PNG")
def save_frame_as_png(
    frame: np.ndarray,
    video_path: str,
) -> Path:
    """
    Construye la ruta y guarda el frame como PNG.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    video_path_obj: Path = Path(video_path)
    filename: str = video_path_obj.stem
    frame_path: Path = OUTPUT_DIR / f"{filename}.png"

    cv2.imwrite(str(frame_path), frame)
    return frame_path

@handle_errors("Error al mostrar el frame en la terminal")
def display_frame_in_terminal(frame: np.ndarray) -> None:
    """Muestra el frame en la terminal usando imgcat."""
    frame_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgcat(data=frame_rgb, height=20)

@handle_errors("Error al obtener frame del video")
def get_frame(
    video_path: str,
    frame_number: int = 10,
) -> Path:
    """
    Extrae un frame específico de un video y lo guarda como PNG.
    """
    video: cv2.VideoCapture = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"No se pudo abrir ({video_path})")

    try:
        validate_frame(
            video=video,
            frame_number=frame_number
        )

        frame: np.ndarray = extract_frame(
            video=video, frame_number=frame_number
        )

        frame_path: Path = save_frame_as_png(
            frame=frame,
            video_path=video_path
        )

        print_styled(
            message=f"✓ Frame ({frame_number}) extraído correctamente: {frame_path}\n",
            color="green"
        )

        display_frame_in_terminal(frame=frame)

    finally:
        video.release()

def main() -> None:
    """Función principal que maneja la ejecución del script."""
    if len(sys.argv) != 3:
        print_styled(
            message="Número de argumentos inválido\n",
            error_type="ValueError",
            color="red"
        )
        print_styled(
            message="📖 Uso: python main.py <video_path> <frame_number>",
            color="cyan"
        )
        print_styled(
            message="📝 Ejemplo: python main.py video.mp4 10",
            color="cyan"
        )
        sys.exit(1)

    video_path: str = sys.argv[1]
    frame_number: int = int(sys.argv[2])
    get_frame(video_path=video_path, frame_number=frame_number)

if __name__ == "__main__":
    main()
