PATIENT_NOTES_SUMMARY_PROMPT = """
        Generate a concise medical summary for the following patient:

        Patient Information:
        - Name: {patient_name}
        - Age: {age} years old
        - Date of Birth: {date_of_birth}

        Medical Notes:
        {notes_text}

        Please provide a structured summary that includes:
        1. Key diagnoses and conditions mentioned
        2. Current medications or treatments
        3. Recent observations and vital signs
        4. Any concerning symptoms or changes
        5. Recommended follow-up actions

        Keep the summary professional, concise, and focused on clinically relevant information.
        Format the response in clear paragraphs without using markdown headers.
"""
