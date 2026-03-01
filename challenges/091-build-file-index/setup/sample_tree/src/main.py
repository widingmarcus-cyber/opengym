def main():
    print("Hello, World!")
    data = load_data()
    process(data)
    save_results(data)

if __name__ == "__main__":
    main()