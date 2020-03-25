from progress.spinner import Spinner
from progressbar import RotatingMarker, ProgressBar
from time import sleep

if __name__ == '__main__':
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