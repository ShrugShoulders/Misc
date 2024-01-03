import json
import os

def organize_json_vertically(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                print(f"File: {filename}")
                print("-" * 30)
                
                for key, value in data.items():
                    print(f"{key}: {value}")
                
                print("\n")

            # Save the organized data back to the file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
                print(f"Organized data saved back to {filename}\n")

if __name__ == "__main__":
    # Take user input for the directory
    user_directory = input("Enter the path to the directory containing your JSON files: ")
    
    # Check if the entered directory exists
    if os.path.exists(user_directory):
        organize_json_vertically(user_directory)
    else:
        print("Directory not found. Please provide a valid directory path.")