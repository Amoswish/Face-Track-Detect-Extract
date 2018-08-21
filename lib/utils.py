import logging
import os
import time
import uuid
from operator import itemgetter

import cv2
import matplotlib.pyplot as plt
import project_root_dir

log_file_root_path = os.path.join(project_root_dir.project_dir, 'logs')
log_time = time.strftime('%Y_%m_%d_%H_%M', time.localtime(time.time()))


def mkdir(path):
    path.strip()
    path.rstrip('\\')
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    else:
        print(path + 'has existed')


def savepic(savepath, imglist, predict):
    fig = plt.figure(figsize=(10, 6))
    for key, val in enumerate(imglist):
        if key + 1 == 3:
            fig.add_subplot(2, 1, 2)
            plt.imshow(val)
            plt.text(140, -5, 'predict:' + str('%.2f' % predict) + '%', color='red', fontsize=17)
            continue
        fig.add_subplot(2, len(imglist) - 1, key + 1)
        plt.imshow(val)

    plt.savefig(savepath + str(time.time()) + '.png')
    plt.clf()
    plt.close('all')


def logging_config(logfile):
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(logfile, encoding='utf-8')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)


def save_to_file(root_dic, tracker):
    face_collect_time = time.strftime('%Y_%m_%d', time.localtime(time.time()))
    directoryname = './own_face_datasets_side/' + face_collect_time + '/'
    # root_dic = root_dic + str(uuid.uuid1())
    root_dic_side = directoryname + str(uuid.uuid1())
    filter_face_addtional_attribute_list = []
    for item in tracker.face_addtional_attribute:
        if item[2] < 1.4 and item[4] < 1:
            filter_face_addtional_attribute_list.append(item)
    if (len(filter_face_addtional_attribute_list) > 0):
        score_reverse_sorted_list = sorted(filter_face_addtional_attribute_list, key=itemgetter(4))
        # item = score_reverse_sorted_list[0]
        for i, item in enumerate(score_reverse_sorted_list):
            if item[1] > 0.998:
                mkdir(root_dic)
                cv2.imwrite(
                    "{0}/{1}_{2}_{3}_{4}_{5}.jpg".format(root_dic, str(uuid.uuid1()), round(item[1], 5), round(item[2], 4), round(item[3], 4), round(item[4], 4)),
                    item[0])
                break


class Logger():

    def __init__(self, module_name) -> None:
        super().__init__()
        path_join = os.path.join(log_file_root_path, module_name)
        mkdir(path_join)

        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.INFO)
        log_file = os.path.join(path_join, '{}.log'.format(log_time))
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file, encoding='utf-8')
            fh.setLevel(logging.INFO)

            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s -  %(threadName)s - %(process)d ")
            ch.setFormatter(formatter)
            fh.setFormatter(formatter)
            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

    def error(self, msg, *args, **kwargs):
        if self.logger is not None:
            self.logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.logger is not None:
            self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        if self.logger is not None:
            self.logger.warning(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.logger is not None:
            self.logger.warning(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        if self.logger is not None:
            self.logger.exception(msg, *args, exc_info=True, **kwargs)
