import subprocess


def do_the_linux_command(command):
    try:
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode("utf-8")
        if error:
            output += "\nОшибка:\n{}".format(error)
    except Exception as e:
        output = str(e)
    return output
