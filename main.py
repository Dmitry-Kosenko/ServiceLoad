import csv

reference_day = {}  # Эталонный день
high_load_day = {}  # День с высокой нагрузкой


def read_csv(file: str):
    out_dict = {}
    with open(file, encoding='utf-8-sig') as r_file:
        # Создаем словарь из CSV файла
        file_reader = csv.DictReader(r_file, delimiter=";")
        # Считывание данных из словаря в более удобный вид
        for row in file_reader:
            out_dict[row["Метод"]] = dict(duration_sum=int(row["Общая продолжительность (мс)"]),
                                          duration_avg=float(row["Средняя продолжительность (мс)"].replace(',', '.')),
                                          call_count=int(row["Количество вызовов"]),
                                          duration_max=int(row["Максимальная продолжительность (мс)"]),
                                          responsible=row["ОтветственныйЗаМетод"][2:-2])
    return out_dict


def compare_days(reference, high_load):
    duration_all = 0
    result_dict = {}
    # считаем общую продолжительность выполнения всех методов эталонного дня
    for i in reference:
        duration_all += reference[i]['duration_sum']
    # для каждого метода из дня высокой нагрузки
    for method in high_load:
        # проверяем есть ли метод в эталонном дне
        if reference.get(method, 'not found') != 'not found':
            # метод есть - работаем
            # общее время выполнения нагрузки; эталона; разница; разница в %; разница в % от суммы общего времени вып. всех методов
            result_dict[method] = dict(hi_duration_sum=high_load[method]['duration_sum'],
                                       ref_duration_sum=reference[method]['duration_sum'],
                                       diff_duration_sum=high_load[method]['duration_sum'] - reference[method]['duration_sum'],
                                       diff_perc_duration_sum=round(
                                           ((high_load[method]['duration_sum'] - reference[method]['duration_sum']) / reference[method]['duration_sum'] * 100), 2),
                                       diff_perc_duration_all=round(((high_load[method]['duration_sum'] - reference[method]['duration_sum']) / duration_all * 100), 2),
                                       # среднее время выполнения нагрузки; эталона; разница; разница в %
                                       hi_duration_avg=high_load[method]['duration_sum'],
                                       ref_duration_avg=reference[method]['duration_sum'],
                                       diff_duration_avg=round(high_load[method]['duration_avg'] - reference[method]['duration_avg'], 2),
                                       diff_perc_duration_avg=round(
                                           ((high_load[method]['duration_avg'] - reference[method]['duration_avg']) / reference[method]['duration_avg'] * 100), 2),
                                       # количество вызовов в нагрузке; эталоне; разница; разница в %
                                       hi_call_count=reference[method]['call_count'],
                                       ref_call_count=reference[method]['call_count'],
                                       call_count_diff=high_load[method]['call_count'] - reference[method]['call_count'],
                                       call_count_diff_perc=round(((high_load[method]['call_count'] - reference[method]['call_count']) / reference[method][
                                           'call_count'] * 100), 2),
                                       # максимальное время выполнения метода в нагрузке; эталоне; разница; разница в %
                                       hi_duration_max=high_load[method]['duration_max'],
                                       ref_duration_max=reference[method]['duration_max'],
                                       duration_max_diff=high_load[method]['duration_max'] - reference[method]['duration_max'],
                                       duration_max_diff_perc=round(((high_load[method]['duration_max'] - reference[method]['duration_max']) / reference[method][
                                           'duration_max'] * 100), 2),
                                       # ответственный за метод
                                       responsible=high_load[method]['responsible'])
        else:
            # метод не найден (новый метод) - не учитываем его
            print(f"Метод {method} не найден в эталоне")
    return result_dict


def sort_dict(src_dict: dict):
    sorted_tuples = sorted(src_dict.items(), key=lambda item: item[1].get('diff_perc_duration_all', 0), reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    for i in sorted_dict:
        print(sorted_dict[i])


if __name__ == '__main__':
    reference_day = read_csv('эталон1.csv')
    high_load_day = read_csv('нагрузка1.csv')
    sort_dict(compare_days(reference_day, high_load_day))
