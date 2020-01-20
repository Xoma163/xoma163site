from apps.Statistics.models import Statistic, Issue


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
    feature = Issue()
    feature.text = text
    feature.save()


def get_issues_text():
    issues = Issue.objects.all()
    features_text = "Добавленные ишю:\n\n"
    for i, feature in enumerate(issues):
        features_text += f"------------------------------{i + 1}------------------------------\n" \
            f"{feature.text}\n"
    return features_text
