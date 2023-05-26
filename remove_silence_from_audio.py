from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent


def remove_silence(input_file_path, output_file_path):
    # load audio file
    audio_file = AudioSegment.from_wav(input_file_path)

    # calculate average dBFS level of the audio file
    average_dBFS = audio_file.dBFS

    # set silence threshold to the average dBFS level
    silence_thresh = int(average_dBFS)

# calculate min_silence_len based on audio file length
    audio_length_ms = len(audio_file)
    m = 0.05  # percentage of audio length
    min_silence_len = int(audio_length_ms * m)  # set to 10% of audio length

    # split audio on silence
    nonsilent_parts = detect_nonsilent(
        audio_file, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # combine parts containing coughs
    combined_audio = AudioSegment.empty()
    for part in nonsilent_parts:
        if part[1] - part[0] > min_silence_len:
            combined_audio = combined_audio + audio_file[part[0]:part[1]]

    # export output file
    combined_audio.export(output_file_path, format="wav")


input_file_path = 'C:/Users/LENOVO/Desktop/RemoveNoise/RemoveNoise/Recording.wav'
output_file_path = 'output.wav'

remove_silence(input_file_path, output_file_path)
