import requests
from urllib import parse
import re
import os
import time

import pandas as pd
from itertools import tee
from tqdm import tqdm

import yaml


CONFIG_PATH = "config/"


def load_config(file_path):
    with open(os.path.join(CONFIG_P
    
    
    ATH, file_path), encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config


def calc_od(file_name, api_key, delay):
    start_time = time.time()

    config = load_config("config.yaml")

    df = pd.read_csv(
        "{input_dir}/{file_name}".format(
            input_dir=config["dirs"]["input_dir"], file_name=file_name
        ),
        encoding=config["encoding"]["input"],
    )

    distance_list = []
    duration_list = []

    count_s = 0
    count_e = 0

    for (i, row) in tqdm(df.iterrows(), total=df.shape[0]):
        LatOrigin = row[config["colNames"]["origins"]["lat"]]
        LongOrigin = row[config["colNames"]["origins"]["long"]]
        # NameOrigin = row[config['colNames']['origins']['name']]

        LatDest = row[config["colNames"]["destination"]["lat"]]
        LongDest = row[config["colNam
        es"]["destination"]["long"]]
        
        # NameDest = row[config['colNames']['destination']['name']]

        if config["mode"] == "walking":  # walking
            url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&\
                    format=json&\
                    callback=result&\
                    reqCoordType=WGS84GEO&\
                    resCoordType=EPSG3857&\
                    appKey={api_key}&\
                    startX={X_origin}&\
                    startY={Y_origin}&\
                    startName={name_origin}&\
                    endX={X_destination}&\
                    endY={Y_destination}&\
                    endName={name_destination}".format(
                api_key=api_key,
                X_origin=LongOrigin,
                Y_origin=LatOrigin,
                name_origin=parse.quote("출발지"),
                X_destination=LongDest,
                Y_destination=LatDest,
                name_destination=parse.quote("목적지"),
            )
        else:  # driving
            url = "https://apis.openapi.sk.com/tmap/routes?version=1&\
                    format=json&\
                    callback=result&\
                    reqCoordType=WGS84GEO&\
                    resCoordType=EPSG3857&\
                    appKey={api_key}&\
                    startX={X_origin}&\
                    startY={Y_origin}&\
                    startName={name_origin}&\
                    endX={X_destination}&\
                    endY={Y_destination}&\
                    endName={name_destination}".format(
                api_key=api_key,
                X_origin=LongOrigin,
                Y_origin=LatOrigin,
                name_origin=parse.quote("출발지"),
                X_destination=LongDest,
                Y_destination=LatDest,
                name_destination=parse.quote("목적지"),
            )

        url_cleaned = re.sub("\s+", "", url)

        response = requests.get(url_cleaned)

        if response.status_code == 204:
            distance_list.append("결과 값을 Response 받을 수 없습니다.")
            duration_list.append("결과 값을 Response 받을 수 없습니다.")
            count_e += 1
            time.sleep(delay)
        else:
            result = response.json()

            if "error" in result:
                if result["error"]["message"] == "유효하지 않은 API Key입니다.":
                    print("\n")
                    print("[Error] 유효하지 않은 API Key입니다. API Key를 다시 확인해주세요.")
                    quit()

                distance_list.append(result["error"]["message"])
                duration_list.append(result["error"]["message"])
                count_e += 1
                time.sleep(delay)

            else:
                distance_list.append(
                    result["features"][0]["properties"]["totalDistance"] / 1000
                )
                duration_list.append(
                    result["features"][0]["properties"]["totalTime"] / 60
                )
                count_s += 1
                time.sleep(delay)

    df["거리(KM)"] = distance_list
    df["소요시간(분)"] = duration_list

    df.to_csv(
        "{out_dir}/{file_name}_완료.csv".format(
            out_dir=config["dirs"]["output_dir"],
            file_name=re.sub(".csv", "", file_name),
        ),
        encoding=config["encoding"]["output"],
        index=False,
    )

    print("\n" * 2)
    print(
        "All Works Sucessfully Done !! (Execution Time : {}s)".format(
            round(time.time() - start_time, 2)
        )
    )
    print(
        "Total : {count_t} | Success : {count_s} | Error : {count_e}".format(
            count_t=count_s + count_e, count_s=count_s, count_e=count_e
        )
    )
