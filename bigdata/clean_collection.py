import pandas as pd
import re
import json
from sklearn.preprocessing import LabelEncoder
import os
import datetime


def clean_activity_learn_log(df):
    # 定义函数来处理data列中的字符串
    def remove_fields(text):
        json_data = json.loads(text)
        fields_to_remove = ['taskId', 'event', 'learnedTime']
        for field in fields_to_remove:
            if field in json_data:
                del json_data[field]
        return json.dumps(json_data)

    # 对data列中的每个字符串应用函数
    df['data'] = df['data'].apply(remove_fields)
    print(f"清除了 activity_learn_log.csv 的 data 列中的冗余信息")

    # # 缺失值处理：删除缺失的行
    # print("删除activity_learn_log.csv中存在不允许的NaN值的行")
    # missing_values = df.isnull().sum()
    # print(missing_values)
    # missing_rows = df[df.isnull().any(axis=1)]
    # print(missing_rows)
    # df = df.dropna()

    # 输出编码映射
    print("下面是 activity_learn_log.csv的编码映射")
    mediaType_label_encoder = LabelEncoder()
    mediaType_labels = df['mediaType'].unique()
    mediaType_mapping = dict(zip(mediaType_labels, mediaType_label_encoder.fit_transform(mediaType_labels)))

    event_label_encoder = LabelEncoder()
    event_labels = df['event'].unique()
    event_mapping = dict(zip(event_labels, event_label_encoder.fit_transform(event_labels)))

    print("mediaType 编码映射:", mediaType_mapping)
    print("event 编码映射: ", event_mapping)

    # 对列进行编码
    df.loc[:, 'mediaType'] = df['mediaType'].map(mediaType_mapping)
    df.loc[:, 'event'] = df['event'].map(event_mapping)


def clean_classroom_courses(df):
    # 缺失值处理：删除缺失的行
    print("删除classroom_courses中存在不允许的NaN值的行")
    missing_values = df.isnull().sum()
    print(missing_values)
    missing_rows = df[df.isnull().any(axis=1)]
    print(missing_rows)
    df = df.dropna()


def clean_classroom_member(df):
    # 缺失值处理：删除缺失的行
    print("删除classroom_member中存在不允许的NaN值的行")
    missing_values = df.isnull().sum()
    print(missing_values)
    rows_before = len(df)
    # lastLearnTime 和 learnedNum 在数据说明中允许为空
    # 删除除了 'lastLearnTime' 和 'learnedNum' 列之外，其他列存在 NaN 值的行
    columns_to_check = df.columns.difference(['lastLearnTime', 'learnedNum'])
    df = df.dropna(subset=columns_to_check)
    # 计算删除了多少行
    rows_deleted = rows_before - len(df)
    print(f"删除了 {rows_deleted} 行存在空值的数据")

    # 特殊处理：删除不包含老师的班级的所有信息
    teacher_classrooms = df[df['role'].str.contains('eacher')]
    # 提取老师所在的班级 ID
    teacher_classrooms_ids = teacher_classrooms['classroomId'].unique()
    non_teacher_classrooms_ids = df[~df['classroomId'].isin(teacher_classrooms_ids)]['classroomId'].unique()
    print("删除不包含老师的班级的 classroomId：", non_teacher_classrooms_ids)
    # 删除 classroom_member 中不包含老师的班级
    df = df[df['classroomId'].isin(teacher_classrooms_ids)]


def clean_course_chapter(df):
    # 缺失值处理：删除缺失的行
    print("删除course_chapter.csv中存在不允许的NaN值的行")
    missing_values = df.isnull().sum()
    print(missing_values)
    missing_rows = df[df.isnull().any(axis=1)]
    print(missing_rows)
    df = df.dropna()

    # 输出编码映射
    print("下面是 course_chapter.csv的编码映射")
    status_label_encoder = LabelEncoder()
    status_labels = df['status'].unique()
    status_mapping = dict(zip(status_labels, status_label_encoder.fit_transform(status_labels)))

    type_label_encoder = LabelEncoder()
    type_labels = df['type'].unique()
    type_mapping = dict(zip(type_labels, type_label_encoder.fit_transform(type_labels)))

    print("status 编码映射:", status_mapping)
    print("type 编码映射:", type_mapping)

    # 对列进行编码
    df.loc[:, 'status'] = df['status'].map(status_mapping)
    df.loc[:, 'type'] = df['type'].map(type_mapping)


def clean_course_task(df):
    # 缺失值处理：删除缺失的行
    print("删除course_task.csv中存在不允许的NaN值的行")
    missing_values = df.isnull().sum()
    print(missing_values)

    rows_before = len(df)
    # number 和 mode 在数据说明中允许为空
    # 删除除了 'number' 和 'mode' 列之外，其他列存在 NaN 值的行
    columns_to_check = df.columns.difference(['number', 'mode'])
    df = df.dropna(subset=columns_to_check)
    # 计算删除了多少行
    rows_deleted = rows_before - len(df)
    print(f"删除了 {rows_deleted} 行存在空值的数据")

    # 将 df['status'] 列中所有值为 "create" 的替换为 "created"
    status_replace_count = (df['status'] == "created").sum()
    df['status'] = df['status'].replace("create", "created")
    status_replaced_count = (df['status'] == "created").sum()
    # 打印结果
    print(f"替换了{status_replaced_count - status_replace_count}列 create 为 created")

    print("下面是 course_task.csv 的编码映射")
    # 输出编码映射
    status_label_encoder = LabelEncoder()
    status_labels = df['status'].unique()
    status_mapping = dict(zip(status_labels, status_label_encoder.fit_transform(status_labels)))

    mode_label_encoder = LabelEncoder()
    mode_labels = df['mode'].unique()
    mode_mapping = dict(zip(mode_labels, mode_label_encoder.fit_transform(mode_labels)))

    type_label_encoder = LabelEncoder()
    type_labels = df['type'].unique()
    type_mapping = dict(zip(type_labels, type_label_encoder.fit_transform(type_labels)))

    print("status 编码映射:", status_mapping)
    print("mode 编码映射: ", mode_mapping)
    print("type 编码映射:", type_mapping)

    # 对列进行编码
    df.loc[:, 'status'] = df['status'].map(status_mapping)
    df.loc[:, 'mode'] = df['mode'].map(mode_mapping)
    df.loc[:, 'type'] = df['type'].map(type_mapping)


def clean_log(df):
    # 清除浏览器的详细版本信息，只保留浏览器类型，方便编码
    print("清除了browser的版本信息，只保留浏览器名称")
    def remove_content_between_parentheses(text):
        return re.sub(r'\(.*?\)', '', text)

    df['browser'] = df['browser'].apply(remove_content_between_parentheses)

    print("下面是 log.csv 的编码映射")
    # 输出编码映射
    module_label_encoder = LabelEncoder()
    module_labels = df['module'].unique()
    module_mapping = dict(zip(module_labels, module_label_encoder.fit_transform(module_labels)))

    action_label_encoder = LabelEncoder()
    action_labels = df['action'].unique()
    action_mapping = dict(zip(action_labels, action_label_encoder.fit_transform(action_labels)))

    browser_label_encoder = LabelEncoder()
    browser_labels = df['browser'].unique()
    browser_mapping = dict(zip(browser_labels, browser_label_encoder.fit_transform(browser_labels)))

    operatingSystem_label_encoder = LabelEncoder()
    operatingSystem_labels = df['operatingSystem'].unique()
    operatingSystem_mapping = dict(
        zip(operatingSystem_labels, operatingSystem_label_encoder.fit_transform(operatingSystem_labels)))

    device_label_encoder = LabelEncoder()
    device_labels = df['device'].unique()
    device_mapping = dict(zip(device_labels, device_label_encoder.fit_transform(device_labels)))

    level_label_encoder = LabelEncoder()
    level_labels = df['level'].unique()
    level_mapping = dict(zip(level_labels, level_label_encoder.fit_transform(level_labels)))

    print("module 编码映射:", module_mapping)
    print("action 编码映射: ", action_mapping)
    print("browser 编码映射:", browser_mapping)
    print("operatingSystem 编码映射:", operatingSystem_mapping)
    print("device 编码映射: ", device_mapping)
    print("level 编码映射:", level_mapping)

    # 对列进行编码
    df.loc[:, 'module'] = df['module'].map(module_mapping)
    df.loc[:, 'action'] = df['action'].map(action_mapping)
    df.loc[:, 'browser'] = df['browser'].map(browser_mapping)
    df.loc[:, 'operatingSystem'] = df['operatingSystem'].map(operatingSystem_mapping)
    df.loc[:, 'device'] = df['device'].map(device_mapping)
    df.loc[:, 'level'] = df['level'].map(level_mapping)


def clean_testpaper(df):
    # 定义函数来处理metas列中的字符串
    def remove_total_scores(text):
        json_df = json.loads(text)
        if 'totalScores' in json_df:
            del json_df['totalScores']
        return json.dumps(json_df)

    # 对score为0且metas列不为NaN的行的metas列中的每个字符串应用函数
    df.loc[(df['score'] == 0) & (~df['metas'].isna()), 'metas'] = df.loc[
        (df['score'] == 0) & (~df['metas'].isna()), 'metas'].apply(remove_total_scores)

    print("下面是 testpaper.csv 的编码映射")
    # 输出编码映射
    status_label_encoder = LabelEncoder()
    status_labels = df['status'].unique()
    status_mapping = dict(zip(status_labels, status_label_encoder.fit_transform(status_labels)))

    type_label_encoder = LabelEncoder()
    type_labels = df['type'].unique()
    type_mapping = dict(zip(type_labels, type_label_encoder.fit_transform(type_labels)))

    print("status 编码映射:", status_mapping)
    print("type 编码映射:", type_mapping)

    # 对列进行编码
    df.loc[:, 'status'] = df['status'].map(status_mapping)
    df.loc[:, 'type'] = df['type'].map(type_mapping)


def clean_testpaper_result(df):
    # 特殊处理
    # 判断score列是否等于objectiveScore和subjectiveScore列的和
    unequal_rows = df[df['score'] != df['objectiveScore'] + df['subjectiveScore']]
    print(f"testpaper_result.csv中有 {len(unequal_rows)} 行 score != objectiveScore + subjectiveScore")
    df.loc[unequal_rows.index, 'score'] = unequal_rows['objectiveScore'] + unequal_rows['subjectiveScore']
    print("将score用后二者之和覆盖")

    print("下面是 testpaper_result.csv 的编码映射")
    # 输出编码映射
    status_label_encoder = LabelEncoder()
    status_labels = df['status'].unique()
    status_mapping = dict(zip(status_labels, status_label_encoder.fit_transform(status_labels)))

    type_label_encoder = LabelEncoder()
    type_labels = df['type'].unique()
    type_mapping = dict(zip(type_labels, type_label_encoder.fit_transform(type_labels)))

    passedStatus_label_encoder = LabelEncoder()
    passedStatus_labels = df['passedStatus'].unique()
    passedStatus_mapping = dict(zip(passedStatus_labels, passedStatus_label_encoder.fit_transform(passedStatus_labels)))

    print("status 编码映射:", status_mapping)
    print("type 编码映射:", type_mapping)
    print("passedStatus 编码映射:", passedStatus_mapping)

    # 对列进行编码
    df.loc[:, 'status'] = df['status'].map(status_mapping)
    df.loc[:, 'type'] = df['type'].map(type_mapping)
    df.loc[:, 'passedStatus'] = df['passedStatus'].map(passedStatus_mapping)


def clean_user_learn_statistics(df):
    print("删除user_learn_statistics.csv中存在不允许的NaN值的行")
    # 缺失值处理：删除缺失的行
    missing_values = df.isnull().sum()
    print(missing_values)
    missing_rows = df[df.isnull().any(axis=1)]
    print(missing_rows)
    df = df.dropna()


def wash_file(file_path, file_name):

    """
    数据清洗的总函数入口
    :param file_path：传入待清洗的csv文件的路径(在update_file中处理为MEDIA_ROOT/file.name)
    :type file_path: str
    :param file_name: 传入待清洗的csv文件本身的文件名(update_file中的file.name)
    :type file_name: str
    """

    data = pd.read_csv(file_path, low_memory=False)
    # ============================ 默认清洗：删除数值完全相同的列 ============================
    if file_name == "activity_learn_log.csv":
        print(f"{file_name} 中值都相同的列: []")
    else:
        unique_value_counts = data.nunique()
        columns_with_same_values = unique_value_counts[unique_value_counts == 1].index.tolist()
        print(f"{file_name} 中值都相同的列: {columns_with_same_values}")
        data.drop(columns=columns_with_same_values, inplace=True)

    # ============================ 默认清洗：删除没有利用价值的列 ============================
    useless_columns = {
        "activity_learn_log.csv": [],
        "classroom_courses.csv": ['courseSetId'],
        "classroom_member.csv": ['createdTime', 'updatedTime', 'deadline', 'refundDeadline', 'deadlineNotified', 'levelId'],
        "course_chapter.csv": ['createdTime', 'updatedTime', 'published_number'],
        "course_task.csv": ['createdTime', 'updatedTime', 'startTime', 'endTime', 'createdUserId', 'fromCourseSetId', 'activityId', 'categoryId'],
        "log.csv": [],
        "testpaper.csv": ['courseSetId', 'createdTime', 'updatedTime', 'target'],
        "testpaper_result.csv": ['courseSetId', 'beginTime', 'endTime', 'updateTime', 'checkTeacherId', 'checkedTime', 'metas'],
        "user_learn_statistics_total.csv" : ['createdTime', 'updatedTime']
    }
    print(f"{file_name} 中没用利用价值的列: {useless_columns[file_name]}")
    data.drop(columns=useless_columns[file_name], inplace=True)

    # ============================= 默认清洗：删除完全相同的行 =============================
    # log要进行特殊处理
    initial_length = len(data)
    if file_name == "log.csv":
        data.drop_duplicates(subset=data.columns.difference(['id', 'data']), keep='last', inplace=True)
        deleted_entries = initial_length - len(data)
        print("{} 中存在 {} 条目除了'id'列和'data'列之外完全相同".format(file_name, deleted_entries))
    else:
        data.drop_duplicates(subset=data.columns.difference(['id']), keep='last', inplace=True)
        deleted_entries = initial_length - len(data)
        print("{} 中存在 {} 条目除了'id'列之外完全相同".format(file_name, deleted_entries))

    # =========================== 特殊处理：根据文件名输入不同的函数 ===========================
    if file_name == "activity_learn_log.csv":
        clean_activity_learn_log(data)
    elif file_name == "classroom_courses.csv":
        clean_classroom_courses(data)
    elif file_name == "classroom_member.csv":
        clean_classroom_member(data)
    elif file_name == "course_chapter.csv":
        clean_course_chapter(data)
    elif file_name == "course_task.csv":
        clean_course_task(data)
    elif file_name == "log.csv":
        clean_log(data)
    elif file_name == "testpaper.csv":
        clean_testpaper(data)
    elif file_name == "testpaper_result.csv":
        clean_testpaper_result(data)
    elif file_name == "user_learn_statistics_total.csv":
        clean_user_learn_statistics(data)

    # 保存数据：

    current_datetime = datetime.datetime.now()
    # 提取年、月、日信息
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day

    folder_path = f"./data_new/{year}_{month}_{day}/"
    os.makedirs(folder_path, exist_ok=True)

    if file_name == "course_chapter.csv" or file_name == "course_task.csv":
        # 特殊处理：拆分了title列，节约内存，加快处理速度
        selected_columns = ['id', 'title']
        selected_data = data[selected_columns]
        save_path1 = folder_path + file_name[:-4] + '_new(2).csv'
        selected_data.to_csv(save_path1, index=False)

        data.drop(columns=['title'], inplace=True)
        save_path2 = folder_path + file_name[:-4] + '_new.csv'
        data.to_csv(save_path2, index=False)

        print(f"新数据已拆分title列保存至 {save_path1} 和 {save_path2}")

    elif file_name == "testpaper.csv":
        selected_columns = ['id', 'name']
        selected_data = data[selected_columns]
        save_path1 = folder_path + file_name[:-4] + '_new(2).csv'
        selected_data.to_csv(save_path1, index=False)

        data.drop(columns=['name'], inplace=True)
        save_path2 = folder_path + file_name[:-4] + '_new.csv'
        data.to_csv(save_path2, index=False)

        print(f"新数据已拆分name列保存至 {save_path1} 和 {save_path2}")
    elif file_name == "testpaper_result.csv":
        selected_columns = ['id', 'paperName']
        selected_data = data[selected_columns]
        save_path1 = folder_path + file_name[:-4] + '_new(2).csv'
        selected_data.to_csv(save_path1, index=False)

        data.drop(columns=['paperName'], inplace=True)
        save_path2 = folder_path + file_name[:-4] + '_new.csv'
        data.to_csv(save_path2, index=False)

        print(f"新数据已拆分paperName列保存至 {save_path1} 和 {save_path2}")
    else:
        save_path = folder_path + file_name[:-4] + "_new.csv"
        data.to_csv(save_path, index=False)
        print(f"新数据已保存至 {save_path}")


def main():
    def list_csv_files(directory):
        csv_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    relative_path_with_prefix = os.path.join("..", "data", relative_path)
                    csv_files.append({
                        'relative_path': relative_path_with_prefix,
                        'file_name': file
                    })
        return csv_files

    directory = "../data/"
    csv_files_info = list_csv_files(directory)
    for file_info in csv_files_info:
        file_path = file_info['relative_path']
        file_name = file_info['file_name']

        wash_file(file_path, file_name)


def init_clean_json():
    tmp_json = {
        "duplication": {
            "explanation1": None,
            "detailes": [],
            "explanation2": None,
            "filter": [],
            "data": {}
        },
        "absence": {
            "explanation": None,
            "detailes": [],
            "data": {}
        },
        "exception": {
            "explanation": None,
            "detailes": [],
            "data": {}
        },
        "speciality": {
            "explanation1": None,
            "detailes": [],
            "explanation2": None,
            "encode": [],
            "memory_reduction": {
                "activity_learn_log": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "classroom_course": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "classroom_member": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "course_chapter": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "course_task": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "log": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "testpaper": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "testpaper_result": {
                    "ori_mem": None,
                    "wash_mem": None
                },
                "user_learn_statistics_total": {
                    "ori_mem": None,
                    "wash_mem": None
                }
            }
        }
    }
    return tmp_json


if __name__ == "__main__":

    clean_dict = init_clean_json()
    main()

    # 指定要保存的 JSON 文件路径
    json_file_path = "my_dict.json"

    # 将字典保存为 JSON 文件
    with open(json_file_path, "w") as json_file:
        json.dump(clean_dict, json_file, indent=4)


