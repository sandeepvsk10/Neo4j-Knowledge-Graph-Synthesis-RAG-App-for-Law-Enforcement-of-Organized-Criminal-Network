import os

#load transcript
def load_transcripts(file_prefix, start_id, end_id):
    """
    Combine content from multiple text files into a single string.

    Parameters:
    - file_prefix: The prefix of the file names (e.g., 'transcrip_id_').
    - start_id: The starting ID number for the files (e.g., 1).
    - end_id: The ending ID number for the files (e.g., 2).

    Returns:
    - A single string containing the combined content of all files.
    """
    # Initialize an empty string to store the combined content
    loaded_call_transcript = ""

    #with open("./Call Transcripts/LLM Generated Transcript.txt","r",encoding = "utf-8") as file:
    #call_transcript = file.read()

    for i in range(start_id, end_id + 1):
        filename = f'{file_prefix}{i}.txt'  # Creates the filename dynamically
        try:
            # Open and read each file
            with open("./call_transcripts/"+ filename, 'r',encoding = "utf-8") as file:
                content = file.read()
                loaded_call_transcript += content + "\n" + ("-"*100) + "\n" # Append the content with a newline
        except FileNotFoundError:
            print(f"File {os.path.join(filename)} not found.")

    return loaded_call_transcript
