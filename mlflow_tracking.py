import mlflow
import os

"""Log params and artifact"""
def tracking_model(question, answer, model_params, text_splitter_params):
    with mlflow.start_run() as run:
        mlflow.log_params(model_params)
        mlflow.log_params(text_splitter_params)
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        with open("outputs/answer-log.txt", "w") as f:
            f.write("Question from user: \n")
            f.write(question)
            f.write("\n")
            f.write("Answer from model: \n")
            f.write(answer)

        mlflow.log_artifacts("outputs")
  