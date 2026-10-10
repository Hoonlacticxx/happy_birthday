import tkinter as tk
import vlc
import os
import sys
import keyboard
import time
import threading

# =========================================================
# CONFIGURACIÓN
# =========================================================

VIDEO_FILE = "video.mp4"
VOLUMEN = 0.15

activo = True
player = None
root = None


# =========================================================
# RUTA DEL VIDEO (PYTHON Y EXE)
# =========================================================

def ruta_archivo(nombre):
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, nombre)


# =========================================================
# CERRAR PROGRAMA
# =========================================================

def detener_todo():
    global activo

    if not activo:
        return

    activo = False

    try:
        keyboard.unhook_all()
    except Exception:
        pass

    def cerrar():
        try:
            if player:
                player.stop()
        except Exception:
            pass

        try:
            root.destroy()
        except Exception:
            pass

    try:
        root.after(0, cerrar)
    except Exception:
        pass


# =========================================================
# INICIAR VIDEO
# =========================================================

def iniciar_video():
    global player

    try:
        ruta_video = ruta_archivo(VIDEO_FILE)

        if not os.path.isfile(ruta_video):
            print(f"No se encontró el video: {ruta_video}")
            return

        instancia_vlc = vlc.Instance(
            "--no-video-title-show",
            "--input-repeat=-1"
        )

        player = instancia_vlc.media_player_new()

        media = instancia_vlc.media_new(ruta_video)
        player.set_media(media)

        # Preparar la ventana de video
        root.update_idletasks()
        player.set_hwnd(root.winfo_id())

        # Reproducir automáticamente
        player.play()

    except Exception as e:
        print("Error al reproducir el video:", e)


# =========================================================
# CONTROL DE VOLUMEN
# =========================================================

def configurar_volumen():
    try:
        from pycaw.pycaw import AudioUtilities

        dispositivos = AudioUtilities.GetSpeakers()
        volumen = dispositivos.EndpointVolume

        # Desmutear y establecer volumen inicial
        volumen.SetMute(0, None)
        volumen.SetMasterVolumeLevelScalar(VOLUMEN, None)

        print(f"Volumen establecido al {int(VOLUMEN * 100)}%")

    except Exception as e:
        print("No se pudo controlar el volumen:", e)


def vigilar_volumen():
    """
    Mientras el programa esté activo en segundo plano:
    - Mantiene el volumen configurado y quita el mute si lo activan.
    """
    try:
        import comtypes
        from pycaw.pycaw import AudioUtilities

        # Inicializar COM para este hilo de Windows
        comtypes.CoInitialize()

        dispositivos = AudioUtilities.GetSpeakers()
        volumen = dispositivos.EndpointVolume

        while activo:
            try:
                # Forzar siempre el desmuteo y restaurar el volumen deseado
                volumen.SetMute(0, None)
                volumen.SetMasterVolumeLevelScalar(VOLUMEN, None)
            except Exception:
                pass

            time.sleep(0.2)

    except Exception as e:
        print("Error vigilando volumen:", e)
    finally:
        try:
            comtypes.CoUninitialize()
        except Exception:
            pass


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

root = tk.Tk()

root.title("feliz cumpleaños papu")
root.configure(bg="black")

# Pantalla completa real, sin barra de tareas ni bordes
root.attributes("-fullscreen", True)

# Ocultar el cursor dentro de la ventana
root.configure(cursor="none")

# Evitar que el usuario la cierre accidentalmente
root.protocol("WM_DELETE_WINDOW", lambda: None)

# Mantener el video en pantalla
root.attributes("-topmost", True)


# =========================================================
# ATAJO PARA SALIR
# =========================================================

keyboard.add_hotkey(
    "h+b",
    detener_todo,
    suppress=True
)


# =========================================================
# INICIAR HILO DE VOLUMEN Y REPRODUCCIÓN
# =========================================================

# Configurar volumen inicial
configurar_volumen()

# Lanzar el vigilante en un hilo separado
hilo_volumen = threading.Thread(target=vigilar_volumen, daemon=True)
hilo_volumen.start()

# Iniciar reproducción del video tras medio segundo
root.after(500, iniciar_video)


# =========================================================
# EJECUTAR PROGRAMA
# =========================================================

try:
    root.mainloop()

finally:
    activo = False

    try:
        keyboard.unhook_all()
    except Exception:
        pass

    try:
        if player:
            player.stop()
            player.release()
    except Exception:
        pass