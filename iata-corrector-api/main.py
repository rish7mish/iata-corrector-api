from evaluator import evaluate_corrections

def main():
    result_df = evaluate_corrections('data/validation_set.csv')
    result_df.to_csv('data/evaluation_result.csv', index=False)
    print("Evaluation completed. Results saved to 'data/evaluation_result.csv'.")

if __name__ == "__main__":
    main()
