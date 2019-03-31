if __name__ == '__main__':
    from pydub import AudioSegment, exceptions
    import os

    dir_in = '_B_100ishSoundbites/'
    dir_out = '_C_100ishGCPCompat/'

    files = os.listdir(dir_in)
    file_count = len(files)

    for i in range(file_count):
        filename = files[i]

        try:
            speech = AudioSegment.from_wav(dir_in + filename)
        except exceptions.CouldntDecodeError:
            print('Failed to decode ' + filename)

        speech = speech.set_channels(1)

        filename_no_ext = ''.join(filename.split('.')[:-1])
        speech.export(dir_out + filename_no_ext + '.pcm', format = 's16le')

        f = open(dir_out + filename_no_ext + '.meta.txt', 'w')
        f.write(str(speech.frame_rate))
        f.close()
