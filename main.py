import cv2

VIDEO_PATH = "video.mp4"

KEYBIND = ord("j")


def reproducir_video_bloqueado():
  cap = cv2.VideoCapture(VIDEO_PATH)

  if not cap.isOpened():
    print("Error: No se pudo abrir el video :( ")
    return

  window_name = "happy birthdayyy"
  cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
  cv2.setWindowProperty(
      window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
  )

  # Calcular el tiempo de espera entre frames para mostrar el video a velocidad normal (fluido)
  fps = cap.get(cv2.CAP_PROP_FPS)
  if fps <= 0:
    fps = 30  # Por defecto si no se detectan los FPS
  delay = int(1000 / fps)

  while cap.isOpened():
    ret, frame = cap.read()

    # Si el video termina, se cierra en auto
    if not ret:
      break

    cv2.imshow(window_name, frame)

    # Revisa la keybind dando la misma espera que el intervalo de frames
    key = cv2.waitKey(delay) & 0xFF

    # 1. Si presionan la keybind, se cierra el programa
    if key == KEYBIND:
      print("Cierre forzado")
      break

    # 2. Cualquier otra tecla es ignorada por completo (no hace nada)

  cap.release()
  cv2.destroyAllWindows()


if __name__ == "__main__":
  reproducir_video_bloqueado()
