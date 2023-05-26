from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent


class RemoveSilenceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Remove Silence')
        self.master.geometry('400x200')
        self.master.configure(bg='black')

        # create browse button
        self.browse_button = Button(
            self.master, text='Browse', command=self.browse_file)
        self.browse_button.place(x=20, y=20)

        # create remove silence button
        self.remove_button = Button(
            self.master, text='Remove Silence', command=self.remove_silence)
        self.remove_button.place(x=20, y=80)

        # create file label
        self.file_label = Label(
            self.master, text='No file selected', bg='black', fg='white')
        self.file_label.place(x=110, y=25)

        # create status label
        self.status_label = Label(
            self.master, text='Ready', bg='black', fg='white')
        self.status_label.place(x=180, y=85)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title='Select Audio File', filetypes=[('Audio Files', '*.wav')])

        if file_path:
            self.file_label.config(text=file_path)

    def remove_silence(self):
        input_file_path = self.file_label.cget('text')
        output_file_path = 'output.wav'

        if input_file_path:
            # load audio file
            audio_file = AudioSegment.from_wav(input_file_path)

            # calculate average dBFS level of the audio file
            average_dBFS = audio_file.dBFS

            # set silence threshold to the average dBFS level
            silence_thresh = int(average_dBFS)

            # calculate min_silence_len based on audio file length
            audio_length_ms = len(audio_file)
            m = 0.05  # percentage of audio length
            # set to 10% of audio length
            min_silence_len = int(audio_length_ms * m)

            # split audio on silence
            nonsilent_parts = detect_nonsilent(
                audio_file, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

            # combine parts containing coughs
            combined_audio = AudioSegment.empty()
            for part in nonsilent_parts:
                if part[1] - part[0] > min_silence_len:
                    combined_audio = combined_audio + \
                        audio_file[part[0]:part[1]]

            # export output file
            combined_audio.export(output_file_path, format="wav")

            # update status label
            self.status_label.config(text='Silence removed successfully')


if __name__ == '__main__':
    root = Tk()
    RemoveSilenceGUI(root)
    root.mainloop()
