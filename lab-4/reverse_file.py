# Reverse the content of a file and store it in another file
def reverse_file_content():
    input_file = input("Enter the input file name: ")
    output_file = input("Enter the output file name: ")
    with open(input_file, 'r') as file:
        content = file.read()
    with open(output_file, 'w') as file:
        file.write(content[::-1])
    print(f"Content reversed and saved to {output_file}.")

if __name__ == "__main__":
    reverse_file_content()
