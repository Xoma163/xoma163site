from apps.Statistics.models import Statistic, Isssue


def append_command_to_statistics(command):
    statistics = Statistic.objects.filter(command=command).first()
    if statistics:
        statistics.count_queries += 1
        statistics.save()
    else:
        statistics = Statistic()
        statistics.command = command
        statistics.count_queries = 1
        statistics.save()


def append_feature(text):
    feature = Isssue()
    feature.text = text
    feature.save()


def get_issues_text():
    issues = Isssue.objects.all()
    features_text = "Добавленные ишю:\n\n"
    for i, feature in enumerate(issues):
        features_text += "------------------------------{}------------------------------\n" \
                         "{}\n".format(i + 1, feature.text)
    return features_text
