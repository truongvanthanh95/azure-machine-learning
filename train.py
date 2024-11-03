from sklearn.linear_model import LogisticRegression
import argparse
import os
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory

data_loc = "https://raw.githubusercontent.com/truongvanthanh95/azure-machine-learning/refs/heads/main/loan_data.csv"
ds = TabularDatasetFactory.from_delimited_files(data_loc)


#Save model for current iteration

run = Run.get_context()
df = ds.to_pandas_dataframe().dropna()
gender = LabelEncoder()
df['person_gender'] = gender.fit_transform(df['person_gender'])
education = LabelEncoder()
df['person_education'] = education.fit_transform(df['person_education'])
home_ownership = LabelEncoder()
df['person_home_ownership'] = home_ownership.fit_transform(df['person_home_ownership'])
loan_intent = LabelEncoder()
df['loan_intent'] = home_ownership.fit_transform(df['loan_intent'])
previous_loan_defaults_on_file = LabelEncoder()
df['previous_loan_defaults_on_file'] = home_ownership.fit_transform(df['previous_loan_defaults_on_file'])

x_df = df
y_df = x_df.pop("loan_status")


x_train, x_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.3, random_state=123)

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()

    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy", np.float(accuracy))

    #Save model for current iteration, also include the value for C and max_iter in filename, random_state=
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(model, 'outputs/hyperDrive_{}_{}'.format(args.C,args.max_iter))

if __name__ == '__main__':
    main()