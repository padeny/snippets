import sys
import time
import multiprocessing
from settings import Config as cfg


def helper():
    ...


def main():
    cam_infos = []
    process_info_list = []
    for cam_id, date_region in cam_infos:
        args = (cam_id, date_region,)
        process_info_list.append(
            (multiprocessing.Process(name=f"calib-task-{cam_id}",
                                     target=helper, args=args + (True,)), args)
        )

    if len(process_info_list) == 0:
        time.sleep(cfg.main_process_sleep_time)
        sys.exit(0)

    # 开始执行多进程并由主进程守护子进程
    for process_info in process_info_list:
        process_info[0].daemon = True
        process_info[0].start()

    while 1:
        time.sleep(cfg.subproc_hc_interval)
        for i, process_info in enumerate(process_info_list):
            process, args = process_info[0], process_info[1]
            if not process.is_alive():
                process.close()
                new_process = multiprocessing.Process(name="", target=helper,
                                                      args=args + (False,))
                new_process.daemon = True
                new_process.start()
                process_info_list[i] = (new_process, args)


if __name__ == "__main__":
    main()
