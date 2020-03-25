from progress.spinner import Spinner
from progressbar import RotatingMarker, ProgressBar
from time import sleep

if __name__ == '__main__':

    import time
    import progressbar


    def custom_len(value):
        # These characters take up more space
        characters = {'进': 2, '度': 2, }

        total = 0
        for c in value:
            total += characters.get(c, 1)

        return total


    bar = progressbar.ProgressBar(widgets=['进度: ', progressbar.Bar(), ' ',
        progressbar.Counter(format='%(value)02d/%(max_value)d'), ],
        len_func=custom_len, )
    for i in bar(range(10)):
        time.sleep(0.1)


    bar = ProgressBar(max_value=10).start()
    for i in range(11):
        bar.update(i)

    spinner = Spinner('Loading')
    for i in range(21):
        sleep(0.25)
        spinner.next()

    print('')
    spinner2 = RotatingMarker()
    for i in range(21):
        spinner2.update(i)
        sleep(0.25)