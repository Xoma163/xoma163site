from apps.Statistics.models import Statistic, Feature


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
    feature = Feature()
    feature.text = text
    feature.save()


def get_features_text():
    features = Feature.objects.all()
    features_text = "Добавленные фичи:\n\n"
    for i, feature in enumerate(features):
        features_text += "------------------------------{}------------------------------\n" \
                         "{}\n".format(i + 1, feature.text)
    return features_text
