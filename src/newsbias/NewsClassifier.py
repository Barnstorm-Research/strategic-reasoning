from transformers import pipeline
import pandas as pd
import csv

class NewsClassifier:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.classifier = pipeline("text-classification", model="newsmediabias/newsmediabias-classifier")
        self.result_csv_path = 'classification_results.csv'
        self.news_dataset = None

    def load_data(self):
        try:
            self.news_dataset = pd.read_csv(self.csv_file_path, delimiter=';',encoding='utf-8', quoting=csv.QUOTE_NONE, on_bad_lines='skip')
            self.news_dataset = self.news_dataset.dropna(subset=['summary']) #Remove rows with missing 'summary'
        except pd.errors.ParserError as e:
            print("Error while reading CSV:", str(e))

    #extract the summary column from the dataset
    def run_classification(self):
        summary_data = self.news_dataset['summary'].tolist()

        # Create empty lists to store the results
        inputs = []
        labels = []
        scores = []

        # Process the summaries in chunks of 100 until we reach the end of the data
        for i in range(0, len(summary_data), 100):
            chunk = [summary_data[j][0:512] for j in range(i,min(i+100, len(summary_data)))]
            results = self.classifier(chunk)
            # print(results)

            # Append the results to the lists
            for input_text, result in zip(chunk, results):
                inputs.append(input_text)
                labels.append(result['label'])
                scores.append(result['score'])

        # Add the new columns to the existing dataframe
        self.news_dataset['Bias Label'] = labels
        self.news_dataset['Bias Score'] = scores

        # Save the results to a CSV file
        self.news_dataset.to_csv(self.csv_file_path, index=False)


        # Create a DataFrame from the lists
        result_df = pd.DataFrame({'Summary': inputs, 'Bias Label': labels, 'Bias Score': scores})
        
        return result_df

if __name__ == "__main__":
    dataset_path = '/Users/marjanabdollahi/Desktop/BRC/Barnstorm_project_23/IRAD/src/test.csv'
    classifier = NewsClassifier(dataset_path) #create NewsClassifier instance
    classifier.load_data()
    result_df = classifier.run_classification()
    print(result_df.head())
