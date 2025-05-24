import json, pickle, torch


def prepare_prediction_structure(ticker):
    """
    - ticker:
    - Return: (config, scaler, model)
    """
    # Read json of configurations
    with open(f"./models/{ticker}/config.json", "r") as file:
        config = json.load(file)

    # Read scaler
    with open(f"./models/{ticker}/scaler.pkl", "rb") as file:
        scaler = pickle.load(file)

    # Read PCA
    try:
        with open(f"./models/{ticker}/pca.pkl", "rb") as file:
            pca = pickle.load(file)
    except:
        pca = None

    # Read model
    if config["model_type"] == "pickle":
        with open(f"./models/{ticker}/model.pkl", "rb") as file:
            model = pickle.load(file)

    elif config["model_type"] == "torch":
        model = torch.load(f"./models/{ticker}/model.pth")
        model.eval()

    elif config["model_type"] == "serial_skl":
        model = []
        with open(f"./models/{ticker}/model.pkl", "rb") as file:
            m = pickle.load(file)
        model.append(m)
        with open(f"./models/{ticker}/variance.pkl", "rb") as file:
            m = pickle.load(file)
        model.append(m)
        with open(f"./models/{ticker}/selection.pkl", "rb") as file:
            m = pickle.load(file)
        model.append(m)

    return config, scaler, model, pca


def data_pipeline(data, sel, model):

    data = sel.transform(data)
    data = model.transform(data)
    return data
