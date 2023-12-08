
import numpy as np
import wave

def wav_to_binary_string(file_path):
    # Abrir el archivo .wav
    with wave.open(file_path, 'rb') as wav_file:
        # Obtener los parámetros del archivo
        params = wav_file.getparams()

        # Guarda los datos del archivo en un objeto byte
        audio_data = wav_file.readframes(params.nframes)

        # Pasa el objeto byte a cadena binaria
        binary_data = ''.join(format(byte, '08b') for byte in audio_data)

        print(params)

    return binary_data, params.framerate

def hamming_code(binary_data):
    # Implementa el código de Hamming (7, 4)
    hamming_coded_data = ""

    # Asegúrate de que la longitud de la cadena binaria sea un múltiplo de 4
    binary_data = binary_data[:len(binary_data) - len(binary_data) % 4]

    # Matriz generadora del código de Hamming (7, 4)
    generator_matrix = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [1, 1, 0, 1],
                                 [1, 0, 1, 1],
                                 [0, 1, 1, 1],
                                 [1, 1, 1, 0]])

    # Divide la cadena binaria en segmentos de 4 bits
    for i in range(0, len(binary_data), 4):
        segment = np.array([int(bit) for bit in binary_data[i:i+4]])

        # Ajusta la representación del segmento a una matriz de una sola dimensión
        segment = segment.flatten()

        # Calcula el código de Hamming para cada segmento
        coded_segment = np.dot(segment, generator_matrix.T) % 2

        # Agrega el segmento codificado a la cadena resultante
        hamming_coded_data += ''.join(str(bit) for bit in coded_segment)

    return hamming_coded_data



def modulate_bpsk(binary_data):
    # Modula la señal utilizando Binary Phase Shift Keying (BPSK)
    modulated_signal = []

    for bit in binary_data:
        if bit == '0':
            symbol = -1  # Representa '0' en BPSK
        else:
            symbol = 1   # Representa '1' en BPSK

        # Agrega el símbolo modulado a la señal resultante
        modulated_signal.append(symbol)

    return modulated_signal

def demodulate_bpsk(modulated_signal):
    # Demodula la señal BPSK
    demodulated_signal = []

    for symbol in modulated_signal:
        if symbol < 0:
            demodulated_bit = '0'
        else:
            demodulated_bit = '1'

        # Agrega el bit demodulado a la señal resultante
        demodulated_signal.append(demodulated_bit)

    return demodulated_signal

def binary_to_audio(binary_data, original_rate):
    # Configuración de parámetros del archivo WAV
  sample_width = 2  # ancho de muestra en bytes (2 bytes para formato PCM de 16 bits)
  frame_rate = 44100  # tasa de muestreo en Hz
  duration = 1.0  # duración en segundos

  # Crear un objeto Wave_write
  with wave.open('output.wav', 'wb') as wave_file:

      wave_file.setnchannels(2)  # un canal (mono)
      wave_file.setsampwidth(sample_width)
      wave_file.setframerate(frame_rate)
      wave_file.setnframes(int(frame_rate * duration))

      # Convertir la cadena binaria a bytes para poder restaurar el audio
      binary_data = ''.join(binary_data)
      byte_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

      wave_file.writeframes(byte_data)


if __name__ == "__main__":
    # Ruta del archivo de audio WAV
    audio_file_path = 'Audio.wav'

    # Etapa 1: Convierte el audio a binario
    binary_data, rate = wav_to_binary_string(audio_file_path)
    print(f'binary_data tipo={type(binary_data)} len={len(binary_data)}   {binary_data[:100]}')

    # Etapa 2: Aplica el código de Hamming
    #hamming_coded_data = hamming_code(binary_data)
    #print(f'hamming_coded_data tipo={type(hamming_coded_data)} len={len(hamming_coded_data)}   {hamming_coded_data[:100]}')

    # Etapa 3: Codifica y modula la señal BPSK
    modulated_signal = modulate_bpsk(binary_data) #cambie hamming_coded_data por binary data para agilizar
    print(f'modulated_signal tipo={type(modulated_signal)} len={len(modulated_signal)}   {modulated_signal[:100]}')

    # Etapa 4: Demodula la señal BPSK
    demodulated_signal = demodulate_bpsk(modulated_signal)
    print(f'demodulated_signal tipo={type(demodulated_signal)} len={len(demodulated_signal)}   {demodulated_signal[:100]}')

    # Etapa 5: Convierte la señal binaria de nuevo a audio
    binary_to_audio(demodulated_signal, rate)
