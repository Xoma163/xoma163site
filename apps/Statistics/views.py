from apps.Statistics.models import Statistics


def append_command_to_statistics(command):
    statistics = Statistics.objects.filter(command=command).first()
    if statistics:
        statistics.count_queries += 1
        statistics.save()
    else:
        statistics = Statistics()
        statistics.command = command
        statistics.count_queries = 1
        statistics.save()
