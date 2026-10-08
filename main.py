import cv2

# ==========================================
# CONFIGURACIÓN
# ==========================================
VIDEO_PATH = "ruta/a/tu/video.mp4"
# Define tu tecla secreta para salir antes de que acabe (Ejemplo: ord('s') para la letra 's', o 27 para 'Esc')
TECLA_SECRETA = ord("j")


def reproducir_video_bloqueado():
  cap = cv2.VideoCapture(VIDEO_PATH)

  if not cap.isOpened():
    print("Error: No se pudo abrir el video :( .")
    return

  window_name = "Reproductor Bloqueado"
  cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
  cv2.setWindowProperty(
      window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
  )

  # Calcular el tiempo de espera por frame basado en los FPS del video para que corra a velocidad real
  fps = cap.get(cv2.CAP_PROP_FPS)
  if fps <= 0:
    fps = 30  # Valor por defecto si no se detectan los FPS
  delay = int(1000 / fps)

  while cap.isOpened():
    ret, frame = cap.read()

    # Si el video termina, se cierra automáticamente
    if not ret:
      break

    cv2.imshow(window_name, frame)

    # Leemos la tecla presionada (esperando el delay calculado por frame)
    key = cv2.waitKey(delay) & 0xFF

    # 1. Si presionan la tecla secreta, salimos antes de tiempo
    if key == TECLA_SECRETA:
      print("Cierre forzado.")
      break

    # 2. Cualquier otra tecla es ignorada por completo (no hace nada)

  cap.release()
  cv2.destroyAllWindows()


if __name__ == "__main__":
  reproducir_video_bloqueado()
