import argparse
import logging
import os
import shutil
import time


def createReplica(sourcePath: str, replicaPath: str, logPath: str = None):

    os.mkdir(replicaPath)  # create replica directory
    logging.info(f"Created directory at {replicaPath}")

    for dirPath, dirNames, fileNames in os.walk(sourcePath):

        # copy source directory files into replica
        for fileName in fileNames:
            sourceFilePath = f"{dirPath}/{fileName}"
            replicaFilePath = f"{replicaPath}/{fileName}"
            shutil.copy2(sourceFilePath, replicaFilePath)
            logging.info(f"Created copy of {sourceFilePath} at {replicaFilePath}")

        # create nested directories in replica
        for dirName in dirNames:
            createReplica(f"{sourcePath}/{dirName}", f"{replicaPath}/{dirName}")
        break

    return 0


def updateReplica(sourcePath: str, replicaPath: str, logPath: str = None):
    for dirPath, dirNames, fileNames in os.walk(sourcePath):

        for fileName in fileNames:
            replicaFilePath = f"{replicaPath}/{fileName}"
            sourceFilePath = f"{dirPath}/{fileName}"
            try:
                # executes if file is in replica and replica file is not up to date
                if os.path.getmtime(replicaFilePath) != os.path.getmtime(
                    sourceFilePath
                ):
                    shutil.copy2(sourceFilePath, replicaFilePath)
                    logging.info(
                        f"Updated copy of {sourceFilePath} at {replicaFilePath}"
                    )
            except FileNotFoundError as e:
                # executes if file not in replica
                shutil.copy2(sourceFilePath, replicaFilePath)
                logging.info(f"Created copy of {sourceFilePath} at {replicaFilePath}")

        for dirName in dirNames:
            replicaDirPath = f"{replicaPath}/{dirName}"
            if not os.path.exists(replicaDirPath):
                # copy source folder dir and its contents in replica
                createReplica(f"{sourcePath}/{dirName}", replicaDirPath)
            else:
                # update source folder dir in replica
                updateReplica(f"{sourcePath}/{dirName}", replicaDirPath)
        break

    return 0


def deleteReplica(replicaPath: str, sourcePath: str, logPath: str = None):
    if not os.path.exists(sourcePath) and os.path.exists(replicaPath):
        # source directory deleted, delete replica
        shutil.rmtree(replicaPath)
        logging.warning(f"Removed directory at {replicaPath}")
    else:
        for dirPath, dirNames, fileNames in os.walk(replicaPath):

            for fileName in fileNames:
                replicaFilePath = f"{replicaPath}/{fileName}"
                sourceFilePath = f"{sourcePath}/{fileName}"

                if not os.path.exists(sourceFilePath):
                    # delete replica file
                    os.remove(replicaFilePath)
                    logging.warning(f"Removed file at {sourceFilePath}")

            for dirName in dirNames:
                replicaDirPath = f"{replicaPath}/{dirName}"
                sourceDirPath = f"{sourcePath}/{dirName}"
                # check for deleted source dir files in replica dir
                deleteReplica(replicaDirPath, sourceDirPath)
            break

    return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str)
    parser.add_argument("--replica", type=str)
    parser.add_argument("--log", type=str)
    parser.add_argument("--interval", default=10, type=int)
    args = parser.parse_args()

    sourcePath = args.source
    replicaPath = args.replica
    logPath = args.log
    interval = args.interval

    if not os.path.exists(logPath):
        os.mkdir(logPath)

    logging.basicConfig(
        level=logging.INFO,
        filename=f"{logPath}/log.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info(f"Logging changes at {logPath}")

    while True:

        logging.info(f"Checking for updates at {sourcePath}")

        deleteReplica(replicaPath, sourcePath)
        if os.path.exists(sourcePath):
            if not os.path.exists(replicaPath):
                createReplica(sourcePath, replicaPath)
            else:
                updateReplica(sourcePath, replicaPath)
        time.sleep(interval)
