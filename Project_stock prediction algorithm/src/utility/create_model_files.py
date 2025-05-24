import os, json, pickle, torch, shutil


def model_files(
    ticker_name,
    scaler,
    model,
    model_type,
    tickers,
    indicators,
    drop=[],
    binary=False,
    pca=None,
    plan="basic",
    version="no_version",
    report={},
):
    """
    - drop: list to drop columns
    - model_type: pickle or torch
    - binary: binary classification or multiclass
    - Ref1: https://scikit-learn.org/stable/model_persistence.html
    - Ref2: https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
    """

    dir_model = f"./models/{plan}"
    if plan not in os.listdir("./models"):
        os.mkdir(dir_model)

    dir_model += f"/{ticker_name}"
    if ticker_name not in os.listdir(f"./models/{plan}"):
        os.mkdir(dir_model)

    dir_model += f"/v{version}"
    if f"v{version}" not in os.listdir(f"./models/{plan}/{ticker_name}"):
        os.mkdir(dir_model)

    if pca == None:
        pca_flag = False
    else:
        pca_flag = True

    data_structure = {}
    data_structure["tickers"] = tickers
    data_structure["indicators"] = indicators
    data_structure["drop"] = drop
    data_structure["model_type"] = model_type
    data_structure["binary"] = binary
    data_structure["pca"] = pca_flag

    with open(f"{dir_model}/config.json", "w") as file:
        json.dump(data_structure, file, ensure_ascii=False, indent=4)
        print(f"{dir_model}/config.json created")

    with open(f"{dir_model}/scaler.pkl", "wb") as file:
        pickle.dump(scaler, file)
        print(f"{dir_model}/scaler.pkl created")

    if model_type == "pickle":
        with open(f"{dir_model}/model.pkl", "wb") as file:
            pickle.dump(model, file)
            print(f"{dir_model}/model.pkl created")

    elif model_type == "torch":
        torch.save(model, f"{dir_model}/model.pth")
        print(f"{dir_model}/model.pth created")

    elif model_type == "serial_skl":
        # array with models:
        # 0: main model
        # 1: variance model
        # 2: select_from_model
        with open(f"{dir_model}/model.pkl", "wb") as file:
            pickle.dump(model[0], file)
            print(f"{dir_model}/model.pkl created")
        try:
            with open(f"{dir_model}/variance.pkl", "wb") as file:
                pickle.dump(model[1], file)            
            print(f"{dir_model}/variance.pkl created")
        except:
            pass
        try:
            with open(f"{dir_model}/selection.pkl", "wb") as file:
                pickle.dump(model[2], file)
            print(f"{dir_model}/selection.pkl created")
        except:
            pass

    if pca_flag == True:
        with open(f"{dir_model}/pca.pkl", "wb") as file:
            pickle.dump(pca, file)
            print(f"{dir_model}/pca.pkl created")

    with open(f"{dir_model}/report.json", "w") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)
        print(f"{dir_model}/report.json created")